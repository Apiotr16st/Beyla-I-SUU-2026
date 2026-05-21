import os
import time
from typing import Any, Dict, List

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from mcp.server.fastmcp import FastMCP


DEFAULT_NAMESPACE = os.getenv("DEFAULT_NAMESPACE", "app")

mcp = FastMCP("k8s-controller", host="0.0.0.0", port=8000)

_k8s_loaded = False


def ensure_k8s() -> tuple[client.CoreV1Api, client.AppsV1Api]:
    global _k8s_loaded

    if not _k8s_loaded:
        try:
            config.load_incluster_config()
        except ConfigException:
            config.load_kube_config()
        _k8s_loaded = True

    return client.CoreV1Api(), client.AppsV1Api()


def deployment_summary(item: Any, namespace: str) -> Dict[str, Any]:
    return {
        "name": item.metadata.name,
        "namespace": namespace,
        "replicas": item.spec.replicas or 0,
        "ready_replicas": item.status.ready_replicas or 0,
        "available_replicas": item.status.available_replicas or 0,
    }


@mcp.tool()
def list_deployments(namespace: str = DEFAULT_NAMESPACE) -> List[Dict[str, Any]]:
    """List deployments in the selected namespace."""
    _, apps = ensure_k8s()
    items = apps.list_namespaced_deployment(namespace=namespace).items
    return [deployment_summary(item, namespace) for item in items]


@mcp.tool()
def list_pods(namespace: str = DEFAULT_NAMESPACE) -> List[Dict[str, str]]:
    """List pods in the selected namespace."""
    core, _ = ensure_k8s()
    pods = core.list_namespaced_pod(namespace=namespace).items
    return [
        {
            "name": pod.metadata.name,
            "phase": pod.status.phase or "Unknown",
            "pod_ip": pod.status.pod_ip or "",
        }
        for pod in pods
    ]


@mcp.tool()
def scale_deployment(name: str, replicas: int, namespace: str = DEFAULT_NAMESPACE) -> Dict[str, Any]:
    """Scale a deployment to the requested number of replicas."""
    _, apps = ensure_k8s()
    apps.patch_namespaced_deployment_scale(
        name=name,
        namespace=namespace,
        body={"spec": {"replicas": replicas}},
    )
    return {
        "status": "ok",
        "action": "scale_deployment",
        "name": name,
        "namespace": namespace,
        "replicas": replicas,
    }


@mcp.tool()
def restart_deployment(name: str, namespace: str = DEFAULT_NAMESPACE) -> Dict[str, Any]:
    """Trigger a rolling restart of a deployment."""
    _, apps = ensure_k8s()
    restarted_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    apps.patch_namespaced_deployment(
        name=name,
        namespace=namespace,
        body={
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": restarted_at,
                        }
                    }
                }
            }
        },
    )
    return {
        "status": "ok",
        "action": "restart_deployment",
        "name": name,
        "namespace": namespace,
        "restarted_at": restarted_at,
    }


@mcp.tool()
def set_loadgenerator(users: int, rate: int, namespace: str = DEFAULT_NAMESPACE) -> Dict[str, Any]:
    """Update the loadgenerator deployment by setting USERS and RATE."""
    _, apps = ensure_k8s()
    deployment = apps.read_namespaced_deployment(name="loadgenerator", namespace=namespace)
    container = deployment.spec.template.spec.containers[0]

    env = container.env or []
    env_by_name = {item.name: item for item in env}

    if "USERS" in env_by_name:
        env_by_name["USERS"].value = str(users)
    else:
        env.append(client.V1EnvVar(name="USERS", value=str(users)))

    if "RATE" in env_by_name:
        env_by_name["RATE"].value = str(rate)
    else:
        env.append(client.V1EnvVar(name="RATE", value=str(rate)))

    apps.patch_namespaced_deployment(
        name="loadgenerator",
        namespace=namespace,
        body={
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": container.name,
                                "env": [{"name": item.name, "value": item.value} for item in env],
                            }
                        ]
                    }
                }
            }
        },
    )

    return {
        "status": "ok",
        "action": "set_loadgenerator",
        "namespace": namespace,
        "users": users,
        "rate": rate,
    }


if __name__ == "__main__":
    mcp.run(transport="sse")
