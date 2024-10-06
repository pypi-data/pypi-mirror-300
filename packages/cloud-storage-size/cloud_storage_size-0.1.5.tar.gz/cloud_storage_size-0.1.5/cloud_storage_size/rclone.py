"""
https://github.com/Johannes11833/rclone_python/blob/master/rclone_python/rclone.py
"""
import os
import json
import logging
import platform
import subprocess
import zipfile
import urllib.request

from functools import wraps
from shutil import which, move, rmtree
from .rclone_env import parse_path_uri, parse_env, parse_config_to_conn_str

logger = logging.getLogger(__name__)


def user_home_local_bin():
    """
    :return: The path to the ~/.local/bin directory.
    """
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin")
    return local_bin


def ensure_path_includes_local_bin():
    """
    Ensure that ~/.local/bin is in the PATH environment variable.
    If it's not, add it and update the .bashrc or .bash_profile file.
    """
    local_bin = user_home_local_bin()
    # Check if ~/.local/bin exists
    if not os.path.exists(local_bin):
        os.makedirs(local_bin, exist_ok=True)

    # Check if ~/.local/bin is in PATH
    if local_bin not in os.environ["PATH"].split(os.pathsep):
        # Add to PATH for the current session
        os.environ["PATH"] = f"{local_bin}:{os.environ['PATH']}"


def __install_rclone():
    """
    Install rclone on the system, location: ~/.local/bin
    This function works for Unix-like systems (Linux/macOS).
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system not in ['linux', 'darwin']:
        raise NotImplementedError(f"Automatic installation not supported for {system}")

    # Determine the appropriate rclone download URL
    if system == 'linux':
        os_name = 'linux'
    else:  # darwin (macOS)
        os_name = 'osx'

    if 'arm' in machine or 'aarch64' in machine:
        arch = 'arm64'
    else:
        arch = 'amd64'

    url = f"https://downloads.rclone.org/rclone-current-{os_name}-{arch}.zip"

    # Create ~/.local/bin if it doesn't exist
    install_dir = os.path.expanduser("~/.local/bin")
    os.makedirs(install_dir, exist_ok=True)

    # Download rclone
    print("Downloading rclone...")
    filename, _ = urllib.request.urlretrieve(url)

    # Extract the zip file
    print("Extracting rclone...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(install_dir)

    # Move the rclone binary to ~/.local/bin
    extracted_dir = os.path.join(install_dir, f"rclone-*-{os_name}-{arch}")
    extracted_dirs = [d for d in os.listdir(install_dir) if d.startswith("rclone-")]
    if extracted_dirs:
        extracted_dir = os.path.join(install_dir, extracted_dirs[0])
        move(os.path.join(extracted_dir, "rclone"), os.path.join(install_dir, "rclone"))

        # Clean up
        rmtree(extracted_dir)

    # Clean up
    os.remove(filename)

    # Make rclone executable
    os.chmod(os.path.join(install_dir, "rclone"), 0o755)

    # Ensure ~/.local/bin is in PATH
    ensure_path_includes_local_bin()

    print(f"rclone has been installed to {install_dir}")
    print("~/.local/bin has been added to your PATH if it wasn't already there.")
    print("Please restart your terminal or run 'source ~/.bashrc' for the changes to take effect.")


def is_installed() -> bool:
    """
    :return: True if rclone is correctly installed on the system.
    """
    if which("rclone") is None:
        return False
    command = ["rclone", "version"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def __check_installed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_installed():
            __install_rclone()
        return func(*args, **kwargs)

    return wrapper


def _run_rclone_cmd(command: str, env=None) -> str:
    result = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("rclone command failed: %s", result.stderr)
        return None
    return result.stdout


@__check_installed
def ls(remote: str, flags: str = "") -> str:
    """
    List the contents of a remote.
    :param remote: The remote to list.
    :param flags: Additional flags to pass to the rclone command.
    :return: The output of the rclone command.
    """
    command = f"rclone ls {remote} {flags}"
    return subprocess.run(command, shell=True, check=True, capture_output=True, text=True).stdout


@__check_installed
def size(bucket_uri: str, **kwargs) -> str:
    """
    List the contents of a remote.
    
    kwargs:
    - conn_str
    - config

    https://rclone.org/docs/#connection-strings
    """
    scheme, bucket_name, _ = parse_path_uri(bucket_uri)

    conn_str = kwargs.get("conn_str", None)
    config = kwargs.get("config", None)
    if not conn_str and config:
        conn_str = parse_config_to_conn_str(config)

    remote = f"{conn_str}{bucket_name}" if conn_str else f"myremote:{bucket_name}"

    local_bin = user_home_local_bin()
    command = [f"{local_bin}/rclone", "size", remote, "--fast-list", "--json"]

    if conn_str:
        # print(command)
        stdout = _run_rclone_cmd(command)
    else:
        env = parse_env(scheme)
        # print(command, env)
        stdout = _run_rclone_cmd(command, env)

    size_info = json.loads(stdout)
    return size_info
