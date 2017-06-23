"""Extra libraries"""
import os
import sys


def home_dir():
    """Find user home directory path"""
    home_addr = os.path.expanduser("~")

    if os.path.exists(home_addr):
        return home_addr


def base_dir():
    """Return base project directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_exists(path: str, f: str=None):
    """Check file existance in the path."""
    if f is not None:
        path = os.path.join(path, f)
    return os.path.exists(path)


def create_dir(path: str, d: str):
    """Create directory(d) in the path."""
    try:
        os.mkdir(os.path.join(path, d))
        return True
    except:
        return False


def has_all_access(path):
    """Check all permissions on a file"""
    if not os.path.exists(path):
        return False

    if os.access(path, os.R_OK) and os.access(path, os.W_OK):
        return True
    return False


def create_empty_db_file(db_name):
    """Create empty database in user home directory"""
    try:
        open(os.path.join(home_dir(), db_name), "w").close()
        return True
    except PermissionError:
        print("Could not create new db file.")
    return False


def create_file_with_content(path: str, f: str, content: str):
    """Create file with content."""
    with open(os.path.join(path, f), "w") as f:
        f.write(content)
    return True


def error(message):
    """Print error message with red color."""
    print("\033[91m{}\033[0m".format(message))


def exit_software(exit_code):
    """Exit the software process."""
    sys.exit(exit_code)


def join_path(p1: str, p2: str):
    """Join paths."""
    return os.path.join(p1, p2)
