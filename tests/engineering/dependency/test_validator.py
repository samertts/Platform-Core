import pytest

from platform_core.engineering.dependency.graph import DependencyGraph
from platform_core.engineering.dependency.models import DependencyNode
from platform_core.engineering.dependency.validator import DependencyValidator


def test_validation():

    graph = DependencyGraph()

    graph.add_node(DependencyNode(id="runtime"))

    graph.add_node(DependencyNode(id="registry"))

    graph.add_dependency(
        "runtime",
        "registry",
    )

    validator = DependencyValidator(graph)

    assert validator.validate()


def test_missing_dependency():

    graph = DependencyGraph()

    graph.add_node(DependencyNode(id="runtime"))

    graph.add_dependency(
        "runtime",
        "missing",
    )

    validator = DependencyValidator(graph)

    with pytest.raises(RuntimeError):
        validator.validate()
