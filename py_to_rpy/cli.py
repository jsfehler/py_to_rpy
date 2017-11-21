import argparse

from py_to_rpy import py_to_rpy
from py_to_rpy import combine_rpy_files
from py_to_rpy import remove_generated_files


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


def main():
    """Executes the py_to_rpy from the command-line."""
    file_list = parser.parse_args().files
    dest_dir = parser.parse_args().dest
    strict = parser.parse_args().strict
    for item in file_list:
        py_to_rpy(item, dest=dest_dir, strict=strict)

    minify_filename = parser.parse_args().minify
    if minify_filename:
        combine_rpy_files(file_list, minify_filename, dest_dir)
        remove_generated_files(file_list, dest_dir)
