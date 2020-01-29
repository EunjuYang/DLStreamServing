import sys, os, threading, json, time
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import KafkaError


class Consumer(threading.Thread):

    def __init__(self, topic, setting, index, buffer):
        super(Consumer, self).__init__()
        self.topic = topic
        self.consumer = KafkaConsumer(setting)
        self.consumer.subscribe([topic])
        self.index = index
        self.buffer = buffer

    def run(self):

        while True:
            msg = self.consumer.poll(1)
            if msg is None:
                continue
            elif msg.error():
                if msg.error.code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d \n" % (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    continue
            else:
                self.buffer[self.index].append(msg.value().decode('utf-8'))


class Producer:

    def __init__(self, topic, config):

        self.topic = topic
        self.producer = KafkaProducer(config)

    def produce(self, data):

        try:
            self.producer.produce(self.topic, data.encode('utf-8'))
            self.producer.poll(0)
        except:
            print("Buffer full, waiting for free space on the queue")
            self.producer.poll(5)  # wait time to free buffer
            self.producer.produce(self.topic, data.encode('utf-8'))

        self.producer.flush()


class StreamParser:

    def __init__(self):

        self.loop_back_win_size = int(os.environ['LOOP_BACK_WIN_SIZE'])
        self.input_shift_step = int(os.environ['INPUT_SHIFT_STEP'])
        self.look_forward_step = int(os.environ['LOOK_FORWARD_STEP'])
        self.look_forward_win_size = int(os.environ['LOOK_FORWARD_WIN_SIZE'])
        self.is_online_train = os.environ['IS_ONLINE_TRAIN']
        self.bootstrap_servers = os.environ['BOOTSTRAP_SERVERS']
        self.src = os.environ['SRC']
        self.dst = os.environ['DST']
        self.group_id = self.src + "_" + self.dst

        self.setting = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }

        self.config = {
            'bootstrap.servers': self.bootstrap_servers,
            'queue.buffering.max.messages': 1000000,
            'client.id': self.group_id,
            'default.topic.config': {'acks': 'all'}
        }

        self.producer = Producer(topic=self.dst,
                                 config=self.config)
        self.n_input = 1  # No multi-modal
        self.buffer = [[] for _ in range(self.n_input)]
        self.consumers = []
        for i in range(self.n_input):
            self.consumers.append(Consumer(topic=self.src,
                                           setting=self.setting,
                                           index=i,
                                           buffer=self.buffer))
            self.consumers[i].start()

    def run(self):

        if self.is_online_train:
            parser = self.train_parser
        elif self.n_input > 1:
            parser = self.multi_parser
        else:
            parser = self.simple_parser

        while True:
            data, is_produce = parser()
            if is_produce:
                self.producer.produce(data=data)
            else:
                time.sleep(0.01)

    def train_parser(self):
        data = ""
        small_delim = ","
        is_produce = False

        # Simple Parser does not consider multi-modality
        if len(self.buffer[0]) >= (self.loop_back_win_size + self.look_forward_step + self.look_forward_win_size):

            for j in range(self.loop_back_win_size):
                data += self.buffer[0][j] + small_delim

            for j in range(self.look_forward_win_size):
                data += self.buffer[0][self.loop_back_win_size + self.look_forward_step - 1 + j] + small_delim


            # remove one time step data from buffer
            for _ in range(self.input_shift_step):
                self.buffer[0].pop(0)

            is_produce = True
        return data, is_produce

    def multi_parser(self):
        data = ""
        small_delim = ","
        is_produce = False

        if all([(True if len(self.buffer[i]) > self.loop_back_win_size else False) for i in range(self.n_input)]):
            for i in range(self.n_input):
                for j in range(self.loop_back_win_size):
                    data += self.buffer[i][j] + small_delim

                # remove one time step data from buffer
                for _ in range(self.input_shift_step):
                    self.buffer[i].pop(0)

            is_produce = True
        return data, is_produce

    def simple_parser(self):

        data = ""
        small_delim = ","
        is_produce = False

        # Simple Parser does not consider multimodality
        if len(self.buffer[0]) >= self.loop_back_win_size:

            for j in range(self.loop_back_win_size):
                data += self.buffer[0][j] + small_delim

            # remove one time step data from buffer
            for _ in range(self.input_shift_step):
                self.buffer[0].pop(0)

            is_produce = True
        return data, is_produce


parser = StreamParser()
parser.run()