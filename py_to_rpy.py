import argparse
import errno
import os

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

extra_indent = "    "


def __safe_new_directory(dest):
    """Create a directory if it doesn't already exist.
    If it exists, do nothing.

    Raises:
        OSError if any other error occurs.

    Returns:
        True if new directory created, else False.
    """
    try:
        os.makedirs(dest)
        return True

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return False


def __is_forbidden(line):
    """Checks if a line should be skipped.

    Args:
        line (string): The line of to validate.

    Returns:
        True if any forbidden lines found, else False.
    """
    forbidden_lines = [
        # No need to import renpy in .rpy files
        "import renpy.exports as renpy",
        # .rpy files don't need renpy imports
        "from renpy."
    ]

    for forbidden_line in forbidden_lines:
        if line.startswith(forbidden_line):
            return True

    return False


def py_to_rpy(filename, dest=None, strict=False):
    """Transpiles a Python file to a Ren'Py file.

    Creates a new .rpy file with an 'init python' block.

    Args:
        dest (string): The folder to place transpiled files into.
        strict (boolean): If true, all renpy imports are skipped.

    """
    if dest:
        dest_string = "{}/".format(dest)
        __safe_new_directory(dest)

    else:
        dest_string = ""

    py_path = "{}.py".format(filename)
    rpy_path = "{}{}.rpy".format(dest_string, filename)

    with open(py_path, "r") as py_file, open(rpy_path, "w") as rpy_file:
        rpy_file.write("init python:")
        rpy_file.write("\n")

        for line in py_file:
            if strict and __is_forbidden(line):
                continue

            if line.strip():  # Line has content on it
                rpy_file.write("{}{}".format(extra_indent, line))
            else:  # Line had only whitespace
                rpy_file.write("\n")


if __name__ == "__main__":
    file_list = parser.parse_args().files
    dest_dir = parser.parse_args().dest
    strict = parser.parse_args().strict
    for item in file_list:
        py_to_rpy(item, dest=dest_dir, strict=strict)
