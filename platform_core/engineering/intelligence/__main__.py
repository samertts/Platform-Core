"""
Engineering CLI entry point.
"""

from pathlib import Path

from .engine import EngineeringEngine


def main() -> None:

    engine = EngineeringEngine()

    result = engine.run(Path("."))

    print()

    print("Repository modules :", len(result["snapshot"].modules))

    print("Graph nodes        :", len(result["graph"].nodes()))

    print("Health score       :", result["analysis"].score)

    print()


if __name__ == "__main__":
    main()
