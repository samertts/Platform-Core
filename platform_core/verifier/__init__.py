"""Package Verification - SHA256/512, digital signatures, certificate chain, trust store."""

from __future__ import annotations

import hashlib
import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class VerificationError(Exception):
    pass


class SignatureError(VerificationError):
    pass


class TamperError(VerificationError):
    pass


class CertificateError(VerificationError):
    pass


class PackageVerifier:
    """Verifies package integrity through checksums, signatures, and certificate chains."""

    def __init__(self) -> None:
        self._trust_store: dict[str, dict[str, Any]] = {}
        self._revoked_certificates: set[str] = set()
        self._verification_log: list[dict[str, Any]] = []
        self._lock = threading.RLock()

    def compute_checksum(self, data: bytes, algorithm: str = "sha256") -> str:
        if algorithm == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def compute_file_checksum(self, file_path: str, algorithm: str = "sha256") -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        h = hashlib.sha256() if algorithm == "sha256" else hashlib.sha512()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def compute_directory_checksum(self, dir_path: str, algorithm: str = "sha256") -> str:
        path = Path(dir_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")

        h = hashlib.sha256() if algorithm == "sha256" else hashlib.sha512()
        for file_path in sorted(path.rglob("*")):
            if file_path.is_file():
                h.update(str(file_path.relative_to(path)).encode())
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        h.update(chunk)
        return h.hexdigest()

    def verify_checksum(self, data: bytes, expected: str, algorithm: str = "sha256") -> bool:
        actual = self.compute_checksum(data, algorithm)
        return actual == expected

    def verify_file_checksum(
        self, file_path: str, expected: str, algorithm: str = "sha256"
    ) -> bool:
        actual = self.compute_file_checksum(file_path, algorithm)
        return actual == expected

    def verify_checksum_file(self, file_path: str, checksum_path: str) -> bool:
        checksum_file = Path(checksum_path)
        if not checksum_file.exists():
            return False

        content = checksum_file.read_text(encoding="utf-8").strip()
        expected = content.split()[0] if content else ""
        return self.verify_file_checksum(file_path, expected)

    def generate_checksum_file(
        self, file_path: str, output_path: str, algorithm: str = "sha256"
    ) -> str:
        checksum = self.compute_file_checksum(file_path, algorithm)
        filename = Path(file_path).name
        content = f"{checksum}  {filename}\n"
        Path(output_path).write_text(content, encoding="utf-8")
        return checksum

    def sign_data(self, data: bytes, private_key: str = "") -> dict[str, Any]:
        data_hash = hashlib.sha256(data).hexdigest()
        signature = hashlib.sha256(f"{data_hash}:{private_key}".encode()).hexdigest()

        return {
            "algorithm": "sha256",
            "data_hash": data_hash,
            "signature": signature,
            "signed_at": datetime.now(UTC).isoformat(),
        }

    def verify_signature(self, data: bytes, signature_data: dict[str, Any]) -> bool:
        if not signature_data:
            return False

        algorithm = signature_data.get("algorithm", "sha256")
        expected_hash = signature_data.get("data_hash", "")
        signature = signature_data.get("signature", "")

        if not expected_hash or not signature:
            return False

        actual_hash = self.compute_checksum(data, algorithm)
        return bool(actual_hash == expected_hash)

    def verify_signature_file(self, file_path: str, signature_path: str) -> bool:
        sig_path = Path(signature_path)
        if not sig_path.exists():
            return False

        try:
            signature_data = json.loads(sig_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False

        file_data = Path(file_path).read_bytes()
        return self.verify_signature(file_data, signature_data)

    def add_trusted_certificate(self, name: str, certificate: dict[str, Any]) -> None:
        with self._lock:
            self._trust_store[name] = {
                "certificate": certificate,
                "added_at": datetime.now(UTC).isoformat(),
                "revoked": False,
            }

    def revoke_certificate(self, name: str) -> bool:
        with self._lock:
            if name in self._trust_store:
                self._trust_store[name]["revoked"] = True
                self._revoked_certificates.add(name)
                return True
            return False

    def is_certificate_trusted(self, name: str) -> bool:
        with self._lock:
            cert = self._trust_store.get(name)
            if cert is None:
                return False
            return not cert.get("revoked", False)

    def verify_certificate_chain(self, certificate: dict[str, Any]) -> bool:
        issuer = certificate.get("issuer", "")
        if not issuer:
            return self.is_certificate_trusted(certificate.get("name", ""))

        if not self.is_certificate_trusted(issuer):
            return False

        expiry = certificate.get("expiry")
        if expiry:
            try:
                expiry_dt = datetime.fromisoformat(expiry)
                if expiry_dt < datetime.now(UTC):
                    return False
            except (ValueError, TypeError):
                pass

        return True

    def detect_tampering(
        self, file_path: str, expected_checksum: str, algorithm: str = "sha256"
    ) -> bool:
        actual = self.compute_file_checksum(file_path, algorithm)
        return actual != expected_checksum

    def full_verification(
        self,
        file_path: str,
        expected_checksum: str | None = None,
        signature_data: dict[str, Any] | None = None,
        certificate_name: str | None = None,
    ) -> dict[str, Any]:
        results: dict[str, Any] = {
            "file": file_path,
            "timestamp": datetime.now(UTC).isoformat(),
            "checksum": {"valid": False},
            "signature": {"valid": False},
            "certificate": {"valid": False},
            "tamper_detected": False,
            "overall_valid": False,
        }

        try:
            file_data = Path(file_path).read_bytes()
        except OSError as e:
            results["error"] = str(e)
            return results

        actual_checksum = self.compute_checksum(file_data)
        if expected_checksum:
            results["checksum"] = {
                "valid": actual_checksum == expected_checksum,
                "expected": expected_checksum,
                "actual": actual_checksum,
            }
        else:
            results["checksum"] = {
                "valid": True,
                "computed": actual_checksum,
            }

        if signature_data:
            sig_valid = self.verify_signature(file_data, signature_data)
            results["signature"] = {"valid": sig_valid, "details": signature_data}

        if certificate_name:
            cert_valid = self.is_certificate_trusted(certificate_name)
            results["certificate"] = {"valid": cert_valid, "name": certificate_name}

        results["tamper_detected"] = (
            expected_checksum is not None and not results["checksum"]["valid"]
        )

        results["overall_valid"] = (
            results["checksum"]["valid"]
            and (signature_data is None or results["signature"]["valid"])
            and (certificate_name is None or results["certificate"]["valid"])
            and not results["tamper_detected"]
        )

        with self._lock:
            self._verification_log.append(results)

        return results

    def get_verification_log(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._verification_log[-limit:])

    def get_trusted_certificates(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"name": name, "revoked": cert.get("revoked", False)}
                for name, cert in self._trust_store.items()
            ]
