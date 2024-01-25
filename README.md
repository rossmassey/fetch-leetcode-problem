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
2. Import with:
    ```python
    import fetch_leetcode_problem
    ```
3. Use as:
    ```python
    # create/update .db file on disk (only need to do once)
    fetch_leetcode_problem.update_problem_listing()
    
    # cookies.txt path for synced code (assume package src dir if not given)
    fetch_leetcode_problem.load_cookie('cookies.txt')
    
    fetch_leetcode_problem.get_problem(1)
    ```

Can also run the main module like:

`python -m src.fetch_leetcode_problem.main 1`

- **u:** update the problem index
- **c:** count number of problems
- `<num>`: get problem info for `<num>`

#### API

- **get_problems(num: int) -> dict | None**
  - query leetcode GraphQL API to return problem info
- **update_problem_listing()**
  - creates lookup table from leetcode REST API all-problem listing, indexed  by `num`
  - `slug` needed for problem info
  - `question_id` (can be separate from `num`) needed for synced code 
- **count_problems() -> int**
  - returns count in local db
- **load_cookie(cookie_path: str = None)**
  - loads cookie to be used in synced code query

#### cookies.txt
Export a Netscape HTTP Cookie File for `leetcode.com` (see browser extensions).

Alternatively, create a file with the text `LEETCODE_SESSION`, a tab (`\t`), 
and your session token. This can be found in the Network tab in developer tools, 
under Request Cookies, for requests to `leetcode.com`.

Save as `cookies.txt` in the `src/fetch_leetcode_problem/` directory, or supply
the `load_cookie` function with its relative location.

## Building & Publishing
Assume `.pypirc` configured in user home directory wih PyPI credentials
```
rm -rf dist
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```