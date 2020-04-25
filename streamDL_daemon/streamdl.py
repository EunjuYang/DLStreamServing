from concurrent import futures
from streamDLbroker import streamDLbroker
import streamDL_pb2_grpc
import time
import logging
import grpc
import signal

_ONE_DAY_IN_SECONDS = 60 * 60 * 24



class streamDL():
    """
    This class work as streamDL_daemon
    This is only for daemon (running and launching server)
    Actual action of streamDL broker is defined in the `streamDLbroker` class
    """

    def __init__(self, log_file=None):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("streamDLBroker")
        self.log_file = log_file

        if log_file:
            self.log_handler = logging.FileHandler(self.log_file)
            self.logger.addHandler(self.log_handler)

        self.__stop = False

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.streamDLbroker = streamDLbroker()

    def stop(self, signum, frame):
        self.__stop = True
        self.logger.info("Receive Signal {0}".format(signum))
        self.logger.info("Stop streamDLBroker")

    def run(self):

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        streamDL_pb2_grpc.add_streamDLbrokerServicer_to_server(self.streamDLbroker, self.server)
        self.server.add_insecure_port('[::]:50091')
        self.server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.server.stop(0)


