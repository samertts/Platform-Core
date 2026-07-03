"""Graph Query Engine - Implements graph traversal and analysis queries.

Supports dependency analysis, impact analysis, circular dependency detection,
shortest path, reachability, and more.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (
    Edge,
    Node,
    NodeType,
    QueryResult,
    QueryType,
)


class QueryEngine:
    """Graph query engine supporting 12+ query types."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def dependency_analysis(self, node_id: str, max_depth: int = 10) -> QueryResult:
        visited: set[str] = set()
        result_nodes: list[Node] = []
        result_edges: list[Edge] = []
        queue: deque[tuple[str, int]] = deque([(node_id, 0)])
        while queue:
            current_id, depth = queue.popleft()
            if current_id in visited or depth > max_depth:
                continue
            visited.add(current_id)
            node = self._store.get_node_optional(current_id)
            if node:
                result_nodes.append(node)
            for edge in self._store.get_outgoing_edges(current_id):
                if edge.target_id not in visited:
                    result_edges.append(edge)
                    queue.append((edge.target_id, depth + 1))
        return QueryResult(
            query_type=QueryType.DEPENDENCY_ANALYSIS,
            nodes=result_nodes,
            edges=result_edges,
            metadata={"source_node": node_id, "max_depth": max_depth},
        )

    def impact_analysis(self, node_id: str, max_depth: int = 10) -> QueryResult:
        visited: set[str] = set()
        result_nodes: list[Node] = []
        result_edges: list[Edge] = []
        queue: deque[tuple[str, int]] = deque([(node_id, 0)])
        while queue:
            current_id, depth = queue.popleft()
            if current_id in visited or depth > max_depth:
                continue
            visited.add(current_id)
            node = self._store.get_node_optional(current_id)
            if node:
                result_nodes.append(node)
            for edge in self._store.get_incoming_edges(current_id):
                if edge.source_id not in visited:
                    result_edges.append(edge)
                    queue.append((edge.source_id, depth + 1))
        return QueryResult(
            query_type=QueryType.IMPACT_ANALYSIS,
            nodes=result_nodes,
            edges=result_edges,
            metadata={"source_node": node_id, "max_depth": max_depth},
        )

    def circular_dependency(self, node_type: NodeType | None = None) -> QueryResult:
        cycles: list[list[str]] = []
        nodes = self._store.get_all_nodes()
        if node_type is not None:
            nodes = [n for n in nodes if n.node_type == node_type]

        def dfs(node_id: str, path: list[str], visited: set[str]) -> None:
            if node_id in path:
                cycle_start = path.index(node_id)
                cycles.append(path[cycle_start:] + [node_id])
                return
            if node_id in visited:
                return
            path.append(node_id)
            for edge in self._store.get_outgoing_edges(node_id):
                dfs(edge.target_id, path, visited)
            path.pop()
            visited.add(node_id)

        visited: set[str] = set()
        for node in nodes:
            if node.id not in visited:
                dfs(node.id, [], visited)

        cycle_node_ids = set()
        for cycle in cycles:
            cycle_node_ids.update(cycle)
        result_nodes = [n for n in self._store.get_all_nodes() if n.id in cycle_node_ids]
        return QueryResult(
            query_type=QueryType.CIRCULAR_DEPENDENCY,
            nodes=result_nodes,
            paths=cycles,
            metadata={"cycle_count": len(cycles)},
        )

    def shortest_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 20,
    ) -> QueryResult:
        if source_id == target_id:
            return QueryResult(
                query_type=QueryType.SHORTEST_PATH,
                paths=[[source_id]],
                metadata={"found": True},
            )
        visited: dict[str, str | None] = {source_id: None}
        queue: deque[str] = deque([source_id])
        depth = 0
        while queue and depth < max_depth:
            level_size = len(queue)
            for _ in range(level_size):
                current = queue.popleft()
                for edge in self._store.get_outgoing_edges(current):
                    if edge.target_id not in visited:
                        visited[edge.target_id] = current
                        if edge.target_id == target_id:
                            path = [target_id]
                            node: str | None = current
                            while node is not None:
                                path.append(node)
                                node = visited[node]
                            path.reverse()
                            result_nodes = []
                            for nid in path:
                                n = self._store.get_node_optional(nid)
                                if n:
                                    result_nodes.append(n)
                            return QueryResult(
                                query_type=QueryType.SHORTEST_PATH,
                                nodes=result_nodes,
                                paths=[path],
                                metadata={"found": True, "length": len(path) - 1},
                            )
                        queue.append(edge.target_id)
            depth += 1
        return QueryResult(
            query_type=QueryType.SHORTEST_PATH,
            paths=[],
            metadata={"found": False},
        )

    def reachability(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 20,
    ) -> QueryResult:
        result = self.shortest_path(source_id, target_id, max_depth)
        result.query_type = QueryType.REACHABILITY
        result.metadata["reachable"] = result.metadata.pop("found", False)
        return result

    def architecture_navigation(
        self,
        node_id: str,
        depth: int = 3,
    ) -> QueryResult:
        visited: set[str] = set()
        result_nodes: list[Node] = []
        result_edges: list[Edge] = []
        queue: deque[tuple[str, int]] = deque([(node_id, 0)])
        while queue:
            current_id, d = queue.popleft()
            if current_id in visited or d > depth:
                continue
            visited.add(current_id)
            node = self._store.get_node_optional(current_id)
            if node:
                result_nodes.append(node)
            for edge in self._store.get_outgoing_edges(current_id):
                if edge.target_id not in visited:
                    result_edges.append(edge)
                    queue.append((edge.target_id, d + 1))
            for edge in self._store.get_incoming_edges(current_id):
                if edge.source_id not in visited:
                    result_edges.append(edge)
                    queue.append((edge.source_id, d + 1))
        return QueryResult(
            query_type=QueryType.ARCHITECTURE_NAVIGATION,
            nodes=result_nodes,
            edges=result_edges,
            metadata={"center_node": node_id, "depth": depth},
        )

    def risk_propagation(
        self,
        node_id: str,
        max_depth: int = 5,
    ) -> QueryResult:
        return self.impact_analysis(node_id, max_depth)

    def repository_health(self) -> QueryResult:
        nodes = self._store.get_nodes_by_type(NodeType.REPOSITORY)
        return QueryResult(
            query_type=QueryType.REPOSITORY_HEALTH,
            nodes=nodes,
            metadata={"repository_count": len(nodes)},
        )

    def execute_query(
        self,
        query_type: QueryType,
        node_id: str = "",
        **kwargs: Any,
    ) -> QueryResult:
        start = time.monotonic()
        if query_type == QueryType.DEPENDENCY_ANALYSIS:
            result = self.dependency_analysis(node_id, **kwargs)
        elif query_type == QueryType.IMPACT_ANALYSIS:
            result = self.impact_analysis(node_id, **kwargs)
        elif query_type == QueryType.CIRCULAR_DEPENDENCY:
            result = self.circular_dependency(**kwargs)
        elif query_type == QueryType.SHORTEST_PATH:
            result = self.shortest_path(node_id, kwargs.get("target_id", ""), **kwargs)
        elif query_type == QueryType.REACHABILITY:
            result = self.reachability(node_id, kwargs.get("target_id", ""), **kwargs)
        elif query_type == QueryType.ARCHITECTURE_NAVIGATION:
            result = self.architecture_navigation(node_id, **kwargs)
        elif query_type == QueryType.RISK_PROPAGATION:
            result = self.risk_propagation(node_id, **kwargs)
        elif query_type == QueryType.REPOSITORY_HEALTH:
            result = self.repository_health()
        else:
            result = QueryResult(query_type=query_type, metadata={"error": "unsupported"})
        elapsed = (time.monotonic() - start) * 1000
        result.execution_time_ms = round(elapsed, 3)
        return result
