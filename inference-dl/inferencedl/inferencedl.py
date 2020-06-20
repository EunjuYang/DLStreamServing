import os, time, datetime
import tensorflow as tf
from onlinedl.utils import ModelManager
from pymongo import MongoClient
import numpy as np

class InferenceDL:

    def __init__(self, model_name, repo_addr, result_addr):
        """
        :param model_name: Inference model is managed by its name.
        :param model_repo_addr: User should give model repo addr
        :param result_addr: User should give mongodb address as IP:Port
        :return: InferenceDL object
        """

        self.model_manager = ModelManager(repo_addr, model_name)
        self.model_path = "/tmp/inference/%s_init"%(model_name)


        self.model_manager.download_model(self.model_path)
        self.save_path = "/tmp/inference/%s" % (model_name)

        self.model_filename = self.model_path.split('/')[-1]
        self.model = tf.keras.models.load_model(self.model_path)
        self.batch_input_shape = (-1,) + self.model.input_shape[1:]

        # mongodb
        self.client = MongoClient('mongodb://%s'%(result_addr))
        self.db = self.client['inference'] # create database named as a model name
        self.collection = self.db[model_name]
        self.collection.remove({})
        self.model_name = model_name
        #TODO: for saved pred-value
        self.saved_value = None
        self.saved_loss_list = [2.0]
        self.max_count = 3
        self.cursor_saved_loss_list = 1
        


    # Below consume-function implement feedforward and send results to database (mongodb)
    def consume(self, data, id):
        result = self.model.predict(data.reshape(self.batch_input_shape), batch_size=data.shape[0])
        result = result.reshape((data.shape[0],))
        data = data[:,-1]

        # Do not use encode and decode
        for i in np.unique(id):
            post = {}
            post['amiid'] = i.item()
            _result_tmp = result[np.where(id.reshape((id.shape[0],))==i)].tolist()
            post['pred'] = _result_tmp # shape is (batch,)
            _true_tmp = data[np.where(id.reshape((id.shape[0],))==i)].tolist()
            post['true'] = _true_tmp # shape is (batch,)
            post['timestamp'] = datetime.datetime.now()
            if self.saved_value:
                _result_tmp_for_loss = [self.saved_value] + _result_tmp
                _tmp_loss = np.sqrt(np.mean((np.asarray(_result_tmp_for_loss[:-1]) - np.asarray(_true_tmp))**2)).item()
            else:
                if _result_tmp[:-1] and _true_tmp[1:]:
                    _tmp_loss = np.sqrt(np.mean((np.asarray(_result_tmp[:-1]) - np.asarray(_true_tmp[1:]))**2)).item()
                else:
                    _tmp_loss = None
            self.saved_value = _result_tmp[-1]
            if not _tmp_loss:
                _tmp_loss = self.saved_loss_list[self.cursor_saved_loss_list - 1]
            post['loss'] = _tmp_loss

            if len(self.saved_loss_list)==self.max_count:
                self.saved_loss_list[self.cursor_saved_loss_list]=_tmp_loss
                self.cursor_saved_loss_list += 1
            else:
                self.saved_loss_list.append(_tmp_loss)
                self.cursor_saved_loss_list += 1
            if self.cursor_saved_loss_list == self.max_count:
                self.cursor_saved_loss_list = 0
            post['average_loss'] = np.mean(np.asarray(self.saved_loss_list)).item()
            
            self.collection.insert_one(post)
        #TODO: change this to support multi-ami
        
        if self.model_manager.download_model(self.save_path):
            tmp_model = tf.keras.models.load_model(self.save_path)

            _sum = 0.0
            for w1, w2 in zip(tmp_model.get_weights(), self.model.get_weights()):
                _sum += np.sum((w1 - w2) ** 2)

            if _sum > 0.0:
                self.model = tmp_model
                post = {}
                post['updated_at_inferencedl'] = datetime.datetime.now()
                self.collection.insert_one(post)