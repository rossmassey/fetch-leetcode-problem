from util import absolute_path


def get_leetcode_session_cookie(cookie_file: str) -> dict:
    token = ''
    try:
        with open(absolute_path(cookie_file), 'r') as file:
            for line in file:
                if 'LEETCODE_SESSION' in line:
                    items = line.strip().split('\t')
                    token = items[-1]  # token value is last item

    except FileNotFoundError:
        print(f'Could not find {cookie_file}')
    
    if not token:
        print(f'LEETCODE_SESSION token not found at {cookie_file}')

    return {'LEETCODE_SESSION': token}
