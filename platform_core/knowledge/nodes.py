"""Node Manager - Manages knowledge graph nodes.

Handles node CRUD, lifecycle transitions, and node queries.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (LifecycleStage, Node, NodeStatus,
                                           NodeType)


class NodeManager:
    """Manages knowledge graph nodes."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def create_node(
        self,
        node_type: NodeType,
        name: str,
        version: str = "1.0.0",
        owner: str = "",
        labels: list[str] | None = None,
        tags: list[str] | None = None,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        lifecycle: LifecycleStage = LifecycleStage.DEVELOPMENT,
    ) -> Node:
        node = Node(
            node_type=node_type,
            name=name,
            version=version,
            owner=owner,
            labels=labels or [],
            tags=tags or [],
            capabilities=capabilities or [],
            metadata=metadata or {},
            lifecycle=lifecycle,
        )
        return self._store.add_node(node)

    def get_node(self, node_id: str) -> Node:
        return self._store.get_node(node_id)

    def update_node(
        self,
        node_id: str,
        name: str | None = None,
        version: str | None = None,
        status: NodeStatus | None = None,
        lifecycle: LifecycleStage | None = None,
        owner: str | None = None,
        metadata: dict[str, Any] | None = None,
        labels: list[str] | None = None,
        tags: list[str] | None = None,
        capabilities: list[str] | None = None,
    ) -> Node:
        node = self._store.get_node(node_id)
        if name is not None:
            node.name = name
        if version is not None:
            node.version = version
        if status is not None:
            node.status = status
        if lifecycle is not None:
            node.lifecycle = lifecycle
        if owner is not None:
            node.owner = owner
        if metadata is not None:
            node.metadata.update(metadata)
        if labels is not None:
            node.labels = labels
        if tags is not None:
            node.tags = tags
        if capabilities is not None:
            node.capabilities = capabilities
        node.updated_at = datetime.now(timezone.utc)
        return self._store.update_node(node)

    def delete_node(self, node_id: str) -> bool:
        return self._store.delete_node(node_id)

    def list_nodes(
        self,
        node_type: NodeType | None = None,
        status: NodeStatus | None = None,
        lifecycle: LifecycleStage | None = None,
        owner: str | None = None,
        tag: str | None = None,
        label: str | None = None,
    ) -> list[Node]:
        nodes = self._store.get_all_nodes()
        if node_type is not None:
            nodes = [n for n in nodes if n.node_type == node_type]
        if status is not None:
            nodes = [n for n in nodes if n.status == status]
        if lifecycle is not None:
            nodes = [n for n in nodes if n.lifecycle == lifecycle]
        if owner is not None:
            nodes = [n for n in nodes if n.owner == owner]
        if tag is not None:
            nodes = [n for n in nodes if tag in n.tags]
        if label is not None:
            nodes = [n for n in nodes if label in n.labels]
        return nodes

    def search_nodes(self, query: str) -> list[Node]:
        query_lower = query.lower()
        return [
            n
            for n in self._store.get_all_nodes()
            if query_lower in n.name.lower()
            or query_lower in n.id.lower()
            or any(query_lower in t.lower() for t in n.tags)
            or any(query_lower in l.lower() for l in n.labels)
            or any(query_lower in str(v).lower() for v in n.metadata.values())
        ]

    def transition_lifecycle(self, node_id: str, new_stage: LifecycleStage) -> Node:
        node = self._store.get_node(node_id)
        node.lifecycle = new_stage
        node.updated_at = datetime.now(timezone.utc)
        return self._store.update_node(node)

    def count(self) -> int:
        return self._store.node_count()

    def get_by_name(self, name: str, node_type: NodeType | None = None) -> list[Node]:
        nodes = self._store.get_all_nodes()
        result = [n for n in nodes if n.name == name]
        if node_type is not None:
            result = [n for n in result if n.node_type == node_type]
        return result

    def get_by_owner(self, owner: str) -> list[Node]:
        return [n for n in self._store.get_all_nodes() if n.owner == owner]

    def clear(self) -> None:
        for node in self._store.get_all_nodes():
            self._store.delete_node(node.id)
