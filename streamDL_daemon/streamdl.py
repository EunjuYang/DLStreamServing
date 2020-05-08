#!/usr/bin/python
import streamDL_pb2

class streamDL:

    def __init__(self, name, input_fmt, is_online_train, update_time, create_time, UUID, online_param, amis):

        self.name = name
        self.input_fmt= input_fmt
        self.is_online_train = is_online_train
        self.update_time = update_time
        self.create_time = create_time
        self.UUID = UUID
        self.online_param = online_param
        self.sp_name_list = []
        self.amis = amis

    def update_sp_info(self, sp_name_list):

        self.sp_name_list = sp_name_list

    def get_model_instance(self):

        ami_list = streamDL_pb2.AMIList()
        for ami in self.amis:
            ami_list.ami_id.append(ami)

        return streamDL_pb2.Model(name=self.name,
                               amis=ami_list,
                               is_online_train=self.is_online_train,
                               create_time=self.create_time)


