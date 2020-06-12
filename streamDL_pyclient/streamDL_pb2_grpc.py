# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import streamDL_pyclient.streamDL_pb2 as streamDL__pb2


class streamDLbrokerStub(object):
    """streamDLbroker
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.set_deploy_model = channel.stream_unary(
                '/streamDL.streamDLbroker/set_deploy_model',
                request_serializer=streamDL__pb2.Model.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )
        self.get_deployed_model = channel.unary_unary(
                '/streamDL.streamDLbroker/get_deployed_model',
                request_serializer=streamDL__pb2.null.SerializeToString,
                response_deserializer=streamDL__pb2.ModelList.FromString,
                )
        self.is_deployed_model = channel.unary_unary(
                '/streamDL.streamDLbroker/is_deployed_model',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )
        self.get_ami_list = channel.unary_unary(
                '/streamDL.streamDLbroker/get_ami_list',
                request_serializer=streamDL__pb2.null.SerializeToString,
                response_deserializer=streamDL__pb2.AMIList.FromString,
                )
        self.restart_online_train = channel.unary_unary(
                '/streamDL.streamDLbroker/restart_online_train',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )
        self.stop_online_train = channel.unary_unary(
                '/streamDL.streamDLbroker/stop_online_train',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )
        self.stop_deployment = channel.unary_unary(
                '/streamDL.streamDLbroker/stop_deployment',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )
        self.get_deployed_model_with_name = channel.unary_unary(
                '/streamDL.streamDLbroker/get_deployed_model_with_name',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Model.FromString,
                )
        self.download_model = channel.unary_unary(
                '/streamDL.streamDLbroker/download_model',
                request_serializer=streamDL__pb2.ModelName.SerializeToString,
                response_deserializer=streamDL__pb2.Reply.FromString,
                )


class streamDLbrokerServicer(object):
    """streamDLbroker
    """

    def set_deploy_model(self, request_iterator, context):
        """deploy model
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_deployed_model(self, request, context):
        """return deployed model list
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def is_deployed_model(self, request, context):
        """check duplicate check
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_ami_list(self, request, context):
        """return ami lists available in the system
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def restart_online_train(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stop_online_train(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stop_deployment(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_deployed_model_with_name(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def download_model(self, request, context):
        """Only used for debugging
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_streamDLbrokerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'set_deploy_model': grpc.stream_unary_rpc_method_handler(
                    servicer.set_deploy_model,
                    request_deserializer=streamDL__pb2.Model.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
            'get_deployed_model': grpc.unary_unary_rpc_method_handler(
                    servicer.get_deployed_model,
                    request_deserializer=streamDL__pb2.null.FromString,
                    response_serializer=streamDL__pb2.ModelList.SerializeToString,
            ),
            'is_deployed_model': grpc.unary_unary_rpc_method_handler(
                    servicer.is_deployed_model,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
            'get_ami_list': grpc.unary_unary_rpc_method_handler(
                    servicer.get_ami_list,
                    request_deserializer=streamDL__pb2.null.FromString,
                    response_serializer=streamDL__pb2.AMIList.SerializeToString,
            ),
            'restart_online_train': grpc.unary_unary_rpc_method_handler(
                    servicer.restart_online_train,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
            'stop_online_train': grpc.unary_unary_rpc_method_handler(
                    servicer.stop_online_train,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
            'stop_deployment': grpc.unary_unary_rpc_method_handler(
                    servicer.stop_deployment,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
            'get_deployed_model_with_name': grpc.unary_unary_rpc_method_handler(
                    servicer.get_deployed_model_with_name,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Model.SerializeToString,
            ),
            'download_model': grpc.unary_unary_rpc_method_handler(
                    servicer.download_model,
                    request_deserializer=streamDL__pb2.ModelName.FromString,
                    response_serializer=streamDL__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'streamDL.streamDLbroker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class streamDLbroker(object):
    """streamDLbroker
    """

    @staticmethod
    def set_deploy_model(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/streamDL.streamDLbroker/set_deploy_model',
            streamDL__pb2.Model.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_deployed_model(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/get_deployed_model',
            streamDL__pb2.null.SerializeToString,
            streamDL__pb2.ModelList.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def is_deployed_model(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/is_deployed_model',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_ami_list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/get_ami_list',
            streamDL__pb2.null.SerializeToString,
            streamDL__pb2.AMIList.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def restart_online_train(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/restart_online_train',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stop_online_train(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/stop_online_train',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stop_deployment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/stop_deployment',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_deployed_model_with_name(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/get_deployed_model_with_name',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Model.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def download_model(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streamDL.streamDLbroker/download_model',
            streamDL__pb2.ModelName.SerializeToString,
            streamDL__pb2.Reply.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
