import os
from concurrent import futures
import grpc
import time
from modelrepo import chunk_pb2_grpc, chunk_pb2
from modelrepo.model import Manager

CHUNK_SIZE = 1024 * 1024  # 1MB


def get_file_chunks(filename, model_name=None, loss=0):

    with open(filename, 'rb') as f:
        yield chunk_pb2.Chunk(name=model_name, loss=loss)
        while True:
            piece = f.read(CHUNK_SIZE);
            if len(piece) == 0:
                return
            yield chunk_pb2.Chunk(name=model_name, buffer=piece, loss=loss)


def save_chunks_to_file(chunks, filename=None):

    chunk = next(chunks)
    if chunk.name is not u'':
        filename = chunk.name
    print("# File is saved in %s" % filename)

    with open(filename, 'wb') as f:
        f.write(chunk.buffer)
        for chunk in chunks:
            f.write(chunk.buffer)

    return filename

class Client:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload_model(self, file_path, model_name, loss):
        """
        client library to upload model file
        :param file_path: file path to upload
        :param model_name: name of model
        :return:
        """
        chunks_generator = get_file_chunks(file_path, model_name, loss)
        response = self.stub.upload_model(chunks_generator)
        assert response.length == os.path.getsize(file_path)

    def download_model(self, model_name, download_path, loss):
        """
        client library to download model file
        :param model_name: name of model which client wants to download
        :param download_path: file path to save the file
        :return:
        """
        response = self.stub.download_model(chunk_pb2.Request(name=model_name, loss=loss))
        if response == None:
            return False
        self.save_chunks_to_file(response, download_path)
        return True

    def save_chunks_to_file(self, chunks, filename=None):

        with open(filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)
        return filename

    def get_model_info(self, model_name):

        response = self.stub.get_model_info(chunk_pb2.Request(name=model_name))
        return response



class ModelServer(chunk_pb2_grpc.FileServerServicer):

    def __init__(self, max_workers=20, repo_path="/tmp/"):

        class Servicer(chunk_pb2_grpc.FileServerServicer):

            def __init__(self, manager):
                super(Servicer, self).__init__()
                self.manager = manager

            def upload_model(self, request_iterator, context):
                filename = self._save_file(request_iterator)
                return chunk_pb2.Reply(length=os.path.getsize(filename))

            def download_model(self, request, context):
                model_name = request.name
                model = self.manager.get(model_name)
                if model is None:
                    return chunk_pb2.Reply(None)
                if request.loss < model.loss:
                    # No return model.
                    return chunk_pb2.Reply(None)
                return get_file_chunks(model.model_file, model_name)

            def get_model_info(self, request, context):
                model_name = request.name
                model = self.manager.get(model_name)

                # Model Name Error
                if model is None:
                    return chunk_pb2.ModelInfo(status=False, message="[Error] No model matching with the requested name")

                return chunk_pb2.ModelInfo(name=model_name,
                                           update_time=model.get_last_update(),
                                           loss=model.get_loss(),
                                           status=True)



            def _save_file(self, chunks):

                chunk = next(chunks)
                if chunk.name is not u'':
                    model_name = chunk.name
                    model_loss = chunk.loss
                else:
                    return None

                file_path = self.manager.update_model(model_name=model_name, loss=model_loss, chunks=chunks)
                return file_path

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        self.manager = Manager(dir_prefix=repo_path)
        chunk_pb2_grpc.add_FileServerServicer_to_server(Servicer(self.manager), self.server)

    def start(self, port):
        self.server.add_insecure_port('[::]:%d'%port)
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)

