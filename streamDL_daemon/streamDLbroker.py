import streamDL_pb2_grpc
import streamDL_pb2
import os
from k8s import k8s
from pykafka import KafkaClient
from streamdl import streamDL
from modelrepo_client.utils import ModelRepoClient

class streamDLbroker(streamDL_pb2_grpc.streamDLbrokerServicer):
    """
    dlCEPbroker
    """

    def __init__(self, MODE="SYSDAEMON"):
        super(streamDLbroker, self).__init__()

        # KAFKA BROKER INFO
        self.KAFKA_BK = os.environ['KAFKA_BK']
        self.stream_prefix = os.environ['STREAM_PREFIX']
        self.k8s_ = k8s(MODE)
        self.kafka_client = KafkaClient(hosts=self.KAFKA_BK)

        self.ModelRepo = {}
        self.ModelRepo['name'] = "modelrepo"
        self.Namespace = "dlstream"
        self.ModelRepo['ep'] = self.k8s_.get_svc_ep(name=self.ModelRepo['name'],namespace=self.Namespace)

        self.Manager = {}
        self.modelrepo_client = ModelRepoClient(self.ModelRepo['ep'])
        self.name_spce = "dlstream"


    def _is_duplicate_model(self, name):
        """
        :param name:
        :return: True if it exist False otherwise
        """

        if name in self.Manager:
            return True
        else:
            return False


    def set_deploy_model(self, request, context):

        input_fmt = {}
        online_param = {}

        # save the model file and model info
        chunk = next(request)
        model_name = chunk.name
        amis = chunk.amis.ami_id
        is_online_train = chunk.is_online_train
        update_time = chunk.update_time
        create_time = chunk.create_time
        UUID = chunk.UUID
        input_fmt['look_back_win_size'] = chunk.input_fmt.look_back_win_size
        input_fmt['input_shift_step'] = chunk.input_fmt.input_shift_step

        if is_online_train:
            input_fmt['look_forward_step'] = chunk.input_fmt.look_forward_step
            input_fmt['look_forward_win_size'] = chunk.input_fmt.look_forward_win_size
            online_param['online_method'] = chunk.online_param.online_method
            online_param['batch_size'] = chunk.online_param.batch_size
            online_param['memory_method'] = chunk.online_param.memory_method
            online_param['episodic_mem_size'] = chunk.online_param.episodic_mem_size
            online_param['is_schedule'] = chunk.online_param.is_schedule


        if self._is_duplicate_model(model_name):
            reply = streamDL_pb2.Reply()
            reply.status = False
            reply.message = "Duplicate model name"
            return reply

        file_path = "/tmp/dlstream_%s" % model_name

        with open(file_path, 'wb') as f:
            f.write(chunk.buffer)
            for chunk in request:
                f.write(chunk.buffer)


        # create model instance
        dl_instance = streamDL(name=model_name,
                             input_fmt=input_fmt,
                             is_online_train=is_online_train,
                             update_time=update_time,
                             create_time=create_time,
                             UUID=UUID,
                             online_param=online_param,
                             amis=amis)

        self.Manager[model_name] = dl_instance

        # upload model file to modelrepo
        self.modelrepo_client.upload_model(model_name, file_path)

        # create stream parser instances
        num_amis = len(amis)
        sp_names = []
        # create stream parser instance for inference
        sp_infer_dst = "dlstream.sp.%s.infer" % model_name
        for ami in amis:
            name = "sp-%s-%s-infer" %(model_name, ami)
            sp_src = self.stream_prefix + ami
            self._create_stream_parser_instance(name=name,
                                                src=sp_src,
                                                dst=sp_infer_dst,
                                                is_online_train=False,
                                                input_format_dict=input_fmt)
            sp_names.append(name)

        # create stream parser instance for train
        if is_online_train:
            sp_train_dst = "dlstream.sp.%s.train" % model_name
            for ami in amis:
                name = "sp-%s-%s-train" % (model_name, ami)
                sp_src = self.stream_prefix + ami
                self._create_stream_parser_instance(name=name,
                                                    src=sp_src,
                                                    dst=sp_train_dst,
                                                    is_online_train=is_online_train,
                                                    input_format_dict=input_fmt)
                sp_names.append(name)

        # update sp_name information
        dl_instance.update_sp_info(sp_names)

        # create inference instance
        # TODO

        # create online trainer instance (if is_online_train is true)
        if is_online_train:
            name = "online-%s--train" % (model_name)
            cep_id = sp_train_dst
            self._create_online_trainer(name, online_param, cep_id, num_amis)

        # delete tmp model file
        os.remove(file_path)

        return streamDL_pb2.Reply(status=True)

    def get_deployed_model(self, request, context):

        model_list = streamDL_pb2.ModelList()
        for key in self.Manager.keys():
            model_list.model.append(self.Manager[key].get_model_instance())
        return model_list

    def is_deployed_model(self, request, context):
        return streamDL_pb2.Reply(status=False)

    def get_ami_list(self, request, context):
        ami_list = streamDL_pb2.AMIList()
        self.topics = self.kafka_client.topics
        for topic in self.topics.keys():
            if topic.startswith((self.stream_prefix.encode(),)):
                ami_list.ami_id.append(topic.decode())
        return ami_list

    def _create_stream_parser_instance(self, name, src, dst, is_online_train, input_format_dict):


        img = "dlstream/stream-parser:v01"
        label = name
        portnum = 59990
        replicas = 1
        namespace = "dlstream"
        env_dict = {"LOOP_BACK_WIN_SIZE" : str(input_format_dict['look_back_win_size']),
                    "INPUT_SHIFT_STEP" : str(input_format_dict['input_shift_step']),
                    "SRC":src,
                    "DST":dst,
                    "LOOK_FORWARD_STEP":str(input_format_dict['look_forward_step']),
                    "LOOK_FORWARD_WIN_SIZE":str(input_format_dict['look_forward_win_size']),
                    "IS_ONLINE_TRAIN": str(is_online_train),
                    "BOOTSTRAP_SERVERS": self.KAFKA_BK}

        self.k8s_.deploy(name, img, label, portnum, replicas, namespace, env_dict)

    def _create_online_trainer(self, name, online_param, cep_id, num_amis):

        img = "dlstream/onlinedl:v01"
        label = name
        portnum = 58990
        replicas = 1
        namespace = "dlstream"
        env_dict = {
            "MODEL_NAME": name,
            "ONLINE_METHOD": online_param['online_method'],
            "FRAMEWORK": "keras",
            "SAVEWEIGHT": "True",
            "MEM_METHOD": online_param["memory_method"],
            "NUM_AMI": str(num_amis),
            "EPISODIC_MEM_SIZE": "100",
            "IS_SCHEDULE": str(online_param["is_schedule"]),
            "MODEL_REPO_ADDR": self.ModelRepo['ep'],
            "CEP_ID": cep_id,
            "KAFKA_BK": self.KAFKA_BK,
            "BATCH_SIZE": str(online_param["batch_size"]),
            "DTYPE": "float32",
            "IS_ADAPTIVE": "False"
        }

        self.k8s_.deploy(name, img, label, portnum, replicas, namespace, env_dict)



