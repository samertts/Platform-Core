"""Healthcare Knowledge - Manages healthcare-specific entities and standards.

Supports HL7, FHIR, LOINC, SNOMED CT, ICD, ASTM, DICOM, IHE,
and other healthcare standards and entities.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import (
    HealthcareEntity,
    HealthcareMapping,
    HealthcareStandard,
    LifecycleStage,
    Node,
    NodeType,
)


class HealthcareKnowledge:
    """Manages healthcare-specific knowledge in the graph."""

    def __init__(self, store: GraphStore, node_manager: NodeManager) -> None:
        self._store = store
        self._node_manager = node_manager
        self._mappings: dict[str, HealthcareMapping] = {}
        self._lock = threading.RLock()

    def register_standard(
        self,
        name: str,
        standard: HealthcareStandard,
        version: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Node:
        return self._node_manager.create_node(
            node_type=NodeType.HEALTHCARE_STANDARD,
            name=name,
            version=version,
            metadata={"standard_type": standard.value, **(metadata or {})},
            labels=["healthcare", "standard", standard.value],
            lifecycle=LifecycleStage.PRODUCTION,
        )

    def register_entity(
        self,
        name: str,
        entity_type: HealthcareEntity,
        metadata: dict[str, Any] | None = None,
    ) -> Node:
        return self._node_manager.create_node(
            node_type=(
                NodeType.DEVICE
                if entity_type
                in (
                    HealthcareEntity.LABORATORY_EQUIPMENT,
                    HealthcareEntity.ANALYZER,
                    HealthcareEntity.MEDICAL_DEVICE,
                )
                else (
                    NodeType.WORKFLOW
                    if entity_type == HealthcareEntity.HEALTHCARE_WORKFLOW
                    else NodeType.MODULE
                )
            ),
            name=name,
            metadata={"healthcare_entity": entity_type.value, **(metadata or {})},
            labels=["healthcare", entity_type.value],
            lifecycle=LifecycleStage.PRODUCTION,
        )

    def create_mapping(
        self,
        node_id: str,
        standard: HealthcareStandard,
        entity_type: HealthcareEntity,
        code: str,
        display_name: str = "",
        version: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> HealthcareMapping:
        mapping = HealthcareMapping(
            node_id=node_id,
            standard=standard,
            entity_type=entity_type,
            code=code,
            display_name=display_name,
            version=version,
            metadata=metadata or {},
        )
        with self._lock:
            self._mappings[mapping.id] = mapping
        return mapping

    def get_mapping(self, mapping_id: str) -> HealthcareMapping | None:
        with self._lock:
            return self._mappings.get(mapping_id)

    def list_mappings(
        self,
        node_id: str | None = None,
        standard: HealthcareStandard | None = None,
        entity_type: HealthcareEntity | None = None,
    ) -> list[HealthcareMapping]:
        with self._lock:
            results = list(self._mappings.values())
        if node_id is not None:
            results = [m for m in results if m.node_id == node_id]
        if standard is not None:
            results = [m for m in results if m.standard == standard]
        if entity_type is not None:
            results = [m for m in results if m.entity_type == entity_type]
        return results

    def find_by_code(
        self,
        code: str,
        standard: HealthcareStandard | None = None,
    ) -> list[HealthcareMapping]:
        with self._lock:
            results = [m for m in self._mappings.values() if m.code == code]
        if standard is not None:
            results = [m for m in results if m.standard == standard]
        return results

    def get_standards_usage(self) -> dict[str, int]:
        with self._lock:
            counts: dict[str, int] = {}
            for m in self._mappings.values():
                key = m.standard.value
                counts[key] = counts.get(key, 0) + 1
            return counts

    def get_healthcare_summary(self) -> dict[str, Any]:
        standards = self._store.get_nodes_by_type(NodeType.HEALTHCARE_STANDARD)
        devices = self._store.get_nodes_by_type(NodeType.DEVICE)
        with self._lock:
            mapping_count = len(self._mappings)
            standards_used = len(set(m.standard.value for m in self._mappings.values()))
        return {
            "total_standards": len(standards),
            "total_devices": len(devices),
            "total_mappings": mapping_count,
            "unique_standards_used": standards_used,
            "usage_by_standard": self.get_standards_usage(),
        }

    def delete_mapping(self, mapping_id: str) -> bool:
        with self._lock:
            return self._mappings.pop(mapping_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._mappings.clear()
