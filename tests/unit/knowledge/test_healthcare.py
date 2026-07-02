"""Unit tests for HealthcareKnowledge."""

from __future__ import annotations

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.healthcare import HealthcareKnowledge
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import (HealthcareEntity,
                                           HealthcareStandard, NodeType)


class TestHealthcareKnowledge:
    def _setup(self) -> tuple[GraphStore, NodeManager, HealthcareKnowledge]:
        store = GraphStore()
        nodes = NodeManager(store)
        hc = HealthcareKnowledge(store, nodes)
        return store, nodes, hc

    def test_register_standard(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_standard("HL7v2", HealthcareStandard.HL7_V2, version="2.5")
        assert node.name == "HL7v2"
        assert node.node_type == NodeType.HEALTHCARE_STANDARD

    def test_register_entity_device(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Analyzer X", HealthcareEntity.ANALYZER)
        assert node.name == "Analyzer X"
        assert node.node_type == NodeType.DEVICE

    def test_register_entity_workflow(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Lab Workflow", HealthcareEntity.HEALTHCARE_WORKFLOW)
        assert node.node_type == NodeType.WORKFLOW

    def test_create_mapping(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Recorder", HealthcareEntity.PATIENT_RECORD)
        mapping = hc.create_mapping(
            node.id,
            HealthcareStandard.FHIR,
            HealthcareEntity.PATIENT_RECORD,
            "FHIR-001",
            display_name="Patient Record Mapping",
        )
        assert mapping.code == "FHIR-001"
        assert mapping.standard == HealthcareStandard.FHIR

    def test_get_mapping(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        mapping = hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C001"
        )
        fetched = hc.get_mapping(mapping.id)
        assert fetched is not None
        assert fetched.code == "C001"

    def test_get_mapping_not_found(self) -> None:
        _, _, hc = self._setup()
        assert hc.get_mapping("nonexistent") is None

    def test_list_mappings(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C1"
        )
        hc.create_mapping(
            node.id, HealthcareStandard.HL7, HealthcareEntity.CLINICAL_DOCUMENT, "C2"
        )
        all_mappings = hc.list_mappings()
        assert len(all_mappings) == 2
        fhir = hc.list_mappings(standard=HealthcareStandard.FHIR)
        assert len(fhir) == 1

    def test_find_by_code(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        hc.create_mapping(
            node.id,
            HealthcareStandard.FHIR,
            HealthcareEntity.CLINICAL_DOCUMENT,
            "CODE1",
        )
        results = hc.find_by_code("CODE1")
        assert len(results) == 1

    def test_get_standards_usage(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C1"
        )
        hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C2"
        )
        hc.create_mapping(
            node.id, HealthcareStandard.HL7, HealthcareEntity.CLINICAL_DOCUMENT, "C3"
        )
        usage = hc.get_standards_usage()
        assert usage["fhir"] == 2
        assert usage["hl7"] == 1

    def test_get_healthcare_summary(self) -> None:
        _, _, hc = self._setup()
        hc.register_standard("FHIR R4", HealthcareStandard.FHIR)
        node = hc.register_entity("Analyzer", HealthcareEntity.ANALYZER)
        hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.ANALYZER, "A1"
        )
        summary = hc.get_healthcare_summary()
        assert summary["total_standards"] == 1
        assert summary["total_devices"] == 1
        assert summary["total_mappings"] == 1

    def test_delete_mapping(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        mapping = hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C1"
        )
        assert hc.delete_mapping(mapping.id) is True
        assert hc.get_mapping(mapping.id) is None

    def test_delete_mapping_not_found(self) -> None:
        _, _, hc = self._setup()
        assert hc.delete_mapping("nonexistent") is False

    def test_clear(self) -> None:
        _, _, hc = self._setup()
        node = hc.register_entity("Doc", HealthcareEntity.CLINICAL_DOCUMENT)
        hc.create_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C1"
        )
        hc.clear()
        assert len(hc.list_mappings()) == 0
