import streamDL_pb2_grpc
import streamDL_pb2

class streamDLbroker(streamDL_pb2_grpc.streamDLbrokerServicer):
    """
    dlCEPbroker
    """

    def __init__(self):
        super(streamDLbroker, self).__init__()

    def deploy_model(self, request, context):
        pass

    def is_deployed_model(self, request, context):
        pass

    def set_input(self, request, context):
        pass

    def get_stream_list(self, request, context):
        pass



