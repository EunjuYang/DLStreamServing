import time

class Model:

    def __init__(self, model_name, file_path):

        self.model_name = model_name
        self.file_path = file_path
        self.num_push = 1
        self.last_update = time.time()

    def __str__(self):
        return self.model_name

class Manager:

    def __init__(self):

        self.model_table = {}
        pass