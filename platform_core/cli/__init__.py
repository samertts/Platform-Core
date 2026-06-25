"""Platform Package Manager CLI - Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from platform_core.packages.manager import PackageManager, PackageError


class PlatformCLI:
    """Command-line interface for the Platform Package Manager."""

    def __init__(self) -> None:
        self._manager = PackageManager()
        self._parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="platform",
            description="Platform Package Manager - Manage modules for the Unified Healthcare Platform",
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        install = subparsers.add_parser("install", help="Install a package")
        install.add_argument("package", help="Package name")
        install.add_argument("--version", "-v", default="", help="Specific version")
        install.add_argument("--dry-run", action="store_true", help="Dry run")

        uninstall = subparsers.add_parser("uninstall", help="Uninstall a package")
        uninstall.add_argument("package", help="Package name")

        update = subparsers.add_parser("update", help="Update a package")
        update.add_argument("package", help="Package name")
        update.add_argument("--version", "-v", default="", help="Target version")

        search = subparsers.add_parser("search", help="Search packages")
        search.add_argument("query", help="Search query")

        subparsers.add_parser("list", help="List installed packages")

        publish = subparsers.add_parser("publish", help="Publish a package")
        publish.add_argument("path", help="Package path")
        publish.add_argument("--name", required=True, help="Package name")
        publish.add_argument("--version", required=True, help="Package version")
        publish.add_argument("--publisher", default="", help="Publisher name")

        verify = subparsers.add_parser("verify", help="Verify a package")
        verify.add_argument("package", help="Package name")

        subparsers.add_parser("doctor", help="Check system health")

        repair = subparsers.add_parser("repair", help="Repair a package")
        repair.add_argument("package", help="Package name")

        rollback = subparsers.add_parser("rollback", help="Rollback a package")
        rollback.add_argument("package", help="Package name")

        registry = subparsers.add_parser("registry", help="Registry operations")
        registry.add_argument("action", choices=["list", "count", "stats"], help="Registry action")

        return parser

    def run(self, args: list[str] | None = None) -> int:
        parsed = self._parser.parse_args(args)

        if not parsed.command:
            self._parser.print_help()
            return 0

        try:
            handler = getattr(self, f"_cmd_{parsed.command}")
            result = handler(parsed)
            print(json.dumps(result, indent=2, default=str))
            return 0
        except PackageError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 2

    def _cmd_install(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.install(
            package_name=args.package,
            version=args.version,
            dry_run=args.dry_run,
        )

    def _cmd_uninstall(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.uninstall(args.package)

    def _cmd_update(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.update(
            package_name=args.package,
            target_version=args.version,
        )

    def _cmd_search(self, args: argparse.Namespace) -> dict[str, Any]:
        results = self._manager.search(args.query)
        return {"query": args.query, "results": results}

    def _cmd_list(self, args: argparse.Namespace) -> dict[str, Any]:
        packages = self._manager.list_installed()
        return {"packages": packages, "count": len(packages)}

    def _cmd_publish(self, args: argparse.Namespace) -> dict[str, Any]:
        from platform_core.packages import PackageManifest

        manifest = PackageManifest()
        manifest.package.name = args.name
        manifest.package.version = args.version
        manifest.package.publisher = args.publisher

        return self._manager.publish(args.path, manifest)

    def _cmd_verify(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.verify(args.package)

    def _cmd_doctor(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.doctor()

    def _cmd_repair(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.repair(args.package)

    def _cmd_rollback(self, args: argparse.Namespace) -> dict[str, Any]:
        return self._manager.rollback(args.package)

    def _cmd_registry(self, args: argparse.Namespace) -> dict[str, Any]:
        if args.action == "list":
            packages = self._manager.registry.list_packages()
            return {
                "packages": [
                    {"name": p.name, "version": p.version, "status": p.status.value}
                    for p in packages
                ]
            }
        elif args.action == "count":
            return {"count": self._manager.registry.count()}
        elif args.action == "stats":
            return {
                "total_packages": self._manager.registry.count(),
                "repositories": self._manager.repository_manager.get_repository_stats(),
            }
        return {}


def main() -> int:
    cli = PlatformCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
