import os, time
import tensorflow as tf
from onlinedl.utils import ModelManager
from pymongo import MongoClient

class InferenceDL:

    def __init__(self, model_name, repo_addr, result_addr):
        """
        :param model_name: Inference model is managed by its name.
        :param model_repo_addr: User should give model repo addr
        :param result_addr: User should give mongodb address as IP:Port
        :return: InferenceDL object
        """


        self.model_manager = ModelManager(repo_addr, model_name)
        self.model_path = "/tmp/inference/%s_init".format(model_name)

        # I didn't test model_manager yet. -Changha
        self.model_manager.download_model(self.model_path)

        self.model_filename = self.model_path.split('/')[-1]
        self.model = tf.keras.models.load_model(self.model_path)
        self.batch_input_shape = (-1,) + self.model.input_shape[1:]

        # mongodb
        self.client = MongoClient('mongodb://%s'.format(result_addr))
        self.db = self.client[model_name]
        self.model_name = model_name
        self.post_dict = {}
        self.post_dict[model_name] = None # key:result

    def consume(self, data):
        data = data.reshape(self.batch_input_shape)
        result = self.model.predict(data, batch_size=data.shape[0])
        self.post_dict[self.model_name] = result
        posts = self.db.posts





