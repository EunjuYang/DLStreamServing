from streamDL_daemon import streamDL_pb2, streamDL_pb2_grpc
import grpc
import time

CHUNK_SIZE = 1024 * 1024 # 1 MB

class Client:

    def __init__(self, address):

        channel = grpc.insecure_channel(address)
        self.stub = streamDL_pb2_grpc.streamDLbrokerStub(channel)

    def set_deploy_model(self, model_file, model_name, ami_list, input_format, is_online_train, online_param):

        deploy_generator = self._deploy_generator(model_file, model_name, ami_list, input_format, is_online_train, online_param)
        response = self.stub.set_deploy_model(deploy_generator)
        print(response.message)
        return

    def get_ami_list(self):

        ami_list = self.stub.get_ami_list(streamDL_pb2.null())
        print(ami_list.ami_id)

    def _deploy_generator(self, model_file, model_name, ami_list, input_format, is_online_train, online_param):

        input_fmt = streamDL_pb2.InputFmt(
            look_back_win_size=input_format['look_back_win_size'],
            input_shift_step=input_format['input_shift_step'],
            look_forward_step=input_format['look_forward_step'],
            look_forward_win_size=input_format['look_forward_win_size']
        )
        online_parameter = streamDL_pb2.onlineParam(
            online_method=online_param['online_method'],
            batch_size=online_param['batch_size'],
            memory_method=online_param['memory_method'],
            episodic_mem_size=online_param['episodic_mem_size'],
            is_schedule=online_param['is_schedule']
        )
        amis = streamDL_pb2.AMIList()
        for ami in ami_list:
            amis.ami_id.append(ami)

        with open(model_file, 'rb') as f:

            while True:
                piece = f.read(CHUNK_SIZE)
                if len(piece) == 0:
                    return

                yield streamDL_pb2.Model(name=model_name,
                                           amis=amis,
                                           buffer=piece,
                                           is_online_train=is_online_train,
                                           input_fmt=input_fmt,
                                           update_time=str(time.time()),
                                           create_time=str(time.time()),
                                           UUID=model_name,
                                           online_param=online_parameter)



if __name__ == '__main__':
    client = Client('127.0.0.1:50091')
    #client.get_ami_list()

    model_file = "/tmp/test_model.h5"
    model_name = "hellotest"
    ami_list = ["ami0", "ami1"]
    input_format = {}
    online_param = {}
    input_format['look_back_win_size'] = 3
    input_format['input_shift_step'] = 1
    input_format['look_forward_step'] = 1
    input_format['look_forward_win_size'] = 1
    online_param['online_method'] = "cont"
    online_param['batch_size'] = 32
    online_param['memory_method'] = "cossim"
    online_param['episodic_mem_size'] = 100
    online_param['is_schedule'] = True
    is_online_train = True


    client.set_deploy_model(model_file, model_name, ami_list, input_format, is_online_train, online_param)
