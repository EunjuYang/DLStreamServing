from streamDLbroker import streamDLbroker
from concurrent import futures
import streamDL_pb2
import streamDL_pb2_grpc
import grpc
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

if __name__ == '__main__':
    max_workers = 3
    streamDLbroker_ = streamDLbroker()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    streamDL_pb2_grpc.add_streamDLbrokerServicer_to_server(streamDLbroker_, server)
    server.add_insecure_port('[::]:50091')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)