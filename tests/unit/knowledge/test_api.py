"""Unit tests for KnowledgeAPI."""

from __future__ import annotations

import pytest
from platform_core.knowledge.api import KnowledgeAPI
from platform_core.knowledge.engine import KnowledgeEngine
from platform_core.knowledge.types import (
    NodeNotFoundError,
    NodeType,
)


class TestKnowledgeAPI:
    def _make_api(self) -> KnowledgeAPI:
        return KnowledgeAPI(KnowledgeEngine())

    def test_create_node(self) -> None:
        api = self._make_api()
        result = api.create_node("module", "test-mod")
        assert result["status"] == "created"
        assert result["node"]["name"] == "test-mod"

    def test_get_node(self) -> None:
        api = self._make_api()
        created = api.create_node("module", "m1")
        node_id = created["node"]["id"]
        result = api.get_node(node_id)
        assert result["node"]["name"] == "m1"

    def test_get_node_not_found(self) -> None:
        api = self._make_api()
        with pytest.raises(NodeNotFoundError):
            api.get_node("nonexistent")

    def test_update_node(self) -> None:
        api = self._make_api()
        created = api.create_node("module", "old")
        node_id = created["node"]["id"]
        result = api.update_node(node_id, name="new")
        assert result["status"] == "updated"
        assert result["node"]["name"] == "new"

    def test_delete_node(self) -> None:
        api = self._make_api()
        created = api.create_node("module", "del")
        node_id = created["node"]["id"]
        result = api.delete_node(node_id)
        assert result["status"] == "deleted"

    def test_list_nodes(self) -> None:
        api = self._make_api()
        api.create_node("module", "m1")
        api.create_node("service", "s1")
        result = api.list_nodes(node_type="module")
        assert result["count"] == 1

    def test_search_nodes(self) -> None:
        api = self._make_api()
        api.create_node("service", "payment-svc")
        result = api.search_nodes("payment")
        assert result["count"] == 1

    def test_create_relationship(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        result = api.create_relationship(
            n1["node"]["id"], n2["node"]["id"], "depends_on"
        )
        assert result["status"] == "created"

    def test_get_relationship(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        created = api.create_relationship(
            n1["node"]["id"], n2["node"]["id"], "depends_on"
        )
        edge_id = created["edge"]["id"]
        result = api.get_relationship(edge_id)
        assert result["edge"]["source_id"] == n1["node"]["id"]

    def test_delete_relationship(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        created = api.create_relationship(
            n1["node"]["id"], n2["node"]["id"], "depends_on"
        )
        result = api.delete_relationship(created["edge"]["id"])
        assert result["status"] == "deleted"

    def test_list_relationships(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        api.create_relationship(n1["node"]["id"], n2["node"]["id"], "depends_on")
        result = api.list_relationships(source_id=n1["node"]["id"])
        assert result["count"] == 1

    def test_dependency_analysis(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        api.create_relationship(n1["node"]["id"], n2["node"]["id"], "depends_on")
        result = api.dependency_analysis(n1["node"]["id"])
        assert "nodes" in result
        assert "execution_time_ms" in result

    def test_impact_analysis(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "target")
        n2 = api.create_node("service", "svc")
        api.create_relationship(n2["node"]["id"], n1["node"]["id"], "depends_on")
        result = api.impact_analysis(n1["node"]["id"])
        assert "impact_level" in result
        assert "total_affected" in result

    def test_shortest_path(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "a")
        n2 = api.create_node("module", "b")
        api.create_relationship(n1["node"]["id"], n2["node"]["id"], "depends_on")
        result = api._engine._queries.shortest_path(n1["node"]["id"], n2["node"]["id"])
        assert result.metadata.get("found") is True

    def test_circular_dependencies(self) -> None:
        api = self._make_api()
        result = api.circular_dependencies()
        assert "cycles" in result
        assert "cycle_count" in result

    def test_architecture_navigation(self) -> None:
        api = self._make_api()
        n1 = api.create_node("module", "center")
        result = api.architecture_navigation(n1["node"]["id"])
        assert "nodes" in result

    def test_architecture_smells(self) -> None:
        api = self._make_api()
        api.create_node("service", "orphan")
        result = api.architecture_smells()
        assert "smells" in result
        assert result["count"] >= 1

    def test_architecture_recommendations(self) -> None:
        api = self._make_api()
        api.create_node("service", "orphan")
        result = api.architecture_recommendations()
        assert "recommendations" in result

    def test_ai_reason(self) -> None:
        api = self._make_api()
        result = api.ai_reason("overview", "architecture")
        assert "answer" in result
        assert "confidence" in result

    def test_create_snapshot(self) -> None:
        api = self._make_api()
        api.create_node("module", "m1")
        result = api.create_snapshot("test")
        assert "snapshot_id" in result
        assert result["node_count"] == 1

    def test_get_entity_history(self) -> None:
        api = self._make_api()
        created = api.create_node("module", "m1")
        result = api.get_entity_history(created["node"]["id"])
        assert result["count"] == 1

    def test_healthcare_summary(self) -> None:
        api = self._make_api()
        result = api.healthcare_summary()
        assert "total_standards" in result

    def test_graph_summary(self) -> None:
        api = self._make_api()
        api.create_node("module", "m1")
        result = api.graph_summary()
        assert result["node_count"] == 1

    def test_health_check(self) -> None:
        api = self._make_api()
        result = api.health_check()
        assert result["status"] == "healthy"
        assert "node_count" in result
