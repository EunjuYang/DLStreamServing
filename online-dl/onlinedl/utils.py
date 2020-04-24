import os
import grpc
from onlinedl import chunk_pb2, chunk_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

class ModelManager:

    def __init__(self, address, model_name):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)
        self.model_name = model_name

    def upload_model(self, file_path):
        """
        client library to upload model file
        :param file_path: file path to upload
        :param model_name: name of model
        :return:
        """
        chunks_generator = self.get_file_chunks(file_path, self.model_name)
        response = self.stub.upload_model(chunks_generator)
        assert response.length == os.path.getsize(file_path)

    def download_model(self, download_path):
        """
        client library to download model file
        :param download_path: file path to save the file
        :return:
        """
        response = self.stub.download_model(chunk_pb2.Request(name=model_name))
        if response == None:
            print("[Error] No model name with %s" %self.model_name)
            return False
        self.save_chunks_to_file(response, download_path)
        return True

    def save_chunks_to_file(self, chunks, filename=None):
        with open(filename, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)
        return filename

    def get_file_chunks(self, filename, model_name=None):

        with open(filename, 'rb') as f:
            while True:
                piece = f.read(CHUNK_SIZE);
                if len(piece) == 0:
                    return
                yield chunk_pb2.Chunk(name=model_name, buffer=piece)



