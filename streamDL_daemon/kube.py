from kubernetes import client, config, watch
from os import path
import yaml

CLUSTER_IP = '10.96.0.1'
class kubecommunicator():

    # dictionary for streamDLServices
    services = {}

    def __init__(self):
        config.load_kube_config()
        self._k8s_v1 = client.CoreV1Api()
        self._k8s_beta = client.ExtensionsV1beta1Api()
        self._k8s_rbac = client.RbacAuthorizationV1beta1Api()
        configuration = client.Configuration()

    def list_pods(self):
        print("Listing pods with their IPs:")
        ret = self.v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" %
                  (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    def list_nodes(self):
        nodes = self.v1.list_node()
        print("Name\tRole\tStatus")
        for i in nodes.items:
            print("%s\t%s\t%s" %
                  (i.metadata.name, i.kind, i.metadata.name))

    def create_container(self):
        container = client.V1Container(
            name="busybox"
        )
        container.image="busybox"
        container.args=["sleep","3600"]
        return container

    def create_pod_with_container(self,cont):
        pod = client.V1Pod()
        pod.metadata = client.V1ObjectMeta(name="busybox")
        spec= client.V1PodSpec()
        spec.containers=[cont]
        pod.spec = spec
        res = v1.create_namespaced_pod(namespace="default", body=pod)
        print("Create pod with container. status='%s'" % str(res.status))

    def create_deployment(self,yaml_name):
        with open(path.join(path.dirname(__file__), yaml_name)) as f:
            dep = yaml.safe_load(f)
            k8s_beta = client.ExtensionsV1beta1Api()
            resp = k8s_beta.create_namespaced_deployment(
                body=dep, namespace="default")
            print("Deployment created. status='%s'" % str(resp.status))

    ## On  Prog
    def make_job(self):
        job = client.V1Job()
        job.metadata = client.V1ObjectMeta()
        job.metadata.name = "process"
        job.spec = client.V1JobSpec(template=client.V1PodTemplate)
        job.spec.template = client.V1PodTemplate()
        job.spec.template.spec = client.V1PodTemplateSpec()
        job.spec.template.spec.restart_policy = "Never"
        job.spec.template.spec.containers = [
            self.create_container()
        ]
        return job

    def delete_deployment(api_instance):
        # Delete deployment
        api_response = api_instance.delete_namespaced_deployment(
            name=DEPLOYMENT_NAME,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        print("Deployment deleted. status='%s'" % str(api_response.status))


if __name__ == '__main__':
    kc = kubecommunicator()
    kc.list_pods()
    kc.list_nodes()
    kc.make_job()
    con1 = kc.create_container()
    kc.create_pod_with_container(con1)
    kc.create_deployment("dummy.yaml")
