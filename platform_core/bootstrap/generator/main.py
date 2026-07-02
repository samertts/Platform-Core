from pathlib import Path

from .bootstrap import engine


def main():

    workspace = Path.cwd()

    engine.run(
        "project",
        workspace,
    )

    engine.run(
        "engine",
        workspace,
    )

    engine.run(
        "capability",
        workspace,
    )

    print()

    print("Platform Bootstrap Complete")


if __name__ == "__main__":

    main()
