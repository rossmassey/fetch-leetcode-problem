# Fetch Problem

Gets a dictionary with information about a leetcode problem, formatted in `rst`
- num 
- title
- slug
- difficulty
- description
- list of examples
- list of constraints
- initial code snippet
- synced user code* 
- function information**
  - name
  - list of params
  - list of param types
  - return type

    
*: requires `cookies.txt`

**: assume implementing only one function for now

## API Overview

#### problem_info.py

- **get_problems(num: int) -> dict | None**
  - query leetcode GraphQL API to return problem info
- **update_problem_listing()**
  - creates lookup table from leetcode REST API all-problem listing, indexed  by `num`
  - `slug` needed for problem info
  - `question_id` (can be separate from `num`) needed for synced code 
- **count_problems() -> int**
  - returns count in local db

## Installing
1. Install package from PyPi
2. Add to your code:
```python3
import fetch_leetcode_problem
```
3. Use as:
```python3
# only need to do once to create .db file
fetch_leetcode_problem.update_problem_listing()

fetch_leetcode_problem.get_problem(1)
```

## cookies.txt
Export a Netscape HTTP Cookie File for `leetcode.com` (see browser extensions).

Alternatively, create a file with the text `LEETCODE_SESSION`, a tab (`\t`), 
and your session token. This can be found in the Network tab in developer tools, 
under Request Cookies, for requests to `leetcode.com`.

Save as `cookies.txt` in the `src/fetch_leetcode_problem/` directory.

## Examples
#### main.py
Usage:
- `main.py u`: update the problem index
- `main.py c`: count number of problems
- `main.py <num>`: get problem info for `<num>`

```
❯ python -m src.fetch_leetcode_problem.main c
0 problems found in database

❯ python -m src.fetch_leetcode_problem.main u
Updating problem listing...
Updated

❯ python -m src.fetch_leetcode_problem.main c
3018 problems found in database

❯ python -m src.fetch_leetcode_problem.main 42
{'num': '42', 'title': 'Trapping Rain Water', 'slug': 'trapping-rain-water', 'difficulty': 'Hard', 'description': 'Given ``n`` non-negative integers representing an elevation map where the width of each bar is ``1``, compute how much water it can trap after raining.\n\n', 'examples': [{'n': 1, 'input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]', 'output': '6', 'img': None, 'explanation': ' The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.\n'}, {'n': 2, 'input': 'height = [4,2,0,3,2,5]', 'output': '9', 'img': None, 'explanation': None}], 'constraints': ['``n == height.length``', '``1 <= n <= 2 * 10^4``', '``0 <= height[i] <= 10^5``'], 'code_snippet': 'class Solution:\n    def trap(self, height: List[int]) -> int:\n        ', 'code': None, 'func': {'name': 'trap', 'params': ['self', 'height'], 'param_types': [None, 'List[int]'], 'rtype': 'int'}}
```

#### Interactive
```
❯ ipython --no-banner -i problem_info.py 

In [1]: count_problems()
Out[1]: 0

In [2]: %time update_problem_listing()
CPU times: user 286 ms, sys: 1.58 s, total: 1.87 s
Wall time: 2.98 s

In [3]: %time count_problems()
CPU times: user 1.53 ms, sys: 6.58 ms, total: 8.11 ms
Wall time: 27.2 ms
Out[3]: 3018

In [4]: %time get_problem(42)
CPU times: user 57.4 ms, sys: 10.1 ms, total: 67.5 ms
Wall time: 353 ms
Out[4]: 
{'num': '42',
 'title': 'Trapping Rain Water',
 'slug': 'trapping-rain-water',
 'difficulty': 'Hard',
 'description': 'Given ``n`` non-negative integers representing an elevation map where the width of each bar is ``1``, compute how much water it can trap after raining.\n\n',
 'examples': [{'n': 1,
   'input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]',
   'output': '6',
   'img': None,
   'explanation': ' The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.\n'},
  {'n': 2,
   'input': 'height = [4,2,0,3,2,5]',
   'output': '9',
   'img': None,
   'explanation': None}],
 'constraints': ['``n == height.length``',
  '``1 <= n <= 2 * 10^4``',
  '``0 <= height[i] <= 10^5``'],
 'code_snippet': 'class Solution:\n    def trap(self, height: List[int]) -> int:\n        ',
 'code': None,
 'func': {'name': 'trap',
  'params': ['self', 'height'],
  'param_types': [None, 'List[int]'],
  'rtype': 'int'}}

```
