import streamDL_pb2_grpc
import streamDL_pb2

class streamDLbroker(streamDL_pb2_grpc.streamDLbrokerServicer):
    """
    dlCEPbroker
    """

    def __init__(self):
        super(streamDLbroker, self).__init__()

    def deploy_model(self, request, context):
        print("deploy model is called")
        return

    def is_deployed_model(self, request, context):
        print("is_deployed_model is called")
        return streamDL_pb2.Reply(status=False)

    def set_input(self, request, context):
        print("set input is called")
        return

    def get_stream_list(self, request, context):
        print("get_stream_list is called")
        return



