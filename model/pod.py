from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Pod:
    name: str
    ready: str
    status: str
    restarts: str
    age: str

    def __str__(self):
        return f"{self.name} ---- {self.ready} ---- {self.status} ---- {self.restarts} ---- {self.age}"
