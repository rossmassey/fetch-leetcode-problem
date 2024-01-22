from util import absolute_path


def get_leetcode_session_cookie() -> dict:
    """
    reads and parses the cookies from 'cookies.txt',
    located in the same directory as this script

    Returns:
        dict: each key-value pair corresponds to a cookie.
    """
    token = ''
    try:
        with open(absolute_path('cookies.txt'), 'r') as file:
            for line in file:
                if 'LEETCODE_SESSION' in line:
                    items = line.strip().split('\t')
                    token = items[-1]  # token value is last item

    except FileNotFoundError:
        print('Could not find cookies.txt')

    return {'LEETCODE_SESSION': token}
