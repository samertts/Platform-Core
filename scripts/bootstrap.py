"""
Platform-Core Bootstrap

Creates the basic Platform-Core structure.

Genesis Version 0.1.0
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIRECTORIES = [
    "platform_core",
    "platform_core/kernel",
    "platform_core/runtime",
    "platform_core/contracts",
    "platform_core/registry",
    "platform_core/events",
    "platform_core/security",
    "platform_core/manifest",
    "platform_core/identity",
    "platform_core/shared",
    "platform_core/bootstrap",
    "docs",
    "tests",
    "examples",
    "templates",
]

for directory in DIRECTORIES:
    path = ROOT / directory
    path.mkdir(parents=True, exist_ok=True)
    print(f"Created: {path}")

print("\nPlatform-Core Bootstrap Complete.")
