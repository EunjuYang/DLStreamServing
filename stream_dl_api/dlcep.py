"""
This file define API supporting deep learning based stream event processing.
It provides client API which gets formatted-stream from streamDL platform.
"""
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError
import kafka, os, threading, sys, time
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

    def batch_interaction_train_generator(self, beta, beta1):
        self.beta = beta
        self.beta1 = beta1
        while True:

            x_shape = (self.batch_size, self.lb_size)
            y_shape = (self.batch_size, self.lf_size)
            x_batch = np.zeros(shape=x_shape, dtype=self.dtype)
            y_batch = np.zeros(shape=y_shape, dtype=self.dtype)

            while len(self.buffer) < self.batch_size:
                time.sleep(1)

            for i in range(self.batch_size):
                x_batch[i] = self.buffer[0][:self.lb_size]
                y_batch[i] = self.buffer[0][self.lb_size:]
                self.buffer.pop(0)

            prev_queue_size = len(self.buffer)

            yield (x_batch, y_batch)


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
