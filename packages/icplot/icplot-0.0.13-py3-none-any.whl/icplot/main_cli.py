#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path
import os

from iccore.cli_utils import launch_common
from iccore.serialization import read_yaml

from icplot.graph import Plot
from icplot.graph.matplotlib import MatplotlibPlotter
from icplot.image_utils import pdf_to_png, svg_to_png, svg_to_pdf
from icplot import tex
from icplot.tex import TexBuildSettings

logger = logging.getLogger(__name__)


def convert(args):
    launch_common(args)

    logger.info("Startubg conversion between %s and %s", args.source, args.target)

    if args.target:
        target = Path(args.target).resolve()
    else:
        target = None

    if args.source.suffix == ".pdf":
        pdf_to_png(args.source.resolve(), target)
    elif args.source.suffix == ".svg":
        if target:
            if target.suffix == ".png":
                svg_to_png(args.source.resolve(), target)
            elif target.suffix == ".pdf":
                svg_to_pdf(args.source.resolve(), target)
        else:
            svg_to_png(args.source)
    elif args.source.suffix == ".tex":
        if args.target:
            target = Path(args.target).resolve()
        else:
            target = Path(os.getcwd())

        settings = TexBuildSettings(
            args.source.resolve(), args.build_dir.resolve(), args.target
        )
        tex.build(settings)

    logger.info("Finished conversion")


def plot(args):

    launch_common(args)

    config = read_yaml(args.config.resolve())

    plotter = MatplotlibPlotter()
    if ["plots"] in config:
        for eachplot in config["plots"]:
            plot = Plot(**eachplot)
            plotter.plot(plot, args.output_dir.resolve())


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument(
        "--source",
        type=Path,
        help="Path to file to be converted from",
    )
    convert_parser.add_argument(
        "--target",
        type=str,
        default="",
        help="Path to file to be converted to",
    )
    convert_parser.add_argument(
        "--build_dir",
        default=Path(os.getcwd()) / "_build/tikz",
        help="Path for build output",
    )
    convert_parser.set_defaults(func=convert)

    plot_parser = subparsers.add_parser("plot")
    plot_parser.add_argument("--config", type=Path, help="Path to the plot config")
    plot_parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the plot output directory",
    )
    plot_parser.set_defaults(func=plot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
