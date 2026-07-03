from pathlib import Path

from platform_core.generator.engine import GeneratorEngine


def test_generate_service(tmp_path: Path) -> None:

    engine = GeneratorEngine()

    result = engine.generate_service(
        tmp_path,
        "user",
    )

    assert result.success

    assert result.created_files == 4

    assert result.created_directories == 1

    assert (tmp_path / "platform_core" / "services" / "user" / "service.py").exists()
