import os
import grpc
from modelrepo_client import chunk_pb2, chunk_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

class ModelRepoClient:

    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload_model(self, model_name, file_path):

        chunks_generator = self._get_file_chunks(file_path, model_name)
        response = self.stub.upload_model(chunks_generator)
        assert response.length == os.path.getsize(file_path)

    def download_model(self, download_path):
        """
        client library to download model file
        :param download_path: file path to save the file
        :return:
        """
        response = self.stub.download_model(chunk_pb2.Request(name=self.model_name))
        if response == None:
            print("[Error] No model name with %s" %self.model_name)
            return False
        self._save_chunks_to_file(response, download_path)
        return True

    def _save_chunks_to_file(self, chunks, filename=None):

        chunk = next(chunks)
        print("# File is saved in %s" % filename)

        with open(filename, 'wb') as f:
            f.write(chunk.buffer)
            for chunk in chunks:
                f.write(chunk.buffer)

        return filename

    def _get_file_chunks(self, filename, model_name, loss=-1):

        with open(filename, 'rb') as f:
            yield chunk_pb2.Chunk(name=model_name)
            while True:
                piece = f.read(CHUNK_SIZE);
                if len(piece) == 0:
                    return
                yield chunk_pb2.Chunk(name=model_name, buffer=piece, loss=loss)



