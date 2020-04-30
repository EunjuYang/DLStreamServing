import time

class Model:

    def __init__(self, model_name, model_file, extension=".h5"):
        """
        :param model_name: (string) model name
        :param param_file: (string) file path of param file
        :param model_json: (string) file path of model json file
        """

        self.model_name = model_name
        self.model_file = model_file
        self.num_push = 0
        self.last_update = time.time()

    def __str__(self):
        return self.model_name

    def flag_update(self):
        self.num_push += 1
        self.last_update = time.strftime('%c', time.localtime(time.time()))

class Manager:

    def __init__(self, dir_prefix):
        """
        :param dir_prefix: Manager repository directory prefix should be ended with "/"
        """

        self.model_table = {}
        self.dir_prefix = dir_prefix

    def create_new_model(self, model_name):
        """
        Create a new model
        :param model_name: model name
        :return: model instance
        """

        if model_name in self.model_table.keys():
            print("[Error] duplicate model is already saved in the repository")
            return None

        model_file = self.dir_prefix + model_name + ".h5"
        model = Model(model_name=model_name,
                      model_file=model_file)
        self.model_table[model_name] = model

        return model

    def get(self, model_name):

        if not (model_name in self.model_table.keys()):
            return None
        return self.model_table[model_name]

    def update_model(self, model_name, chunks):

        model = self.get(model_name)
        if model is None:
            model = self.create_new_model(model_name)
        if model is None:
            return None

        file_path = model.model_file
        with open(file_path, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)

            model.flag_update()

        return file_path

