# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import modelrepo.chunk_pb2 as chunk__pb2


class FileServerStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.upload_model = channel.stream_unary(
                '/FileServer/upload_model',
                request_serializer=chunk__pb2.Chunk.SerializeToString,
                response_deserializer=chunk__pb2.Reply.FromString,
                )
        self.download_model = channel.unary_stream(
                '/FileServer/download_model',
                request_serializer=chunk__pb2.Request.SerializeToString,
                response_deserializer=chunk__pb2.Chunk.FromString,
                )


class FileServerServicer(object):
    """Missing associated documentation comment in .proto file"""

    def upload_model(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def download_model(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'upload_model': grpc.stream_unary_rpc_method_handler(
                    servicer.upload_model,
                    request_deserializer=chunk__pb2.Chunk.FromString,
                    response_serializer=chunk__pb2.Reply.SerializeToString,
            ),
            'download_model': grpc.unary_stream_rpc_method_handler(
                    servicer.download_model,
                    request_deserializer=chunk__pb2.Request.FromString,
                    response_serializer=chunk__pb2.Chunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FileServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileServer(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def upload_model(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/FileServer/upload_model',
            chunk__pb2.Chunk.SerializeToString,
            chunk__pb2.Reply.FromString,
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
        return grpc.experimental.unary_stream(request, target, '/FileServer/download_model',
            chunk__pb2.Request.SerializeToString,
            chunk__pb2.Chunk.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
