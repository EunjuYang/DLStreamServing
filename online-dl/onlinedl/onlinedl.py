import os, time
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.models import Sequential
import quadprog
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from .utils import ModelManager

class OnlineDLError(Exception):
    __module__ = Exception.__module__

    def __str__(self):
        return "not yet supported"


def _k_subabs(y_true, y_pred):
    return K.mean(K.abs(y_true - y_pred), axis=-1)


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


class inMemory:

    def __init__(self, num_ami, episodic_mem_size, b_input_shape, b_output_shape):
        """
        Memory used in ContinualDL. inMemory works in "ring buffer" manner
        :param num_ami:
        :param episodic_mem_size:
        :param b_input_shape:
        :param b_output_shape:
        """
        self.memcnt = [0] * num_ami
        self.episodic_mem_size = episodic_mem_size
        self.memory_data = np.zeros([num_ami, episodic_mem_size] + list(b_input_shape[1:]))
        self.memory_target = np.zeros([num_ami, episodic_mem_size] + list(b_output_shape[1:]))

    # This is a ring-buffer method which is compared with proposed method
    def insert(self, x, y, ids):
        argindex = np.squeeze(np.argsort(ids, axis=0, kind='heapsort'))
        u, indices = np.unique(ids[argindex], return_index=True)
        bsz_list = np.append(indices, [len(x)])
        for enum, id in enumerate(u):
            endcnt = min(self.episodic_mem_size, self.memcnt[id] + bsz_list[enum + 1] - bsz_list[enum])
            effbsz = endcnt - self.memcnt[id]
            self.memory_data[id, self.memcnt[id]: endcnt] = x[argindex][bsz_list[enum + 1] - effbsz:bsz_list[enum + 1]]
            self.memory_target[id, self.memcnt[id]: endcnt] = y[argindex][
                                                              bsz_list[enum + 1] - effbsz:bsz_list[enum + 1]]
            self.memcnt[id] += effbsz
            if self.memcnt[id] == self.episodic_mem_size:
                self.memcnt[id] = 0

    def get(self):
        x, y = [], []
        for i in range(len(self.memcnt)):
            x.append(self.memory_data[i, :self.memcnt[i]]) if self.memcnt[i] else None
            y.append(self.memory_target[i, :self.memcnt[i]]) if self.memcnt[i] else None
        return x, y


class cossimMemory(inMemory):

    def __init__(self, num_ami, episodic_mem_size, b_input_shape, b_output_shape):
        """
        Memory used in ContinualDL. cossimMemory works using cos-similarity
        :param num_ami:
        :param episodic_mem_size:
        :param b_input_shape:
        :param b_output_shape:
        """
        super(cossimMemory, self).__init__(num_ami, episodic_mem_size, b_input_shape, b_output_shape)
        self.given_criteria = np.ones((b_input_shape[1:]))

    def insert(self, x, y, ids):
        argindex = np.squeeze(np.argsort(ids, axis=0, kind='heapsort'))
        u, indices = np.unique(ids[argindex], return_index=True)
        bsz_list = np.append(indices, [len(x)])
        for enum, id in enumerate(u):
            tmp_np = np.concatenate(
                (self.memory_data[id, :self.memcnt[id]], x[argindex][bsz_list[enum]:bsz_list[enum + 1]]))
            if tmp_np.shape[0] != 1:
                tmp_np_y = np.concatenate(
                    (self.memory_target[id, :self.memcnt[id]], y[argindex][bsz_list[enum]:bsz_list[enum + 1]]))
                cossim_results = cosine_similarity(tmp_np.reshape((tmp_np.shape[0], -1)),
                                                   self.given_criteria.reshape(1, -1))
                cossim_results = cossim_results.reshape(-1)
                cossim_range = np.linspace(min(cossim_results), max(cossim_results), self.episodic_mem_size + 1)
                store_idx = []
                store_idx.append(np.where(cossim_results == (min(cossim_results)))[0][0])
                store_idx.append(np.where(cossim_results == (max(cossim_results)))[0][0])
                for i in range(len(cossim_range[1:-2])):
                    idx_bool = (cossim_results >= cossim_range[i + 1]) & (cossim_results < cossim_range[i + 2])
                    if not np.any(idx_bool):
                        continue
                    np_idx = np.where(idx_bool.reshape(-1) == True)
                    store_idx.append(np.random.choice(np.asarray(np_idx).reshape(-1)))
                self.memory_data[id, :len(store_idx)] = tmp_np[store_idx]
                self.memory_target[id, :len(store_idx)] = tmp_np_y[store_idx]
                self.memcnt[id] = len(store_idx)
            else:
                self.memory_data[id, :1] = tmp_np[0]
                self.memory_target[id, :1] = y[argindex][bsz_list[enum]:bsz_list[enum + 1]]
                self.memcnt[id] = 1

    def compare_insert(self, x, y, ids):
        argindex = np.squeeze(np.argsort(ids, axis=0, kind='heapsort'))
        u, indices = np.unique(ids[argindex], return_index=True)

        TAM = [0] * len(u)
        bsz_list = np.append(indices, [len(x)])
        for enum, id in enumerate(u):
            tmp_np = np.concatenate(
                (self.memory_data[id, :self.memcnt[id]], x[argindex][bsz_list[enum]:bsz_list[enum + 1]]))
            if tmp_np.shape[0] != 1:
                tmp_np_y = np.concatenate(
                    (self.memory_target[id, :self.memcnt[id]], y[argindex][bsz_list[enum]:bsz_list[enum + 1]]))
                cossim_results = cosine_similarity(tmp_np.reshape((tmp_np.shape[0], -1)),
                                                   self.given_criteria.reshape(1, -1))
                cossim_results = cossim_results.reshape(-1)
                cossim_range = np.linspace(min(cossim_results), max(cossim_results), self.episodic_mem_size + 1)
                store_idx = []
                store_idx.append(np.where(cossim_results == (min(cossim_results)))[0][0])
                store_idx.append(np.where(cossim_results == (max(cossim_results)))[0][0])
                for i in range(len(cossim_range[1:-2])):
                    idx_bool = (cossim_results >= cossim_range[i + 1]) & (cossim_results < cossim_range[i + 2])
                    if not np.any(idx_bool):
                        continue
                    np_idx = np.where(idx_bool.reshape(-1) == True)
                    store_idx.append(np.random.choice(np.asarray(np_idx).reshape(-1)))

                if np.var(self.memory_data[id, :self.memcnt[id]]) < np.var(tmp_np[store_idx]):
                    TAM[enum] = 1

                if TAM[enum]:
                    self.memory_data[id, :len(store_idx)] = tmp_np[store_idx]
                    self.memory_target[id, :len(store_idx)] = tmp_np_y[store_idx]
                    self.memcnt[id] = len(store_idx)
            else:
                self.memory_data[id, :1] = tmp_np[0]
                self.memory_target[id, :1] = y[argindex][bsz_list[enum]:bsz_list[enum + 1]]
                self.memcnt[id] = 1
        return TAM


class OnlineDL:

    def __init__(self,model_name,online_method='cont',framework='keras'):

        # TODO
        self.model_manager = ModelManager()
        model_path = self.model_manager.pull(model_name)

        # Parameters
        online_method = os.getenv('ONLINE_METHOD', online_method)
        framework = os.getenv('FRAMEWORK', framework)
        self.save_weight = bool(os.getenv('SAVEWEIGHT', None))

        self.model_filename = model_path.split('/')[-1]
        self.online_method = online_method
        self.framework = framework

        model = tf.keras.models.load_model(model_path)

        if self.online_method == 'inc':
            if self.framework == 'keras':
                # check attribute error which is mainly caused by not declared value.
                _wm = self._check_attribute_error(model, 'wm')
                _tt = self._check_attribute_error(model, 'tt')

                # recompile the keras model
                self.model = model.compile(optimizer=model.optimizer,
                                           loss=model.loss,
                                           metrics=model.metrics + [_k_subabs],
                                           loss_weights=model.loss_weights,
                                           sample_weight_mode=model.sample_weight_mode if model.sample_weight_mode else None,
                                           weighted_metrics=_wm,
                                           target_tensors=_tt)
            elif self.framework == 'tf':
                # TODO make tf code
                raise OnlineDLError

        elif self.online_method == 'cont':
            if self.framework == 'keras':
                # check attribute error which is mainly caused by not declared value.
                _wm = self._check_attribute_error(model, 'wm')
                _tt = self._check_attribute_error(model, 'tt')

                self.model = Sequential()
                for layer in model.layers:
                    self.model.add(layer)

                self.opt_fn = model.optimizer
                self.loss_fn = model.loss_functions[0]
                self.batch_input_shape = (-1,) + model.input_shape[1:]
                self.batch_output_shape = (-1,) + model.output_shape[1:]


            elif self.framework == 'tf':
                # TODO make tf code
                raise OnlineDLError

    def save(self):
        self.model.save_weights(self.model_filename + '/ckpts')
        self.model_manager.push(self.model_filename + '/ckpts')
        # TODO push to model repository

    @staticmethod
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


class ContinualDL(OnlineDL):

    def __init__(self, model, online_method='cont', framework='keras', mem_method='ringbuffer', num_ami=1, episodic_mem_size=100, cont_method=''):
        super(ContinualDL, self).__init__(model, online_method, framework)

        num_ami = int(os.getenv('NUM_AMI', num_ami))
        episodic_mem_size = int(os.getenv('EPISODIC_MEM_SIZE', episodic_mem_size))
        self.mem_method = os.getenv('MEM_METHOD', mem_method)
        self.cont_method = os.getenv('CONT_METHOD', cont_method)

        if self.mem_method == 'ringbuffer':
            self.inMemory = inMemory(num_ami, episodic_mem_size, self.batch_input_shape, self.batch_output_shape)
        elif self.mem_method == 'cossim':
            self.inMemory = cossimMemory(num_ami, episodic_mem_size, self.batch_input_shape, self.batch_output_shape)
        self.projected_gradients = []
        for v in range(len(self.model.trainable_variables)):
            self.projected_gradients.append(
                tf.Variable(tf.zeros(self.model.trainable_variables[v].get_shape()), trainable=False))

        if self.cont_method == "SCHEDULE_METHOD":
            self.consume = self._compare_consume
        else:
            self.consume = self._consume

    def _consume(self, data, target, id):

        data = data.reshape(self.batch_input_shape)
        x = tf.cast(data, tf.float32)
        with tf.GradientTape() as tape:
            pred = self.model(x)
            loss_value = self.loss_fn(target, pred)
        now_grads = tape.gradient(loss_value, self.model.trainable_weights)
        flat_now_grad = tf.concat([tf.reshape(grad, [-1]) for grad in now_grads], 0)

        prev_x, prev_y = self.inMemory.get()
        self.inMemory.insert(data, target, id)

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
        offset = 0
        for v in self.projected_gradients:
            shape = v.get_shape()
            v_params = 1
            for dim in shape:
                v_params *= dim
            v.assign(tf.reshape(tf.cast(flat_now_grad[offset:offset + v_params], dtype=tf.float32), shape))
            offset += v_params

        self.opt_fn.apply_gradients(
            zip(self.projected_gradients, self.model.trainable_weights))

    def _compare_consume(self, data, target, id):
        data = data.reshape(self.batch_input_shape)
        x = tf.cast(data, tf.float32)
        with tf.GradientTape() as tape:
            pred = self.model(x)
            loss_value = self.loss_fn(target, pred)
        now_grads = tape.gradient(loss_value, self.model.trainable_weights)
        flat_now_grad = tf.concat([tf.reshape(grad, [-1]) for grad in now_grads], 0)

        prev_x, prev_y = self.inMemory.get()
        TAM = self.inMemory.compare_insert(data, target, id)

        if prev_x != []:
            if any(TAM):
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
        offset = 0
        for v in self.projected_gradients:
            shape = v.get_shape()
            v_params = 1
            for dim in shape:
                v_params *= dim
            v.assign(tf.reshape(tf.cast(flat_now_grad[offset:offset + v_params], dtype=tf.float32), shape))
            offset += v_params

        self.opt_fn.apply_gradients(
            zip(self.projected_gradients, self.model.trainable_weights))

class IncrementalDL(OnlineDL):

    def __init__(self, model, online_method='inc', framework='keras'):

        super(IncrementalDL, self).__init__(model, online_method, framework)

        pass

    # profiling procedure is implemented at once when calling __init__ function.
    def profile(self):
        # save weight to restore self.model.weights
        saved_weights = self.model.get_weights()

        inp = []
        profile = []
        batch = 32
        epoch = 30

        # We checked longer delay when first calling model.fit() than after first.
        # Therefore, for warm-start, we call model.fit() before profiling.
        dataX, dataY = self._build_data_for_profile(batch)
        self.model.fit(dataX, dataY, batch_size=batch, epochs=1, verbose=0, shuffle=False)

        for i in range(1, epoch+1, 1):
            dataX, dataY = self._build_data_for_profile(batch)
            s = time.time()
            self.model.fit(dataX, dataY, batch_size=batch, epochs=i, verbose=0, shuffle=False)
            profile += [time.time() - s]
            inp += [i]
        lr = LinearRegression().fit(np.array(inp).reshape((-1, 1)), profile)

        # restore weight in self.model.weights
        self.model.set_weights(saved_weights)
        return lr.coef_[0], lr.intercept_

    def _build_data_for_profile(self, size):
        # calculate x_shape and y_shape
        x_shape, y_shape = 1, 1
        for i in self.batch_input_shape[1:]:
            x_shape *= i
        for i in self.batch_output_shape[1:]:
            y_shape *= i
        return np.random.rand(size*x_shape).reshape(self.batch_input_shape), \
               np.random.rand(size*y_shape).reshape(self.batch_output_shape)