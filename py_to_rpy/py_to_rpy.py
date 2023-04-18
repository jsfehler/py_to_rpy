import errno
import json
import os

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


def _is_forbidden(line):
    """Checks if a line should be skipped.

    Args:
        line (string): The line of to validate.

    Returns:
        True if any forbidden lines found, else False.
    """
    processed_line = line.lstrip()

    # Don't strip lines that are specifically ignored.
    ignore_lines = __get_config()["ignore"]
    for ignore_line in ignore_lines:
        if processed_line.startswith(ignore_line):
            return False

    # Strip lines that are specifically declared.
    remove_lines = __get_config()["remove"]
    for remove_line in remove_lines:
        if processed_line.startswith(remove_line):
            return True

    return False


def py_to_rpy(filename, dest=None, strict=False):
    """Transpiles a Python file to a Ren'Py file.

    Creates a new .rpy file with an 'init python' block.

    Args:
        dest (string): The folder to place transpiled files into.
        strict (boolean): If true, all renpy imports are skipped.

    """
    # If saving into a different destination than the origin file,
    # build the path out of destination + the filename
    if dest:
        __safe_new_directory(dest)
        dest_string = "{}/".format(dest)
        rpy_filename = os.path.basename(filename)[:-3]

    else:
        dest_string = ""
        rpy_filename = filename[:-3]

    rpy_path = "{}{}.rpy".format(dest_string, rpy_filename)

    with open(filename, "r") as py_file, open(rpy_path, "w") as rpy_file:
        rpy_file.write("init python:\n")

        for line in py_file:
            if strict and _is_forbidden(line):
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
    # If saving into a different destination than the origin file,
    # build the path out of destination + the filename
    if dest:
        dest_string = "{}/".format(dest)

    else:
        dest_string = ""

    ordered = __get_config()["order"]
    unordered = [i for i in filenames if i not in ordered]
    ordered_filenames = ordered + unordered

    with open("{}{}.rpy".format(dest_string, final_filename), "a") as f_file:
        f_file.write("init python:\n")
        for filename in ordered_filenames:
            f_file.write("\n")

            if dest:
                rpy_filename = os.path.basename(filename)
            else:
                rpy_filename = filename

            with open("{}{}.rpy".format(dest_string, rpy_filename), "r") as f:
                for line in f.readlines():
                    if line != "init python:\n":
                        f_file.write(line)


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
        if dest:
            rpy_filename = os.path.basename(file)
        else:
            rpy_filename = file

        os.remove("{}{}.rpy".format(dest_string, rpy_filename))
