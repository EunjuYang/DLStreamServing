import os
from concurrent import futures
import grpc
import time
from modelrepo import chunk_pb2, chunk_pb2_grpc
from modelrepo.model import Manager

CHUNK_SIZE = 1024 * 1024  # 1MB


def get_file_chunks(filename, out_name=None):

    with open(filename, 'rb') as f:
        yield chunk_pb2.Chunk(name=out_name)
        while True:
            piece = f.read(CHUNK_SIZE);
            if len(piece) == 0:
                return
            yield chunk_pb2.Chunk(buffer=piece)


def save_chunks_to_file(chunks, filename=None):

    chunk = next(chunks)
    if chunk.name is not u'':
        filename = chunk.name
    print("# File is saved in %s" % filename)

    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)

    return filename

class Client:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload(self, in_file_name, target_name=None):
        chunks_generator = get_file_chunks(in_file_name, target_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)

    def download(self, target_name, out_file_name):
        response = self.stub.download(chunk_pb2.Request(name=target_name))
        save_chunks_to_file(response, out_file_name)


class ModelServer(chunk_pb2_grpc.FileServerServicer):
    def __init__(self, max_workers=20):

        class Servicer(chunk_pb2_grpc.FileServerServicer):

            def __init__(self, manager):
                super(Servicer, self).__init__()
                self.manager = manager

            def upload(self, request_iterator, context):
                filename = save_chunks_to_file(request_iterator)
                return chunk_pb2.Reply(length=os.path.getsize(filename))

            def download(self, request, context):
                if request.name:
                    return get_file_chunks(request.name)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        self.manager = Manager()
        chunk_pb2_grpc.add_FileServerServicer_to_server(Servicer(self.manager), self.server)

    def start(self, port):
        self.server.add_insecure_port('[::]:%d'%port)
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)

