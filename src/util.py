import os
import time
import functools


def absolute_path(relative_path: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)

