#!/usr/bin/python
import streamDL_pb2
import time

class streamDL:

    def __init__(self, name, input_fmt, is_online_train, update_time, create_time, UUID, online_param, amis, loss=0.0):

        self.name = name
        self.input_fmt= input_fmt
        self.is_online_train = is_online_train
        self.update_time = str(time.time())
        self.create_time = str(time.time())
        self.UUID = UUID
        self.online_param = online_param
        self.sp_name_list = []
        self.online_train_name_list = []
        self.amis = amis
        self.inferencedl_name_list = []
        self.loss = loss

    def set_sp_info(self, sp_name_list):
        self.sp_name_list = sp_name_list

    def set_update_time(self, update_time):
        self.update_time = update_time

    def set_loss(self, loss):
        self.loss = loss

    def get_model_instance(self):

        ami_list = streamDL_pb2.AMIList()
        for ami in self.amis:
            ami_list.ami_id.append(ami)

        if self.is_online_train:
            input_fmt = streamDL_pb2.InputFmt(
                look_back_win_size=self.input_fmt['look_back_win_size'],
                input_shift_step=self.input_fmt['input_shift_step'],
                look_forward_step=self.input_fmt['look_forward_step'],
                look_forward_win_size=self.input_fmt['look_forward_win_size']
            )
            online_parameter = streamDL_pb2.onlineParam(
                online_method=self.online_param['online_method'],
                batch_size=self.online_param['batch_size'],
                memory_method=self.online_param['memory_method'],
                episodic_mem_size=self.online_param['episodic_mem_size'],
                is_schedule=self.online_param['is_schedule']
            )
        else:
            input_fmt = streamDL_pb2.InputFmt(
                look_back_win_size=self.input_fmt['look_back_win_size'],
                input_shift_step=self.input_fmt['input_shift_step'],
                look_forward_step = None,
                look_forward_win_size = None
            )
            online_parameter = streamDL_pb2.onlineParam(
                online_method=None,
                batch_size=None,
                memory_method=None,
                episodic_mem_size=None,
                is_schedule=None
            )

        return streamDL_pb2.Model(name=self.name,
                                  amis=ami_list,
                                  is_online_train=self.is_online_train,
                                  create_time=self.create_time,
                                  input_fmt=input_fmt,
                                  online_param=online_parameter,
                                  UUID=self.UUID,
                                  update_time=self.update_time,
                                  loss=self.loss)

    def set_online_train_info(self, online_train_list):
        self.online_train_name_list = online_train_list

    def set_inferencedl_info(self, inferencedl_list):
        self.inferencedl_name_list = inferencedl_list

    def get_inferencedl_info(self):
        return self.inferencedl_name_list

    def get_sp_info(self):
        return self.sp_name_list

    def get_online_train_info(self):
        return self.online_train_name_list

    def __str__(self):

        return self.name


