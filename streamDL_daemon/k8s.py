from kubernetes import client, config
from pprint import pprint
import json

class k8s:

    def __init__(self):

        self.config = config.load_kube_config()
        self.v1 = client.AppsV1Api()
        self.k8s_core = client.CoreV1Api()

    def deploy_with_svc(self, name, img, label, portnum, replicas, namespace):

        # create deployment
        self.deploy(name, img, label, portnum, replicas, namespace)

        # create service
        svc_body = client.V1Service(
            api_version="v1",
            kind= "Service",
            metadata=client.V1ObjectMeta(
                name=name,
                labels={"app": name}
            ),
            spec=client.V1ServiceSpec(
                ports=[client.V1ServicePort(
                    port=portnum,
                    target_port=portnum
                )],
                selector={"app": label},
                type="ClusterIP"
            )
        )

        resp = self.k8s_core.create_namespaced_service(
            body=svc_body,
            namespace=namespace
        )
        print("Service created. status = %s" % resp.metadata.name)
        print(resp.metadata)



    def _create_deployment_object(self, name, img, label, deployment_name, portnum, replicas, env_dict):

        # envionment variable list
        env_list = []
        for key in env_dict.keys():
            env_list.append(client.V1EnvVar(name=key, value=env_dict[key]))

        # Pod template container
        container = client.V1Container(
            name=name,
            image=img,
            env=env_list,
            ports=[client.V1ContainerPort(container_port=portnum)]
        )

        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": label}),
            spec=client.V1PodSpec(containers=[container])
        )

        # Create the specification of deployment
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            template=template,
            selector={'matchLabels':{'app': label}}
        )

        # Instantiate the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec
        )

        return deployment

    def deploy(self, name, img, label, portnum, replicas, namespace, env_dict):

        print("deploy is called")
        deployment = self._create_deployment_object(name, img, label, name, portnum, replicas, env_dict)
        api_repsponse = self._create_deployment(deployment, namespace)
        print(api_repsponse)

        return api_repsponse

    def _create_deployment(self, deployment, namespace):

        # Create deployment
        api_response = self.v1.create_namespaced_deployment(
            body=deployment,
            namespace=namespace
        )

        print(api_response)

    def update_deployment(self,  deployment, img, deployment_name, namespace):

        # Update container image
        deployment.spec.template.spec.container[0].image = img
        # Update the deployment
        api_response = self.v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment
        )

    def delete_deployment(self, deployment_name, namespace):

        # Delete deployment
        api_response = self.v1.delete_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5
            )
        )

    def get_svc_ep(self, name, namespace):
        """
        get the endpoint of service
        :param name: name of service
        :param namespace: namespace of the service
        :return:
        """
        pretty = 'pretty_example'  # str | If 'true', then the output is pretty printed. (optional)
        exact = True  # bool | Should the export be exact.  Exact export maintains cluster-specific fields like 'Namespace'. Deprecated. Planned for removal in 1.18. (optional)
        export = True  # bool | Should this value be exported.  Export strips fields that a user can not specify. Deprecated. Planned for removal in 1.18. (optional)
        api_response = self.k8s_core.read_namespaced_endpoints(name, namespace, pretty=pretty, exact=exact, export=export)
        ip = (api_response.subsets[0].addresses[0].ip)
        portnum = (api_response.subsets[0].ports[0].port)

        return "%s:%s" %(ip, portnum)

if __name__ == '__main__':

    k8s_ = k8s()
    name = "sp-01"
    img = "dlstream/stream-parser:v01"
    label = name
    portnum = 59990
    replicas = 1
    namespace = "dlstream"
    env_dict = {"LOOP_BACK_WIN_SIZE":"3",
                "INPUT_SHIFT_STEP":"1",
                "SRC":"0",
                "DST":"cep0",
                "LOOK_FORWARD_STEP":"1",
                "LOOK_FORWARD_WIN_SIZE":"1",
                "IS_ONLINE_TRAIN":"True",
                "BOOTSTRAP_SERVERS":"143.248.146.115:9092,143.248.146.116:9092,143.248.146.117:9092"}
    k8s_.deploy(name, img, label, portnum, replicas, namespace, env_dict)
