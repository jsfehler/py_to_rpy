import argparse
import errno
import json
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

parser.add_argument(
    "--minify",
    help="Output rpy to one file instead of multiple",
    nargs="?"
)

extra_indent = "    "


def __get_config():
    """Get data from the config file."""
    with open("py_to_rpy.json", "r") as f:
        raw = f.read()
        data = json.loads(raw)

    return data


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
    # Don't strip lines that are specifically ignored.
    ignore_lines = __get_config()["ignore"]
    for ignore_line in ignore_lines:
        if line.startswith(ignore_line):
            return False

    # Strip lines that are specifically declared.
    remove_lines = __get_config()["remove"]
    for remove_line in remove_lines:
        if line.startswith(remove_line):
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


def combine_rpy_files(filenames, final_filename, dest=None):
    """Combines multiple .rpy files into one.

    Args:
        filenames (list): The files to combine.
        final_filename (string): The name for the combined file.
        dest (string): The directory to place the file.
    """
    if dest:
        dest_string = "{}/".format(dest)

    else:
        dest_string = ""

    with open("{}{}.rpy".format(dest_string, final_filename), "a") as f_file:
        for filename in filenames:
            f_file.write("\n")
            with open("{}{}.rpy".format(dest_string, filename), "r") as f:
                f_file.write(f.read())


def remove_generated_files(files, dest=None):
    """Deletes all the generated .rpy files.

    Args:
        files (list): The files to remove.
        dest (string): The directory the files are in.
    """
    if dest:
        dest_string = "{}/".format(dest)

    else:
        dest_string = ""

    for file in files:
        os.remove("{}{}.rpy".format(dest_string, file))


if __name__ == "__main__":
    file_list = parser.parse_args().files
    dest_dir = parser.parse_args().dest
    strict = parser.parse_args().strict
    for item in file_list:
        py_to_rpy(item, dest=dest_dir, strict=strict)

    minify_filename = parser.parse_args().minify
    if minify_filename:
        combine_rpy_files(file_list, minify_filename, dest_dir)
        remove_generated_files(file_list, dest_dir)
