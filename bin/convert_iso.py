#!/usr/bin/python3

import argparse
import logging
import shlex
import subprocess
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a DVD ISO to MP4 using HandBrakeCLI"
    )

    parser.add_argument("input", help="Path to input ISO file")
    parser.add_argument("output", help="Path to output MP4 file")

    parser.add_argument(
        "-t",
        "--title",
        type=int,
        help="DVD title number (default: auto)",
    )

    parser.add_argument(
        "-p",
        "--preset",
        default="Fast 1080p30",
        help="HandBrake preset (default: %(default)s)",
    )

    parser.add_argument(
        "--start",
        type=int,
        help="Start time in seconds (for partial encodes)",
    )

    parser.add_argument(
        "--duration",
        type=int,
        help="Encode duration in seconds (for test clips)",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--scan",
        action="store_true",
        help="Scan ISO to list available titles (no encoding)",
    )

    group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress HandBrake output",
    )

    return parser.parse_args()


def get_video_height(input_file):
    """Use MediaInfo to get the source video height"""
    cmd = ["mediainfo", "--Inform=Video;%Height%", str(input_file)]
    try:
        height_str = (
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
        return int(height_str)
    except subprocess.CalledProcessError:
        print("Error: failed to run mediainfo")
        sys.exit(1)
    except ValueError:
        print(f"Error: invalid height returned: {height_str}")
        sys.exit(1)


def build_command(args):
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    cmd = ["HandBrakeCLI", "-i", str(input_path)]

    if args.quiet:
        cmd += ["-v", "quiet"]

    # Scan mode
    if args.scan:
        cmd += ["-t", "0"]
        return cmd

    # Output + preset
    cmd += ["-o", args.output, "--preset", args.preset]

    # Title
    if args.title is not None:
        cmd += ["-t", str(args.title)]

    # Always enforce square pixels
    height = get_video_height(input_path)
    cmd += ["--non-anamorphic", "-l", str(height)]

    # Partial encode options
    if args.start is not None:
        cmd += ["--start-at", f"duration:{args.start}"]

    if args.duration is not None:
        cmd += ["--stop-at", f"duration:{args.duration}"]

    return cmd


def run(cmd, quiet=False):
    try:
        logging.info("Running command: %s", shlex.join(cmd))

        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if not quiet:
            logging.info("\n%s", result.stdout)

        return result

    except subprocess.CalledProcessError as e:
        logging.error("Error during conversion")
        if e.stdout:
            logging.error("\n%s", e.stdout)
        sys.exit(e.returncode)


def setup_logging(quiet: bool):
    level = logging.ERROR if quiet else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def main():
    args = parse_args()
    setup_logging(args.quiet)
    cmd = build_command(args)
    run(cmd, quiet=args.quiet)


if __name__ == "__main__":
    main()
