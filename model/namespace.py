from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Namespace:
    name: str
    description: str
    kubeconfig: str

    def __str__(self):
        return f"{self.name} ({self.description})"
