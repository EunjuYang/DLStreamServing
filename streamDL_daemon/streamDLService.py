"""
# cepService class
# dl-based cep service information is stored in the class
"""
import grpc
import streamDL_pb2


""" 
This Class contains cepService information.
It should be compatible with service type defined in protocol buffer
"""
class streamDLService:


    instance_info = []
    request_rate = 0

    def __init__(self, service_name, image_info):

        self.service_name = service_name
        self.image_info = image_info

    def get_num_instance(self):
        return len(self.instance_info)

    def get_request_rate(self):
        return self.request_rate

    def set_request_rate(self, request_rate):
        self.request_rate = request_rate

    def get_CEP_status(self):
        pass

    # I am not sure whether it is implemented here or not
    # If it's possible, it would be better to implement scale_up / down functions
    # in Kubernetes.
    def scale_up(self, resource_info):
        # TODO for gyusang
        pass

    def scale_down(self, resource_info):
        # TODO for gyusang
        pass


