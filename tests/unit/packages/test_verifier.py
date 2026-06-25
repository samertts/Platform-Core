"""Unit tests for Package Verification."""

import pytest
from platform_core.verifier import PackageVerifier, VerificationError


class TestPackageVerifier:
    def test_init(self) -> None:
        verifier = PackageVerifier()
        assert verifier is not None

    def test_compute_checksum_sha256(self) -> None:
        verifier = PackageVerifier()
        checksum = verifier.compute_checksum(b"test data", "sha256")
        assert len(checksum) == 64

    def test_compute_checksum_sha512(self) -> None:
        verifier = PackageVerifier()
        checksum = verifier.compute_checksum(b"test data", "sha512")
        assert len(checksum) == 128

    def test_verify_checksum(self) -> None:
        verifier = PackageVerifier()
        data = b"test data"
        checksum = verifier.compute_checksum(data)
        assert verifier.verify_checksum(data, checksum)

    def test_verify_checksum_invalid(self) -> None:
        verifier = PackageVerifier()
        assert not verifier.verify_checksum(b"test", "invalid_checksum")

    def test_sign_and_verify(self) -> None:
        verifier = PackageVerifier()
        data = b"test data"
        sig = verifier.sign_data(data, "private_key")
        assert verifier.verify_signature(data, sig)

    def test_verify_signature_invalid(self) -> None:
        verifier = PackageVerifier()
        assert not verifier.verify_signature(b"test", {})

    def test_trust_store(self) -> None:
        verifier = PackageVerifier()
        verifier.add_trusted_certificate("test-cert", {"name": "test-cert"})
        assert verifier.is_certificate_trusted("test-cert")
        assert not verifier.is_certificate_trusted("nonexistent")

    def test_revoke_certificate(self) -> None:
        verifier = PackageVerifier()
        verifier.add_trusted_certificate("test-cert", {"name": "test-cert"})
        assert verifier.revoke_certificate("test-cert")
        assert not verifier.is_certificate_trusted("test-cert")

    def test_certificate_chain(self) -> None:
        verifier = PackageVerifier()
        verifier.add_trusted_certificate("root", {"name": "root"})
        cert = {"name": "child", "issuer": "root"}
        assert verifier.verify_certificate_chain(cert)

    def test_tamper_detection(self) -> None:
        verifier = PackageVerifier()
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            f.flush()
            try:
                correct_checksum = verifier.compute_file_checksum(f.name)
                assert not verifier.detect_tampering(f.name, correct_checksum)
                assert verifier.detect_tampering(f.name, "wrong_checksum")
            finally:
                os.unlink(f.name)

    def test_full_verification(self) -> None:
        verifier = PackageVerifier()
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            f.flush()
            try:
                checksum = verifier.compute_file_checksum(f.name)
                result = verifier.full_verification(f.name, expected_checksum=checksum)
                assert result["overall_valid"]
            finally:
                os.unlink(f.name)

    def test_verification_log(self) -> None:
        verifier = PackageVerifier()
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            f.flush()
            try:
                verifier.full_verification(f.name)
                log = verifier.get_verification_log()
                assert len(log) == 1
            finally:
                os.unlink(f.name)

    def test_trusted_certificates_list(self) -> None:
        verifier = PackageVerifier()
        verifier.add_trusted_certificate("cert1", {"name": "cert1"})
        verifier.add_trusted_certificate("cert2", {"name": "cert2"})
        certs = verifier.get_trusted_certificates()
        assert len(certs) == 2
