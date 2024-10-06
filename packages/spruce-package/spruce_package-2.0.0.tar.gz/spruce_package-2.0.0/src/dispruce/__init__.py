import pyarrow as pa
from .sprucepy import *

# __all__ = ['Spruce']


# import ctypes
# import sys
# from pathlib import Path
# import importlib.util
# import subprocess
# import logging

# # Configure logging for debugging purposes
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# def get_poetry_env_path():
#     """Retrieve the Poetry environment path."""
#     try:
#         result = subprocess.run(
#             ["poetry", "env", "info", "-p"],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         poetry_path = Path(result.stdout.strip())
#         logger.debug(f"Poetry environment path: {poetry_path}")
#         return poetry_path
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to get Poetry environment path: {e}")
#         raise RuntimeError("Failed to retrieve Poetry environment path.") from e

# def get_pyarrow_lib_path(poetry_env_path):
#     """Construct the path to pyarrow's shared libraries."""
#     python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
#     pyarrow_path = poetry_env_path / 'lib' / python_version / 'site-packages' / 'pyarrow'
#     logger.debug(f"pyarrow library path: {pyarrow_path}")
#     return pyarrow_path

# def load_shared_library(lib_name, lib_dir):
#     """Load a shared library using its absolute path with RTLD_GLOBAL."""
#     lib_filename = {
#         'linux': f"{lib_name}.so",
#         # Uncomment and adjust the following lines if you plan to support other platforms
#         # 'darwin': f"{lib_name}.dylib",
#         # 'win32': f"{lib_name}.dll"
#     }.get(sys.platform)

#     if not lib_filename:
#         logger.error(f"Unsupported platform: {sys.platform}")
#         raise OSError(f"Unsupported platform: {sys.platform}")

#     lib_path = lib_dir / lib_filename
#     logger.debug(f"Attempting to load library: {lib_path}")

#     if not lib_path.exists():
#         logger.error(f"Shared library not found: {lib_path}")
#         raise FileNotFoundError(f"Shared library not found: {lib_path}")

#     try:
#         library = ctypes.CDLL(str(lib_path), ctypes.RTLD_GLOBAL)
#         logger.debug(f"Successfully loaded {lib_path}")
#         return library
#     except OSError as e:
#         logger.error(f"Failed to load {lib_path}: {e}")
#         raise OSError(f"Failed to load {lib_path}: {e}") from e

# # Step 1: Get Poetry environment path
# poetry_env_path = get_poetry_env_path()

# # Step 2: Get pyarrow's library path
# pyarrow_lib_path = get_pyarrow_lib_path(poetry_env_path)

# # Step 3: Define paths to your custom libraries
# current_dir = Path(__file__).resolve().parent
# libs_dir = current_dir / 'libs'
# logger.debug(f"Custom libraries directory: {libs_dir}")

# # Step 4: Load dependencies first with RTLD_GLOBAL
# # Load libarrow_python.so first
# libarrow_python = load_shared_library('libarrow_python', pyarrow_lib_path)

# # Then load libspruce.so
# libspruce = load_shared_library('libspruce', libs_dir)

# # Finally, load libA (sprucepy)
# libA = load_shared_library('sprucepy.cpython-312-x86_64-linux-gnu', libs_dir)