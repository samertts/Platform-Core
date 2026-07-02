"""Unit tests for NodeManager."""

from __future__ import annotations

import pytest

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import LifecycleStage, NodeStatus, NodeType


class TestNodeManager:
    def _make_manager(self) -> NodeManager:
        return NodeManager(GraphStore())

    def test_create_node(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.SERVICE, "auth-service")
        assert node.name == "auth-service"
        assert node.node_type == NodeType.SERVICE

    def test_get_node(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.MODULE, "core")
        fetched = mgr.get_node(node.id)
        assert fetched.name == "core"

    def test_update_node(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.MODULE, "old-name")
        updated = mgr.update_node(node.id, name="new-name")
        assert updated.name == "new-name"

    def test_update_node_status(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.MODULE, "m")
        updated = mgr.update_node(node.id, status=NodeStatus.DEPRECATED)
        assert updated.status == NodeStatus.DEPRECATED

    def test_delete_node(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.MODULE, "del")
        assert mgr.delete_node(node.id) is True
        assert mgr.count() == 0

    def test_list_nodes_by_type(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1")
        mgr.create_node(NodeType.SERVICE, "s1")
        modules = mgr.list_nodes(node_type=NodeType.MODULE)
        assert len(modules) == 1
        assert modules[0].name == "m1"

    def test_list_nodes_by_status(self) -> None:
        mgr = self._make_manager()
        n1 = mgr.create_node(NodeType.MODULE, "a")
        n2 = mgr.create_node(NodeType.MODULE, "b")
        mgr.update_node(n1.id, status=NodeStatus.INACTIVE)
        inactive = mgr.list_nodes(status=NodeStatus.INACTIVE)
        assert len(inactive) == 1

    def test_list_nodes_by_owner(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1", owner="alice")
        mgr.create_node(NodeType.MODULE, "m2", owner="bob")
        alice_nodes = mgr.list_nodes(owner="alice")
        assert len(alice_nodes) == 1

    def test_list_nodes_by_tag(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1", tags=["critical"])
        mgr.create_node(NodeType.MODULE, "m2", tags=["optional"])
        critical = mgr.list_nodes(tag="critical")
        assert len(critical) == 1

    def test_list_nodes_by_label(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1", labels=["core"])
        mgr.create_node(NodeType.MODULE, "m2", labels=["util"])
        core = mgr.list_nodes(label="core")
        assert len(core) == 1

    def test_search_nodes(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.SERVICE, "payment-service")
        mgr.create_node(NodeType.SERVICE, "auth-service")
        results = mgr.search_nodes("payment")
        assert len(results) == 1
        assert results[0].name == "payment-service"

    def test_transition_lifecycle(self) -> None:
        mgr = self._make_manager()
        node = mgr.create_node(NodeType.MODULE, "m")
        updated = mgr.transition_lifecycle(node.id, LifecycleStage.PRODUCTION)
        assert updated.lifecycle == LifecycleStage.PRODUCTION

    def test_get_by_name(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "core")
        mgr.create_node(NodeType.SERVICE, "core")
        results = mgr.get_by_name("core")
        assert len(results) == 2
        modules_only = mgr.get_by_name("core", node_type=NodeType.MODULE)
        assert len(modules_only) == 1

    def test_get_by_owner(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1", owner="alice")
        mgr.create_node(NodeType.MODULE, "m2", owner="alice")
        mgr.create_node(NodeType.MODULE, "m3", owner="bob")
        alice = mgr.get_by_owner("alice")
        assert len(alice) == 2

    def test_clear(self) -> None:
        mgr = self._make_manager()
        mgr.create_node(NodeType.MODULE, "m1")
        mgr.create_node(NodeType.MODULE, "m2")
        mgr.clear()
        assert mgr.count() == 0
