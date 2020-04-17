"""
This file define API supporting deep learning based stream event processing.
It provides client API which gets formatted-stream from streamDL platform.
"""
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError
import kafka, os, threading, sys, time
import math
import numpy as np

IS_BROKER = False


class StreamDLStub():

    def __init__(self,
                 kafka_bk,
                 cep_id,
                 stream_bk,
                 batch_size,
                 dtype,
                 adaptive_batch_mode=True):
        """

        :param kafka_bk: information of KAFKA Broker
        :param cep_id: cep id of this deep learning model
        :param stream_bk: information of streamDL Broker
        :param batch_size: batch size of stream data provider
        """

        self.kafka_bk = kafka_bk
        self.cep_id = cep_id
        self.stream_bk = stream_bk
        self.consumer = Consumer(kafka_bk=kafka_bk,
                                 group_id=cep_id,
                                 topic=cep_id,
                                 dtype=dtype)
        self.buffer = self.consumer.get_buffer()
        self.batch_size = batch_size
        self.dtype = dtype

        if IS_BROKER:
            lb_size, is_train, lf_size = self._get_stream_fmt_from_broker()
            self.lb_size = lb_size
            self.is_train = is_train
            self.lf_size = lf_size

        self.consumer.start()
        self.adaptive_batch = adaptive_batch_mode
        if adaptive_batch_mode:
            self.batch_train_generator = self._adaptive_batch_train_generator
        else:
            self.batch_train_generator = self._batch_train_generator

    def _get_stream_fmt_from_broker(self):
        # grpc call
        lb_size = None
        is_train = None
        lf_size = None
        return lb_size, is_train, lf_size

    def set_stream_fmt(self, lb_size, is_train, lf_size=0):
        """
        setting stream data format
        :param lb_size: (int) look back window size
        :param is_train: (bool) is stream used for train or not
        :param lf_size: (int) look forward window size
        :return:
        """
        self.lb_size = lb_size
        self.is_train = is_train
        self.lf_size = lf_size

    def _adaptive_batch_train_generator(self):

        while True:
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            elif len(self.buffer) < self.batch_size:
                bs = len(self.buffer)
            else:
                bs = self.batch_size
            x_shape = (bs, self.lb_size)
            y_shape = (bs, self.lf_size)
            x_batch = np.zeros(shape=x_shape, dtype=self.dtype)
            y_batch = np.zeros(shape=y_shape, dtype=self.dtype)

            for i in range(bs):
                x_batch[i] = self.buffer[0][:self.lb_size]
                y_batch[i] = self.buffer[0][self.lb_size:]
                self.buffer.pop(0)

            yield (bs, x_batch, y_batch)

    def _batch_train_generator(self):

        while True:

            x_shape = (self.batch_size, self.lb_size)
            y_shape = (self.batch_size, self.lf_size)
            x_batch = np.zeros(shape=x_shape, dtype=self.dtype)
            y_batch = np.zeros(shape=y_shape, dtype=self.dtype)

            while len(self.buffer) < self.batch_size:
                time.sleep(0.1)

            for i in range(self.batch_size):
                x_batch[i] = self.buffer[0][:self.lb_size]
                y_batch[i] = self.buffer[0][self.lb_size:]
                self.buffer.pop(0)

            yield (self.batch_size, x_batch, y_batch)


class IncStreamDLStub(StreamDLStub):

    def __init__(self, kafka_bk, cep_id, stream_bk, batch_size, dtype):

        super(IncStreamDLStub, self).__init__(kafka_bk, cep_id, stream_bk, batch_size, dtype)
        self.ld = 1
        self.last_timestep = 0
        self.err_queue = SizeQueue(5, 0.3)
        self.prev_queue_size = 0
        self.precision = 1e-10
        self.delta = 1e-2
        self.mult1 = 1
        self.multiplier = (60000/(self.ld ** (1/3.)))   # normalization


    def set_beta_for_incremental(self, beta, beta1):
        self.beta = beta
        self.beta1 = beta1

    def solver_naive2(self, a, b, d):
        b /= a
        d /= a
        a = 1 # FIXME: Seems that it is not required.

        q = (-b ** 2) / 9
        r = (-27 * d - 2 * b ** 3) / 54

        disc = q ** 3 + r ** 2

        if disc > 0:
            s = r + (disc) ** (1 / 2.)
            s = -((-s) ** (1 / 3.)) if s < 0 else (s ** (1 / 3.))
            t = r - (disc) ** (1 / 2.)
            t = -((-t) ** (1 / 3.)) if s < 0 else (s ** (1 / 3.))

            term1 = b / 3.0
            x1 = -term1 + s + t
            term1 += (s + t) / 2.0
            realRoot12 = -term1 # FIXME: Seems that it is not required.
            return x1
        else:
            print('nonono')
            return -1

    def batch_calc3_batch(self, test_err, e, prev_err):
        a = 1 / self.ld
        b = (self.beta * e - self.beta1 * self.mult1)
        d = -self.multiplier * test_err / prev_err / e
        x2 = self.solver_naive2(a, b, d)
        return x2

    def fe_batch(self, e, e_rate):
        d = self.batch_calc3_batch(e_rate, e, 1)
        return (d ** 2) / self.ld / 2 + d * e * self.beta - self.beta1 * d * self.mult1 + self.multiplier * e_rate / e / d

    def fed_batch(self, e, e_rate):
        return (self.fe_batch(e + self.delta, e_rate) - self.fe_batch(e, e_rate)) / self.delta

    def newton_batch(self, x_start, x_end, e_rate, go):
        x = go
        dx = self.fed_batch(x, e_rate) # FIXME: Seems that it is not required.
        r = 0.99
        a = 1
        x_prev = -1
        i = 0
        if True:
            while math.fabs(x-x_prev) > self.precision:
                a *= r
                dx = self.fed_batch(x, e_rate)
                x_prev = x
                x -= a*dx
                x = x_end if x > x_end else x
                x = x_start  if x < x_start else x
                i=i+1
        global suma
        global count
        suma = suma+i
        count = count + 1
        print('newton result', x_end, x, i, suma/float(count))
        return (self.batch_calc3_batch(e_rate, x, 1), x)

    def na(self, f):
        return int(math.floor(f))

    def batch_train_generator(self, test_err, FIX=None):
        self.err_queue.push(test_err)

        timestep = time.time() - self.last_timestep

        queue_size = len(self.buffer)
        self.ld = (queue_size - self.prev_queue_size) / timestep if self.last_timestep else 1

        req = self.beta1 / (1 - self.beta * self.ld)
        if timestep < req:
            time.sleep(req - timestep)
            timestep = req

        amount = sys.maxsize
        while queue_size < amount:
            tmpe = (timestep - self.beta1) / (self.beta * self.ld * timestep)

            if FIX:
                batch_star = FIX
                epoch = tmpe
            else:
                batch_star, epoch = self.newton_batch(1, tmpe, test_err / self.err_queue.avr, tmpe)
            epoch = max(int(math.floor(epoch)), 1)
            amount = max(self.na(batch_star), 1)

            if queue_size < amount:
                time.sleep((amount - queue_size) / self.ld - timestep)
            elif int(math.floor(queue_size)) > amount:
                print(f'check queue_size is {queue_size} and amount size is {amount}')

        x_shape = (amount, self.lb_size)
        y_shape = (amount, self.lf_size)
        x_batch = np.zeros(shape=x_shape, dtype=self.dtype)
        y_batch = np.zeros(shape=y_shape, dtype=self.dtype)

        for i in range(amount):
            x_batch[i] = self.buffer[0][:self.lb_size]
            y_batch[i] = self.buffer[0][self.lb_size:]
            self.buffer.pop(0)

        self.prev_queue_size = len(self.buffer)
        self.last_timestep = time.time()

        yield (x_batch, y_batch, epoch)


# SizeQueue is used in IncStreamDLStub()
class SizeQueue:

    def __init__(self, size, value):
        self.sum = 0.0
        self.size = size
        self.div = max(size, 1)
        self.q = []
        for _ in range(size):
            self.q.append(value)
            self.sum += value
        self.avr = self.sum / self.div

    def push(self, value):
        self.q.append(value)
        p = self.q.pop(0)
        self.sum += (value-p)
        # self.max = max(value, self.max)
        self.avr = self.sum / self.div
        return p

    def max(self):
        return max(self.q)


class Consumer(threading.Thread):

    def __init__(self, kafka_bk, group_id, topic, dtype=np.float):
        """
        :param kafka_bk: information of kafka broker
        :param group_id: group id of cnonsumer
        :param topic: topic name
        :param dtype: data type of stream data
        """

        super(Consumer, self).__init__()
        conf = {
            'bootstrap.servers': kafka_bk,
            'group.id': group_id
        }
        self.topic = topic
        self.kafka_bk = kafka_bk
        self.dtype = dtype

        # wait until topic is created in Kafka broker
        while not self._check_topic(topic):
            time.sleep(1)
            continue

        # create Kafka Consumer
        self.consumer = KafkaConsumer(conf)
        self.consumer.subscribe([topic])
        self.buffer = []

    def run(self):

        while True:

            msg = self.consumer.poll(1)
            if msg is None:
                continue
            elif msg.error():
                if msg.error.code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d \n" % (msg.topic(), msg.partition(), msg.offset()))
                else:
                    continue
            else:
                data = msg.value().decode('utf-8').split(',')
                data = np.array(data[:-1])
                data = data.astype(self.dtype)
                self.buffer.append(data)

    def get_buffer(self):
        return self.buffer

    def _check_topic(self, topic):
        cons = kafka.KafkaConsumer(group_id='check_topics', bootstrap_servers=self.kafka_bk)
        topics = cons.topics()
        if topic in topics:
            return True
        else:
            return False
