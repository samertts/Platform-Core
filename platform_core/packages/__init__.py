"""Platform Package Manager - Core types and constants."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class PackageStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    YANKED = "yanked"
    ARCHIVED = "archived"


class RepositoryType(Enum):
    LOCAL = "local"
    REMOTE = "remote"
    MIRROR = "mirror"
    OFFLINE = "offline"
    GOVERNMENT = "government"


class InstallStatus(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    VERIFYING = "verifying"
    INSTALLING = "installing"
    MIGRATING = "migrating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class DependencyType(Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    PEER = "peer"
    DEV = "dev"


class LifecycleMaturity(Enum):
    EXPERIMENTAL = "experimental"
    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"
    MATURE = "mature"
    LEGACY = "legacy"


class SignatureAlgorithm(Enum):
    SHA256 = "sha256"
    SHA512 = "sha512"
    RSA_SHA256 = "rsa-sha256"
    RSA_SHA512 = "rsa-sha512"
    ED25519 = "ed25519"


@dataclass(frozen=True)
class PackageUUID:
    id: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.id)


@dataclass
class PackageIdentity:
    uuid: PackageUUID = field(default_factory=PackageUUID)
    name: str = ""
    version: str = "0.1.0"
    description: str = ""
    publisher: str = ""
    license: str = "proprietary"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: PackageStatus = PackageStatus.ACTIVE


@dataclass
class PackageDependencies:
    required: list[dict[str, Any]] = field(default_factory=list)
    optional: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PackageCapabilities:
    provides: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)


@dataclass
class PackageCompatibility:
    platform_core: str = ">=1.0.0"
    runtime: str = "python>=3.11"
    sdk_version: str = ">=1.0.0"


@dataclass
class PackageLifecycle:
    maturity: LifecycleMaturity = LifecycleMaturity.EXPERIMENTAL
    status: PackageStatus = PackageStatus.ACTIVE
    deprecation_date: datetime | None = None
    sunset_date: datetime | None = None


@dataclass
class PackageChecksum:
    algorithm: str = "sha256"
    value: str = ""


@dataclass
class PackageSignature:
    algorithm: SignatureAlgorithm = SignatureAlgorithm.SHA256
    certificate: str = ""
    signature: str = ""
    signed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    signer: str = ""


@dataclass
class PackageManifest:
    package: PackageIdentity = field(default_factory=PackageIdentity)
    identity: dict[str, Any] = field(default_factory=dict)
    compatibility: PackageCompatibility = field(default_factory=PackageCompatibility)
    dependencies: PackageDependencies = field(default_factory=PackageDependencies)
    capabilities: PackageCapabilities = field(default_factory=PackageCapabilities)
    lifecycle: PackageLifecycle = field(default_factory=PackageLifecycle)
    security: dict[str, Any] = field(default_factory=dict)
    checksum: PackageChecksum = field(default_factory=PackageChecksum)


@dataclass
class RegistryEntry:
    uuid: PackageUUID = field(default_factory=PackageUUID)
    name: str = ""
    version: str = "0.1.0"
    publisher: str = ""
    signature: PackageSignature = field(default_factory=PackageSignature)
    dependencies: PackageDependencies = field(default_factory=PackageDependencies)
    capabilities: PackageCapabilities = field(default_factory=PackageCapabilities)
    compatibility: PackageCompatibility = field(default_factory=PackageCompatibility)
    lifecycle: PackageLifecycle = field(default_factory=PackageLifecycle)
    checksum: PackageChecksum = field(default_factory=PackageChecksum)
    license: str = "proprietary"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: PackageStatus = PackageStatus.ACTIVE


@dataclass
class RepositoryConfig:
    name: str = ""
    type: RepositoryType = RepositoryType.LOCAL
    url: str = ""
    priority: int = 0
    enabled: bool = True
    trusted: bool = False
    mirror_of: str = ""
    last_synced: datetime | None = None


@dataclass
class InstallRecord:
    package_name: str = ""
    package_version: str = ""
    install_path: str = ""
    installed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    checksum: PackageChecksum = field(default_factory=PackageChecksum)
    status: InstallStatus = InstallStatus.PENDING
    repository: str = ""
    dependencies_installed: list[str] = field(default_factory=list)


@dataclass
class Snapshot:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    description: str = ""
    installed_packages: list[InstallRecord] = field(default_factory=list)
    checksum: str = ""


@dataclass
class Transaction:
    id: UUID = field(default_factory=uuid4)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    operations: list[dict[str, Any]] = field(default_factory=list)
    status: str = "pending"
    error: str | None = None
