from platform_core.cli.core.parser import build_parser


def main() -> int:
    parser = build_parser()

    args = parser.parse_args()

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return args.handler(args)
