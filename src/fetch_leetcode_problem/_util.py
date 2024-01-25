"""
Common utility functions
"""
import os


def absolute_path(relative_path: str) -> str:
    """
    Get absolute path to file in fetch_leetcode_problem directory

    Args:
        relative_path (str): relative path to file

    Returns:
        str: absolute path to file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)
