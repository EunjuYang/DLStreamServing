from kubernetes import client, config


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    body = client.V1Service(
                api_version= "v1",
                kind= "Service",
                metadata=client.V1ObjectMeta(
                  name= "ws-service",
                  labels={"app": "ws"}
                  ),
                spec=client.V1ServiceSpec(
                  ports=[client.V1ServicePort(
                      port=8080,
                      target_port=8080
                      )],
                  selector={"app": "ws"},
                  type="NodePort"
                    )
                )
    k8s_core_v1 = client.CoreV1Api()
    resp = k8s_core_v1.create_namespaced_service(
        body=body, namespace="default")
    print("Service created. status='%s'" % resp.metadata.name)


if __name__ == '__main__':
    main()