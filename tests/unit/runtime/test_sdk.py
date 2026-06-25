from __future__ import annotations

import pytest

from platform_core.runtime.sdk.loader import SDKLoader


class MockSDK:
    VERSION = "1.2.0"
    CAPABILITIES = ["auth", "logging"]
    METADATA = {"author": "test"}


class TestSDKLoader:
    def test_init(self) -> None:
        loader = SDKLoader()
        assert loader.sdk_count == 0

    def test_register(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        assert loader.sdk_count == 1

    def test_list_sdks(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        sdks = loader.list_sdks()
        assert len(sdks) == 1
        assert sdks[0]["id"] == "test-sdk"
        assert sdks[0]["version"] == "1.2.0"

    def test_get_capabilities(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        caps = loader.get_capabilities("test-sdk")
        assert "auth" in caps
        assert "logging" in caps

    def test_get_capabilities_not_found(self) -> None:
        loader = SDKLoader()
        with pytest.raises(ValueError):
            loader.get_capabilities("nonexistent")

    def test_get_sdk(self) -> None:
        loader = SDKLoader()
        sdk = MockSDK()
        loader.register("test-sdk", sdk)
        assert loader.get_sdk("test-sdk") is sdk

    def test_get_sdk_none(self) -> None:
        loader = SDKLoader()
        assert loader.get_sdk("nonexistent") is None

    def test_negotiate_version_exact(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        version = loader.negotiate_version("test-sdk", "1.2.0")
        assert version == "1.2.0"

    def test_negotiate_version_gte(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        version = loader.negotiate_version("test-sdk", ">=1.0.0")
        assert version == "1.2.0"

    def test_negotiate_version_incompatible(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        with pytest.raises(ValueError, match="not compatible"):
            loader.negotiate_version("test-sdk", ">=2.0.0")

    def test_unregister(self) -> None:
        loader = SDKLoader()
        loader.register("test-sdk", MockSDK())
        assert loader.unregister("test-sdk")
        assert loader.sdk_count == 0
        assert not loader.unregister("nonexistent")
