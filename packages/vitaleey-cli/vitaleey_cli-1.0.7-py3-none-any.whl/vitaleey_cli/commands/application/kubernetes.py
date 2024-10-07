import os
import click

from vitaleey_cli.utils.kubernetes import Kubernetes, KubernetesException


@click.group(help="Kubernetes helper commands")
def group():
    pass


@group.command()
@click.argument("cluster_name")
def set_registry(cluster_name):
    """
    Set the kubernetes registry
    """

    try:
        kubernetes = Kubernetes(
            cluster_name or os.environ.get("KUBERNETES_CLUSTER_NAME")
        )
        kubernetes.set_registry(
            os.environ.get("DOCKER_REGISTRY"),
            os.environ.get("DOCKER_USERNAME"),
            os.environ.get("DOCKER_PASSWORD"),
            os.environ.get("DOCKER_EMAIL"),
        )
    except KubernetesException as e:
        raise click.UsageError(str(e))


@group.command("nodes")
@click.argument("cluster_name")
def get_nodes(cluster_name):
    """
    Get the kubernetes nodes
    """

    try:
        kubernetes = Kubernetes(
            cluster_name or os.environ.get("KUBERNETES_CLUSTER_NAME")
        )
        nodes = kubernetes.get_nodes()
        click.echo(nodes)
    except KubernetesException as e:
        raise click.UsageError(str(e))
