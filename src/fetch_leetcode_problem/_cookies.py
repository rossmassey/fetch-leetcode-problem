"""
Get cookie for LeetCode API
"""


def get_leetcode_session_cookie(cookie_file: str) -> dict:
    """
    Get the LEETCODE_SESSION token from browser cookies file

    Args:
        cookie_file (str): path to Netscape HTTP Cookie File

    Returns:
        dict: containing token
    """
    token = ''
    try:
        with open(cookie_file, 'r') as file:
            for line in file:
                if 'LEETCODE_SESSION' in line:
                    items = line.strip().split('\t')
                    token = items[-1]  # token value is last item

    except FileNotFoundError:
        print(f'Could not find {cookie_file}')

    if not token:
        print(f'LEETCODE_SESSION token not found')

    return {'LEETCODE_SESSION': token}
