from pathlib import Path
import platform


def doctor():

    print()

    print("Platform Doctor")

    print("-" * 40)

    print(f"Python : {platform.python_version()}")

    print(f"OS : {platform.system()}")

    print()

    required = [

        "README.md",

        "pyproject.toml",

        "platform_core",

    ]

    for item in required:

        if Path(item).exists():

            print(f"[ OK ] {item}")

        else:

            print(f"[FAIL] {item}")

    print()

    print("Doctor Finished.")
