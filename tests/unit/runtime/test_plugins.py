from __future__ import annotations

import pytest

from platform_core.runtime.plugins.engine import PluginEngine


class TestPluginEngine:
    def test_init(self) -> None:
        engine = PluginEngine()
        assert engine.plugin_count == 0

    def test_list_plugins_empty(self) -> None:
        engine = PluginEngine()
        assert engine.list_plugins() == []

    def test_validate_compatibility_not_found(self) -> None:
        engine = PluginEngine()
        errors = engine.validate_compatibility("nonexistent")
        assert len(errors) == 1

    @pytest.mark.asyncio
    async def test_discover_empty_paths(self) -> None:
        engine = PluginEngine()
        result = await engine.discover([])
        assert result == []

    @pytest.mark.asyncio
    async def test_load_nonexistent(self) -> None:
        engine = PluginEngine()
        with pytest.raises(ValueError, match="not found"):
            await engine.load("nonexistent")

    @pytest.mark.asyncio
    async def test_activate_nonexistent(self) -> None:
        engine = PluginEngine()
        with pytest.raises(ValueError, match="not found"):
            await engine.activate("nonexistent")

    def test_get_plugin_none(self) -> None:
        engine = PluginEngine()
        assert engine.get_plugin("nonexistent") is None
