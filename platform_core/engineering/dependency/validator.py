from platform_core.engineering.dependency.graph import DependencyGraph


class DependencyValidator:
    def __init__(self, graph: DependencyGraph):

        self.graph = graph

    def validate(self):

        for capability in self.graph.capabilities():
            for dependency in self.graph.dependencies_of(capability):
                if not self.graph.exists(dependency):
                    raise RuntimeError(f"Unknown capability: {dependency}")

        return True
