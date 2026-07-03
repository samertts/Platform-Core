from __future__ import annotations

from typing import Any

from platform_core.cli.core.parser import build_parser


def main() -> int:
    parser = build_parser()

    args = parser.parse_args()

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    handler: Any = args.handler
    result: int = handler(args)
    return result
