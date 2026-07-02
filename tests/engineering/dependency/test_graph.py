from platform_core.engineering.dependency.graph import DependencyGraph
from platform_core.engineering.dependency.models import DependencyNode


def test_graph():

    graph = DependencyGraph()

    graph.add_node(DependencyNode(id="runtime"))

    graph.add_node(DependencyNode(id="registry"))

    graph.add_dependency(
        "runtime",
        "registry",
    )

    assert graph.exists("runtime")

    assert graph.dependencies_of("runtime") == ["registry"]
