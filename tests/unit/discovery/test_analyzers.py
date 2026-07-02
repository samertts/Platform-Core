"""Unit tests for Analyzers."""

from platform_core.discovery.analyzers import (
    ArchitectureAnalyzer,
    CIAnalyzer,
    DependencyAnalyzer,
    DockerAnalyzer,
    DocumentationAnalyzer,
    FrameworkAnalyzer,
    LanguageAnalyzer,
    SecurityAnalyzer,
    TestingAnalyzer,
    run_all_analyzers,
)


class TestLanguageAnalyzer:
    def test_detect_python(self) -> None:
        analyzer = LanguageAnalyzer()
        files = [
            {"name": "main.py", "extension": ".py", "path": "main.py"},
            {"name": "utils.py", "extension": ".py", "path": "utils.py"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["primary"] == "Python"
        assert len(result["distribution"]) == 1

    def test_detect_mixed_languages(self) -> None:
        analyzer = LanguageAnalyzer()
        files = [
            {"name": "main.py", "extension": ".py", "path": "main.py"},
            {"name": "app.ts", "extension": ".ts", "path": "app.ts"},
            {"name": "index.js", "extension": ".js", "path": "index.js"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["primary"] == "Python"
        assert len(result["distribution"]) == 3

    def test_empty_files(self) -> None:
        analyzer = LanguageAnalyzer()
        result = analyzer.analyze("/tmp", [])
        assert result["primary"] == "Unknown"

    def test_config_files_excluded(self) -> None:
        analyzer = LanguageAnalyzer()
        files = [
            {"name": "config.yaml", "extension": ".yaml", "path": "config.yaml"},
            {"name": "data.json", "extension": ".json", "path": "data.json"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["primary"] == "Unknown"


class TestFrameworkAnalyzer:
    def test_detect_fastapi(self, tmp_path) -> None:
        (tmp_path / "requirements.txt").write_text("fastapi==0.100.0\nuvicorn==0.23.0")
        analyzer = FrameworkAnalyzer()
        files = [
            {
                "name": "requirements.txt",
                "path": "requirements.txt",
                "extension": ".txt",
            }
        ]
        result = analyzer.analyze(str(tmp_path), files)
        assert any(f["name"] == "FastAPI" for f in result["detected"])

    def test_no_frameworks(self) -> None:
        analyzer = FrameworkAnalyzer()
        result = analyzer.analyze("/tmp", [])
        assert result["detected"] == []


class TestArchitectureAnalyzer:
    def test_detect_microservices(self) -> None:
        analyzer = ArchitectureAnalyzer()
        files = [
            {"name": "docker-compose.yml", "path": "docker-compose.yml"},
            {"name": "main.py", "path": "services/api/main.py"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["pattern"] in ("microservices", "modular_monolith", "monolith")

    def test_empty_repo(self) -> None:
        analyzer = ArchitectureAnalyzer()
        result = analyzer.analyze("/tmp", [])
        assert result["pattern"] == "unknown"


class TestDocumentationAnalyzer:
    def test_full_documentation(self) -> None:
        analyzer = DocumentationAnalyzer()
        files = [
            {"name": "README.md", "path": "README.md"},
            {"name": "CHANGELOG.md", "path": "CHANGELOG.md"},
            {"name": "CONTRIBUTING.md", "path": "CONTRIBUTING.md"},
            {"name": "LICENSE", "path": "LICENSE"},
            {"name": "openapi.json", "path": "openapi.json"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["has_readme"] is True
        assert result["has_changelog"] is True
        assert result["has_license"] is True
        assert result["score"] > 0.5

    def test_missing_readme(self) -> None:
        analyzer = DocumentationAnalyzer()
        result = analyzer.analyze("/tmp", [])
        assert result["has_readme"] is False
        assert result["score"] == 0.0


class TestTestingAnalyzer:
    def test_detect_pytest(self) -> None:
        analyzer = TestingAnalyzer()
        files = [
            {"name": "test_main.py", "path": "test_main.py"},
            {"name": "test_utils.py", "path": "test_utils.py"},
            {"name": "conftest.py", "path": "conftest.py"},
        ]
        result = analyzer.analyze("/tmp", files)
        assert result["test_files"] == 2
        assert result["test_framework"] == "pytest"

    def test_no_tests(self) -> None:
        analyzer = TestingAnalyzer()
        result = analyzer.analyze("/tmp", [{"name": "main.py", "path": "main.py"}])
        assert result["test_files"] == 0


class TestSecurityAnalyzer:
    def test_detect_hardcoded_secret(self, tmp_path) -> None:
        (tmp_path / "config.py").write_text('password = "secret123"')
        analyzer = SecurityAnalyzer()
        files = [{"name": "config.py", "path": "config.py", "size": 30}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["secret_patterns_found"] > 0

    def test_clean_code(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        analyzer = SecurityAnalyzer()
        files = [{"name": "main.py", "path": "main.py", "size": 10}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["secret_patterns_found"] == 0

    def test_missing_gitignore(self) -> None:
        analyzer = SecurityAnalyzer()
        result = analyzer.analyze("/tmp", [{"name": "main.py", "path": "main.py", "size": 10}])
        assert result["has_gitignore"] is False


class TestDependencyAnalyzer:
    def test_count_requirements(self, tmp_path) -> None:
        (tmp_path / "requirements.txt").write_text("fastapi==0.100.0\nuvicorn==0.23.0\n")
        analyzer = DependencyAnalyzer()
        files = [{"name": "requirements.txt", "path": "requirements.txt"}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["total"] == 2

    def test_count_package_json(self, tmp_path) -> None:
        content = '{"dependencies": {"react": "^18.0.0"}, "devDependencies": {"jest": "^29.0.0"}}'
        (tmp_path / "package.json").write_text(content)
        analyzer = DependencyAnalyzer()
        files = [{"name": "package.json", "path": "package.json"}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["total"] == 2


class TestCIAnalyzer:
    def test_detect_github_actions(self) -> None:
        analyzer = CIAnalyzer()
        files = [{"name": "ci.yml", "path": ".github/workflows/ci.yml"}]
        result = analyzer.analyze("/tmp", files)
        assert result["system"] == "GitHub Actions"
        assert result["has_ci"] is True

    def test_no_ci(self) -> None:
        analyzer = CIAnalyzer()
        result = analyzer.analyze("/tmp", [{"name": "main.py", "path": "main.py"}])
        assert result["has_ci"] is False


class TestDockerAnalyzer:
    def test_detect_dockerfile(self, tmp_path) -> None:
        (tmp_path / "Dockerfile").write_text("FROM python:3.11\nCOPY . .\nEXPOSE 8000\n")
        analyzer = DockerAnalyzer()
        files = [{"name": "Dockerfile", "path": "Dockerfile"}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["detected"] is True
        assert result["base_image"] == "python:3.11"
        assert 8000 in result["ports"]

    def test_multi_stage(self, tmp_path) -> None:
        (tmp_path / "Dockerfile").write_text("FROM python:3.11 AS builder\nFROM python:3.11\n")
        analyzer = DockerAnalyzer()
        files = [{"name": "Dockerfile", "path": "Dockerfile"}]
        result = analyzer.analyze(str(tmp_path), files)
        assert result["multi_stage"] is True


class TestRunAllAnalyzers:
    def test_run_all(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "test_main.py").write_text("def test_x(): pass")
        files = [
            {"name": "main.py", "path": "main.py", "extension": ".py", "size": 10},
            {"name": "README.md", "path": "README.md", "extension": ".md", "size": 100},
            {
                "name": "test_main.py",
                "path": "test_main.py",
                "extension": ".py",
                "size": 30,
            },
        ]
        result = run_all_analyzers(str(tmp_path), files)
        assert result.language.primary == "Python"
        assert result.documentation.has_readme is True
        assert result.testing.test_files == 1
