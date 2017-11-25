import argparse
import glob

from .py_to_rpy import py_to_rpy
from .py_to_rpy import combine_rpy_files
from .py_to_rpy import remove_generated_files


def run(file_list, dest_dir, strict, minify_filename):
    scanned_files = []

    for f in file_list:
        for item in glob.glob(f):
            py_to_rpy(item, dest=dest_dir, strict=strict)
            scanned_files.append(item)

    if minify_filename:
        for i in range(0, len(scanned_files)):
            scanned_files[i] = scanned_files[i][:-3]

        combine_rpy_files(scanned_files, minify_filename, dest_dir)
        remove_generated_files(scanned_files, dest_dir)


def main():
    """Executes the py_to_rpy from the command-line."""
    parser = argparse.ArgumentParser()

    parser.add_argument("files", help="List of files to convert", nargs="+")

    parser.add_argument(
        "--dest",
        help="The folder to place transpiled files into",
        nargs="?"
    )

    parser.add_argument(
        "--strict",
        help="When this flag is active, all renpy imports are skipped",
        action='store_true'
    )

    parser.add_argument(
        "--minify",
        help="Output rpy to one file instead of multiple",
        nargs="?"
    )

    file_list = parser.parse_args().files
    dest_dir = parser.parse_args().dest
    strict = parser.parse_args().strict
    minify_filename = parser.parse_args().minify

    run(file_list, dest_dir, strict, minify_filename)
