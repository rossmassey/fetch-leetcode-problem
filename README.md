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

## Usage

#### Installing
1. Install package from Python Package Index (PyPI)
2. Use `import fetch_leetcode_problem` or `from fetch_leetcode_problem import ...`

   
#### API

- **get_problem(num: int) -> dict | None**
  - query leetcode GraphQL API to return problem info for `num`
- **update_problem_listing()**
  - creates lookup table from leetcode REST API all-problem listing, indexed  by `num`
  - `slug` needed for problem info
  - `question_id` (can be separate from `num`) needed for synced code 
- **count_problems() -> int**
  - returns count in local db
- **load_cookie(cookie_path: str = None)**
  - loads cookie to be used in synced code query
  
   
#### Example
    In [1]: import fetch_leetcode_problem as lc
    
    In [2]: lc.count_problems()
    Out[2]: 0
    
    In [3]: lc.update_problem_listing()
    
    In [4]: lc.count_problems()
    Out[4]: 3018
    
    In [5]: lc.load_cookie('cookies.txt')
    
    In [6]: lc.get_problem(1)
    Out[6]:
    {'num': '1',
     'title': 'Two Sum',
     'slug': 'two-sum',
     'difficulty': 'Easy',
     'description': 'Given an array of integers ``nums``\xa0and an integer ``target``, return *indices of the two numbers such that they add up to ``target``*.\n\nYou may assume that each input would have ***exactly* one solution**, and you may not use the *same* element twice.\n\nYou can return the answer in any order.\n\n',
     'examples': [{'input': 'nums = [2,7,11,15], target = 9',
       'output': '[0,1]',
       'img': None,
       'explanation': ' Because nums[0] + nums[1] == 9, we return [0, 1].\n'},
      {'input': 'nums = [3,2,4], target = 6',
       'output': '[1,2]',
       'img': None,
       'explanation': None},
      {'input': 'nums = [3,3], target = 6',
       'output': '[0,1]',
       'img': None,
       'explanation': None}],
     'constraints': ['``2 <= nums.length <= 10^4``',
      '``-10^9 <= nums[i] <= 10^9``',
      '``-10^9 <= target <= 10^9``',
      '**Only one valid answer exists.**'],
     'code_snippet': 'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        ',
     'code': 'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        \n        complements = {}\n        \n        for i, num in enumerate(nums):\n            complements[num] = i\n            \n        for i, num in enumerate(nums):\n            if (target - num) in complements and complements[target-num] != i:\n                return [i, complements[target-num]]',
     'func': {'name': 'twoSum',
      'params': ['self', 'nums', 'target'],
      'param_types': [None, 'List[int]', 'int'],
      'rtype': 'List[int]'}}

Can also run the main module like:

`python -m fetch_leetcode_problem.main 1`

- **u:** update the problem index
- **c:** count number of problems
- `<num>`: get problem info for `<num>`

#### cookies.txt
Export a Netscape HTTP Cookie File for `leetcode.com` (see browser extensions).

Alternatively, create a file with the text `LEETCODE_SESSION`, a tab (`\t`), 
and your session token. This can be found in the Network tab in developer tools, 
under Request Cookies, for requests to `leetcode.com`.

Save as `cookies.txt` in the `src/fetch_leetcode_problem/` directory, or supply
the `load_cookie` function with its relative location.

##### copy cookies.txt to site packages
Run these commands from location of `cookies.txt` for it to remain available

```
package_location=$(pip show rossmassey.fetch-leetcode-problem | grep Location)
package_path=$(echo package_location | cut -d ' ' -f2)
cp cookies.txt package_path
```

#### Deleting database
1. Find site packages location with `pip show rossmassey.fetch-leetcode-problem`
2. Find `fetch_leetcode_problem` directory under site packages
3. Delete `problems.db`

## Building & Publishing to PyPI
Assume `.pypirc` configured in user home directory wih PyPI credentials
```
rm -rf dist
python3 -m build
python3 -m twine upload --repository pypi dist/*
```
