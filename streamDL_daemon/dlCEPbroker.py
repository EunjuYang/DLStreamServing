import dlCEPbroker_pb2
import dlCEPbroker_pb2_grpc

class dlCEPbroker(dlCEPbroker_pb2_grpc.dlCEPbrokerServicer):
    """
    dlCEPbroker
    """

    # dictionary for streamDLServices
    services = {}

    def deploy(self, request, context):
        print(request.name)
        print(request.image_name)
        # TODO #
        return dlCEPbroker_pb2.return_msg(status=True)

    def get_cep_status(self, request, context):
        print(request.name)
        print(request.image_name)
        # TODO #
        return dlCEPbroker_pb2.return_msg(status=True)

    def get_stream_list(self, request, context):
        pass

