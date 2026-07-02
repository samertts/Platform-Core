from __future__ import annotations

import os
import tempfile

import pytest

from platform_core.runtime.config.engine import ConfigurationEngine
from platform_core.runtime.config.schema import ConfigField, ConfigSchema


@pytest.fixture
def schema() -> ConfigSchema:
    s = ConfigSchema()
    s.add_field(ConfigField(name="database.url", type=str, required=True))
    s.add_field(ConfigField(name="database.pool_size", type=int, default=5))
    s.add_field(ConfigField(name="logging.level", type=str, default="INFO"))
    return s


@pytest.fixture
def engine(schema: ConfigSchema) -> ConfigurationEngine:
    return ConfigurationEngine(schema=schema)


class TestConfigurationEngine:
    def test_initial_state(self, engine: ConfigurationEngine) -> None:
        assert not engine.loaded
        assert engine.sources == []
        assert engine.all == {}

    @pytest.mark.asyncio
    async def test_load_env_prefix(self, engine: ConfigurationEngine) -> None:
        os.environ["TEST_DB_URL"] = "postgresql://localhost/test"
        os.environ["TEST_DB_POOL"] = "10"
        try:
            await engine.load(["TEST_"])
            assert engine.get("db.url") == "postgresql://localhost/test"
            assert engine.get("db.pool") == 10
        finally:
            del os.environ["TEST_DB_URL"]
            del os.environ["TEST_DB_POOL"]

    @pytest.mark.asyncio
    async def test_load_json_file(self, engine: ConfigurationEngine) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"database": {"url": "sqlite:///test.db"}}')
            f.flush()
            try:
                await engine.load([f.name])
                assert engine.get("database.url") == "sqlite:///test.db"
            finally:
                os.unlink(f.name)

    @pytest.mark.asyncio
    async def test_load_yaml_file(self, engine: ConfigurationEngine) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("database:\n  url: sqlite:///test.yaml.db\n")
            f.flush()
            try:
                await engine.load([f.name])
                assert engine.get("database.url") == "sqlite:///test.yaml.db"
            finally:
                os.unlink(f.name)

    def test_get_with_default(self, engine: ConfigurationEngine) -> None:
        assert engine.get("nonexistent", "default") == "default"

    def test_get_section(self, engine: ConfigurationEngine) -> None:
        engine._config = {"database": {"url": "test", "pool": 5}}
        section = engine.get_section("database")
        assert section == {"url": "test", "pool": 5}

    def test_set_value(self, engine: ConfigurationEngine) -> None:
        engine.set("new.key", "value")
        assert engine.get("new.key") == "value"

    def test_validate_missing_required(self, engine: ConfigurationEngine) -> None:
        errors = engine.validate()
        assert any("database.url" in e for e in errors)

    def test_validate_valid(self, engine: ConfigurationEngine) -> None:
        engine._config = {"database.url": "sqlite:///test.db"}
        errors = engine.validate()
        assert not any("database.url" in e for e in errors)

    def test_watch_callback(self, engine: ConfigurationEngine) -> None:
        changes: list[tuple[str, object, object]] = []
        engine.watch("test", lambda k, o, n: changes.append((k, o, n)))
        engine.set("test", "value")
        assert len(changes) == 1
        assert changes[0] == ("test", None, "value")

    def test_schema_property(self, engine: ConfigurationEngine) -> None:
        schema = engine.schema
        assert "database.url" in schema
        assert schema["database.url"]["required"] is True
