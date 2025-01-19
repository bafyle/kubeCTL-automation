from dataclasses import dataclass


class QuickDeployment:
    def __init__(self, resource: str, description: str, local_machine_port: int, pod_port: int = None):
        self.resource = resource
        self.description = description
        self.local_machine_port = local_machine_port
        if pod_port is None:
            self.pod_port = self.local_machine_port
        else:
            self.pod_port = pod_port

    def __str__(self):
        return f"{self.resource} port: ({self.port})"
