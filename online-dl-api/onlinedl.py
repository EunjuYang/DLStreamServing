import os, time
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
import quadprog
import numpy as np


class MyError(Exception):
    __module__ = Exception.__module__

    def __str__(self):
        return "not yet supported"


def _check_attribute_error(target, arg_name):
    if arg_name == 'tt':
        try:
            target.target_tensors
        except AttributeError:
            return None
        else:
            return target.target_tensors
    elif arg_name == 'wm':
        try:
            target.weighted_matrics
        except AttributeError:
            return None
        else:
            return target.weighted_matrics


def _k_subabs(y_true, y_pred):
    return K.mean(K.abs(y_true - y_pred), axis=-1)


class OnlineDL:

    def __init__(self,
                 model,
                 online_method='cont',
                 framework='keras'):
        super(OnlineDL, self).__init__()
        if model is None or online_method is None or framework is None:
            raise TypeError
        self.model = None
        self.online_method = online_method
        self.framework = framework
        if self.online_method == 'inc':
            if self.framework == 'keras':
                # check attribute error which is mainly caused by not declared value.
                _wm = _check_attribute_error(model, 'wm')
                _tt = _check_attribute_error(model, 'tt')

                # recompile the keras model
                self.model = model.compile(optimizer=model.optimizer,
                                           loss=model.loss,
                                           metrics=model.metrics + [_k_subabs],
                                           loss_weights=model.loss_weights,
                                           sample_weight_mode=model.sample_weight_mode if model.sample_weight_mode else None,
                                           weighted_metrics=_wm,
                                           target_tensors=_tt)
            elif self.framework == 'tf':
                raise MyError  # TODO make tf code

        elif self.online_method == 'cont':
            if self.framework == 'keras':
                # check attribute error which is mainly caused by not declared value.
                _wm = _check_attribute_error(model, 'wm')
                _tt = _check_attribute_error(model, 'tt')

                self.model = Sequential()
                for layer in model.layers:
                    self.model.add(layer)

                self.opt_fn = model.optimizer
                self.loss_fn = model.loss_functions[0]
                self.batch_input_shape = (-1,) + model.input_shape[1:]
                self.batch_output_shape = (-1,) + model.output_shape[1:]


            elif self.framework == 'tf':
                raise MyError  # TODO make tf code


def project2cone2(gradient_np, memories_np, margin=0.5, eps=1e-3):
    """
        Solves the GEM dual QP described in the paper given a proposed
        gradient "gradient", and a memory of task gradients "memories".
        Overwrites "gradient" with the final projected update.

        input:  gradient, p-vector
        input:  memories, (t * p)-vector
        output: x, p-vector
    """
    t = memories_np.shape[0]
    P = np.dot(memories_np, memories_np.transpose())
    P = 0.5 * (P + P.transpose()) + np.eye(t) * eps
    q = np.dot(memories_np, gradient_np) * -1
    G = np.eye(t)
    h = np.zeros(t) + margin
    v = quadprog.solve_qp(P, q, G, h)[0]
    x = np.dot(v, memories_np) + gradient_np
    return x


# This is a inMemory for Continual Learning
# Therefore, we need to additionally create inMemory for Incremental Learning
class inMemory:

    def __init__(self, num_ami, episodic_mem_size, b_input_shape, b_output_shape):
        self.prev_memcnt = None
        self.memcnt = [0] * num_ami
        self.episodic_mem_size = episodic_mem_size
        self.memory_data = np.zeros([num_ami, episodic_mem_size] + list(b_input_shape[1:]))
        self.memory_target = np.zeros([num_ami, episodic_mem_size] + list(b_output_shape[1:]))


    def insert(self, x, y, ids):
        argindex = np.squeeze(np.argsort(ids, axis=0, kind='heapsort'))
        u, indices = np.unique(ids[argindex], return_index=True)
        bsz_list = np.append(indices, [len(x)])
        self.prev_memcnt = self.memcnt.copy()
        for enum, id in enumerate(u):
            endcnt = min(self.episodic_mem_size, self.memcnt[id]+bsz_list[enum+1]-bsz_list[enum])
            effbsz = endcnt - self.memcnt[id]
            self.memory_data[id, self.memcnt[id]: endcnt] = x[argindex][bsz_list[enum+1]-effbsz:bsz_list[enum+1]]
            self.memory_target[id, self.memcnt[id]: endcnt] = y[argindex][bsz_list[enum+1]-effbsz:bsz_list[enum+1]]
            self.memcnt[id] += effbsz
            if self.memcnt[id] == self.episodic_mem_size:
                self.memcnt[id] = 0

    def get(self):
        x, y = [], []
        for i in range(len(self.prev_memcnt)):
            x.append(self.memory_data[i, :self.memcnt[i]]) if self.memcnt[i] else None
            y.append(self.memory_target[i, :self.memcnt[i]]) if self.memcnt[i] else None
        return x, y

    def compare(self):
        pass

    def update(self):
        pass


class ContinualDL(OnlineDL):

    def __init__(self, model, online_method='cont', framework='keras', num_ami=1, episodic_mem_size=100):
        super(ContinualDL, self).__init__(model, online_method, framework)
        self.inMemory = inMemory(num_ami, episodic_mem_size, self.batch_input_shape, self.batch_output_shape)
        self.projected_gradients = []
        for v in range(len(self.model.trainable_weights)):
            self.projected_gradients.append(
                tf.Variable(tf.zeros(model.trainable_weights[v].get_shape()), trainable=False))


    def consume(self, data, target, id):
        data = data.reshape(self.batch_input_shape)
        x = tf.cast(data, tf.float32)
        with tf.GradientTape() as tape:
            pred = self.model(x)
            loss_value = self.loss_fn(target, pred)
        now_grads = tape.gradient(loss_value, self.model.trainable_weights)
        flat_now_grad = tf.concat([tf.reshape(grad, [-1]) for grad in now_grads], 0)

        self.inMemory.insert(data, target, id)
        prev_x, prev_y = self.inMemory.get()
        if prev_x != []:
            flat_prev_grads = []
            for i in range(len(prev_x)):
                _px = tf.cast(prev_x[i], tf.float32)
                with tf.GradientTape() as tape:
                    _px = self.model(_px)
                    prev_loss_value = self.loss_fn(prev_y[i], _px)
                prev_grads = tape.gradient(prev_loss_value, self.model.trainable_weights)
                flat_prev_grads.append(tf.concat([tf.reshape(grad, [-1]).numpy() for grad in prev_grads], 0))

            array_dotp = []
            for flat_prev_grad in flat_prev_grads:
                array_dotp.append(tf.reduce_sum(tf.multiply(flat_now_grad, flat_prev_grad)))

            if np.sum(np.less(array_dotp, 0)):
                flat_now_grad = project2cone2(flat_now_grad.numpy().astype('float64'),
                                         np.asarray(flat_prev_grads, dtype=np.float64), margin=0.5)


        print('hi ch')


def _data_generator_for_test(size, type='value', range=(1,2)):
    if type=='int':
        return np.random.randint(range[0], range[1], size=size)
    elif type=='value':
        return np.random.rand(size)



# This is main code for TEST
if __name__ == '__main__':
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Conv1D

    gpu_devices = tf.config.experimental.list_physical_devices('GPU')
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)

    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(6, 6)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='Adadelta',
                  loss='mse')

    # pseudo data generator, batch_-(input_x, input_y, ami_id)
    num_ami = 10
    batch_size = 5
    look_back = 36
    look_forward = 1
    batch_input_x = _data_generator_for_test(batch_size*look_back)
    batch_input_x = batch_input_x.reshape(batch_size, look_back)
    batch_input_y = _data_generator_for_test(batch_size*look_forward)
    batch_input_y = batch_input_y.reshape(batch_size, look_forward)
    batch_ami_id = _data_generator_for_test(batch_size * look_forward, type='int', range=(0, num_ami))
    batch_ami_id = batch_ami_id.reshape(batch_size, look_forward)

    x = ContinualDL(model, num_ami=num_ami)
    x.consume(batch_input_x, batch_input_y, batch_ami_id)
    print('hi')