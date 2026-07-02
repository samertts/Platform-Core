from collections import defaultdict


class DependencyGraph:
    def __init__(self):

        self.nodes = {}

        self.edges = defaultdict(set)

    def add_node(self, node):

        self.nodes[node.id] = node

        self.edges[node.id]

    def add_dependency(
        self,
        capability,
        dependency,
    ):

        self.edges[capability].add(dependency)

    def dependencies_of(
        self,
        capability,
    ):

        return sorted(self.edges.get(capability, []))

    def exists(
        self,
        capability,
    ):

        return capability in self.nodes

    def capabilities(self):

        return sorted(self.nodes.keys())
