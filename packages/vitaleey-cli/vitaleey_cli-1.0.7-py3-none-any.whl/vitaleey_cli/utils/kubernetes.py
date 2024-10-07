import logging
import subprocess
import tempfile
import os

logger = logging.getLogger(__name__)


class KubernetesException(Exception):
    pass


class Kubernetes:
    """
    Kubernetes class to interact with kubectl commands
    """

    def __init__(self, digitalocean_cluster_name):

        if not digitalocean_cluster_name:
            raise KubernetesException("DigitalOcean cluster name is required")

        kubeconfig_file = self.get_digitalocean_cluster_kubeconfig(
            digitalocean_cluster_name
        )
        print(kubeconfig_file)
        if not kubeconfig_file:
            raise KubernetesException("kubeconfig file is required")
        self._kubeconfig_file = kubeconfig_file

    def run(self, command: list, kubectl=True):
        cli_command = "kubectl"
        if kubectl:
            if command[0] != cli_command:
                command = [cli_command] + command
            command.append(f"--kubeconfig={self._kubeconfig_file}")

            logger.debug(f"Running kubectl command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise KubernetesException(f"Executing {command}:\n\n{result.stderr}")

        logger.debug(result.stdout)
        return result.stdout

    def get_digitalocean_cluster_kubeconfig(self, digitalocean_cluster_name):
        logger.info(f"Get digitalocean cluster kubeconfig")

        file = os.path.join(tempfile.gettempdir(), "kubeconfig")
        result = self.run(
            [
                "doctl",
                "kubernetes",
                "cluster",
                "kubeconfig",
                "show",
                digitalocean_cluster_name,
            ],
            kubectl=False,
        )

        with open(file, "w") as f:
            f.write(result)
        return file

    def get_nodes(self):
        logger.info(f"Get kubernetes nodes")
        return self.run(["get", "nodes"])

    def set_registry(self, registry, docker_username, docker_password, docker_email):
        logger.info(f"Set docker registry for kubernetes")
        return self.run(
            [
                "create",
                "secret",
                "docker-registry",
                "regcred",
                f"--docker-server={registry}",
                f"--docker-username={docker_username}",
                f"--docker-password={docker_password}",
                f"--docker-email={docker_email}",
            ]
        )
