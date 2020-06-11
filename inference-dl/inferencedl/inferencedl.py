import os, time
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
        self.model_manager.model_name = "%s_current" %(model_name)
        self.save_path = "tmp/inference/%s_current" % (model_name)

        self.model_filename = self.model_path.split('/')[-1]
        self.model = tf.keras.models.load_model(self.model_path)
        self.batch_input_shape = (-1,) + self.model.input_shape[1:]

        # mongodb
        self.client = MongoClient('mongodb://%s'%(result_addr))
        self.db = self.client['inference'] # create database named as a model name
        self.collection = self.db[model_name]
        self.collection.remove({})
        self.model_name = model_name

        self.transition_decision = 0.1

    # Below consume-function implement feedforward and send results to database (mongodb)
    def consume(self, data, id):
        result = self.model.predict(data.reshape(self.batch_input_shape), batch_size=data.shape[0])
        result = result.reshape((data.shape[0],))
        data = data[:,-1]
        # Do not use encode and decode
        for i in np.unique(id):
            post = {}
            post['amiid'] = i.item()
            post['pred'] = result[np.where(id.reshape((id.shape[0],))==i)].tolist() # shape is (batch,)
            post['true'] = data[np.where(id.reshape((id.shape[0],))==i)].tolist() # shape is (batch,)
            post['timestamp'] = time.time() # time.time() is global UTC value
            self.collection.insert_one(post)

        if self.model_manager.download_model(self.save_path):
            tmp_model = tf.keras.models.load_model(self.save_path)

            _sum = 0.0
            for w1, w2 in zip(tmp_model.get_weights(), self.model.get_weights()):
                _sum += np.sum((w1 - w2) ** 2)

            if _sum > self.transition_decision:
                self.model = tmp_model
                post['updated_at'] = time.time()
                self.collection.insert_one(post)