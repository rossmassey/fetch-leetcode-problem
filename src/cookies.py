import os


def get_leetcode_session() -> str | None:
    """
    reads and parses the cookies from 'cookies.txt',
    located in the same directory as this script

    Returns:
        dict: each key-value pair corresponds to a cookie.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_file_path = os.path.join(script_dir, 'cookies.txt')

    try:
        with open(cookies_file_path, 'r') as file:
            for line in file:
                if 'LEETCODE_SESSION' in line:
                    items = line.strip().split('\t')
                    return items[-1]

    except FileNotFoundError:
        print('Could not find cookies.txt')

    return None
