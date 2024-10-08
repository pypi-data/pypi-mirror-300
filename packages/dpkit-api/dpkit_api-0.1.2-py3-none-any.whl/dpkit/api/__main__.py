import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any


def cli_openapi(args: Any) -> None:
    from dpkit.api.app import make_app

    app = make_app(store=None, modules=None, users=None)
    out = ""

    if args.format == "json":
        out = json.dumps(app.openapi(), indent=2)

    if args.format == "yaml":
        import yaml

        out = yaml.dump(app.openapi())

    if not out:
        raise RuntimeError(f"unknown format: {args.format}")

    if args.output == "-":
        print(out)
    else:
        Path(args.output).write_text(out)


def openapi(p: ArgumentParser) -> None:
    p.set_defaults(func=cli_openapi)
    p.add_argument(
        "--output",
        help="path to the output (use '-' for stdout)",
        type=str,
        default="-",
    )
    p.add_argument(
        "--format",
        help="format to use for output (json or yaml)",
        type=str,
        default="json",
    )


def main(args: Any = None) -> None:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    for function in [openapi]:
        function(subparsers.add_parser(function.__name__.replace("_", "-")))
    opts = parser.parse_args(args)

    try:
        if not hasattr(opts, "func"):
            parser.print_help(sys.stderr)
            sys.exit(2)

        opts.func(opts)
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
