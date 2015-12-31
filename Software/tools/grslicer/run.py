#!/usr/bin/env python

import argparse

from grslicer.settings import settings_iter
from grslicer import run
from grslicer.util import progress


def _ask_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('-o', '--output', help='Output G-Code file')
    parser.add_argument('-is', '--settings',
                        help='Input settings file (will be overridden if additional parameters are supplied)')
    parser.add_argument('-os', '--output-settings', dest="output_settings",
                        help='Output file where used settings will be stored')
    parser.add_argument('--scanline', action='store_true', dest="scan_line",
                        help='Use a scan line slicer')

    help_template = '{}: {} (default: {})'
    for group_key, prop in settings_iter():
        h = help_template.format(group_key, prop.description, prop.default)
        parser.add_argument('-' + prop.arg, '--' + prop.name, type=prop.TYPE, help=h, default=prop.default)
    return parser.parse_args()


if __name__ == "__main__":
    args = _ask_parameters()
    progress.init(progress.ProgressReporterToPrint(delta_ms=300))

    run.slicing(args.input, args.output, args.settings, vars(args), args.output_settings, args.scan_line)
