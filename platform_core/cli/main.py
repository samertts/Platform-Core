"""
Platform-Core Command Line Interface

Genesis Version 0.1.0
"""

from pathlib import Path
import argparse
import platform
import sys

VERSION = "0.1.0"


def banner():
    print("=" * 60)
    print("Platform-Core")
    print("Knowledge Driven Engineering Platform")
    print(f"Version : {VERSION}")
    print("=" * 60)


def doctor():
    print("\nRunning Platform Doctor...\n")

    print(f"Python Version : {platform.python_version()}")
    print(f"Operating System : {platform.system()} {platform.release()}")
    print(f"Current Directory : {Path.cwd()}")

    required = [
        "README.md",
        "pyproject.toml",
        "platform_core",
    ]

    print()

    for item in required:
        if Path(item).exists():
            print(f"[ OK ] {item}")
        else:
            print(f"[FAIL] {item}")

    print("\nDoctor Finished.")


def init():
    print("\nPlatform-Core Initialization Complete.")


def validate():
    print("\nValidation is not implemented yet.")


def build():
    print("\nBuild system is not implemented yet.")


def main():

    parser = argparse.ArgumentParser(
        prog="platform",
        description="Platform-Core CLI"
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="doctor"
    )

    args = parser.parse_args()

    banner()

    if args.command == "doctor":
        doctor()

    elif args.command == "init":
        init()

    elif args.command == "validate":
        validate()

    elif args.command == "build":
        build()

    else:
        print(f"\nUnknown command: {args.command}")


if __name__ == "__main__":
    main()
