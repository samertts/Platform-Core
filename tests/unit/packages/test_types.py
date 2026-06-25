"""Unit tests for Package Manager core types."""

import pytest
from platform_core.packages import (
    PackageStatus,
    RepositoryType,
    InstallStatus,
    DependencyType,
    LifecycleMaturity,
    SignatureAlgorithm,
    PackageUUID,
    PackageIdentity,
    PackageDependencies,
    PackageCapabilities,
    PackageCompatibility,
    PackageLifecycle,
    PackageChecksum,
    PackageSignature,
    PackageManifest,
    RegistryEntry,
    RepositoryConfig,
    InstallRecord,
    Snapshot,
    Transaction,
)


class TestPackageTypes:
    def test_package_status(self) -> None:
        assert PackageStatus.ACTIVE.value == "active"
        assert PackageStatus.DEPRECATED.value == "deprecated"
        assert PackageStatus.YANKED.value == "yanked"

    def test_repository_type(self) -> None:
        assert RepositoryType.LOCAL.value == "local"
        assert RepositoryType.REMOTE.value == "remote"
        assert RepositoryType.GOVERNMENT.value == "government"

    def test_install_status(self) -> None:
        assert InstallStatus.PENDING.value == "pending"
        assert InstallStatus.COMPLETED.value == "completed"
        assert InstallStatus.FAILED.value == "failed"

    def test_dependency_type(self) -> None:
        assert DependencyType.REQUIRED.value == "required"
        assert DependencyType.OPTIONAL.value == "optional"

    def test_lifecycle_maturity(self) -> None:
        assert LifecycleMaturity.EXPERIMENTAL.value == "experimental"
        assert LifecycleMaturity.STABLE.value == "stable"

    def test_signature_algorithm(self) -> None:
        assert SignatureAlgorithm.SHA256.value == "sha256"
        assert SignatureAlgorithm.SHA512.value == "sha512"

    def test_package_uuid(self) -> None:
        uuid = PackageUUID()
        assert str(uuid) is not None

    def test_package_identity(self) -> None:
        identity = PackageIdentity(name="test", version="1.0.0")
        assert identity.name == "test"
        assert identity.version == "1.0.0"

    def test_package_dependencies(self) -> None:
        deps = PackageDependencies(
            required=[{"name": "dep1", "version": ">=1.0.0"}],
            optional=[{"name": "dep2", "version": ">=2.0.0"}],
        )
        assert len(deps.required) == 1
        assert len(deps.optional) == 1

    def test_package_capabilities(self) -> None:
        caps = PackageCapabilities(
            provides=["auth", "logging"],
            requires=["event_bus"],
        )
        assert "auth" in caps.provides
        assert "event_bus" in caps.requires

    def test_package_compatibility(self) -> None:
        compat = PackageCompatibility()
        assert compat.platform_core == ">=1.0.0"

    def test_package_manifest(self) -> None:
        manifest = PackageManifest()
        manifest.package.name = "test"
        manifest.package.version = "1.0.0"
        assert manifest.package.name == "test"

    def test_registry_entry(self) -> None:
        entry = RegistryEntry(name="test", version="1.0.0")
        assert entry.name == "test"
        assert entry.status == PackageStatus.ACTIVE

    def test_repository_config(self) -> None:
        config = RepositoryConfig(name="local", type=RepositoryType.LOCAL)
        assert config.name == "local"
        assert config.enabled is True

    def test_install_record(self) -> None:
        record = InstallRecord(package_name="test", package_version="1.0.0")
        assert record.package_name == "test"
        assert record.status == InstallStatus.PENDING

    def test_snapshot(self) -> None:
        snapshot = Snapshot(description="test snapshot")
        assert snapshot.description == "test snapshot"

    def test_transaction(self) -> None:
        transaction = Transaction()
        assert transaction.status == "pending"
