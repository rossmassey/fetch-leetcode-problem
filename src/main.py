import problem_info
import sys


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        # fetch all the leetcode problems and store in local sqlite
        if argument.lower() == 'u':
            print('Updating problem listing...')
            problem_info.update_problem_listing()
            print('Updated')

        # count problems stored in index
        elif argument.lower() == 'c':
            count = problem_info.count_problems()
            print(f'{count} problems found in database')

        else:
            try:
                # fetch info for single problem
                info = problem_info.get_problem(int(argument))

                if info is None:
                    print(f'No problem info returned')
                else:
                    print(info)

            except ValueError:
                print(f'Invalid argument: {argument}')
                print_help()
    else:
        print('No arguments provided.')
        print_help()


def print_help():
    print('Usage:')
    print('')
    print('main.py u      -- update the problem index')
    print('main.py c      -- count number of problems')
    print('main.py <num>  -- get problem info for <num>')


def print_info(info):
    title = f"{info['num']} - {info['title']} - {info['difficulty']}"
    print(title)
    print('=' * len(title))
    print(info['description'])

    print('Examples:')
    for example in info['examples']:
        print_example(example)

    print('Constraints:')
    for constraint in info['constraints']:
        print(f'- {constraint}')

    print('Initial code:')
    print(info['code_snippet'])

    print('Synced code:')
    print(info['code'])

    print('Func info:')
    print(info['func'])

def print_example(example):
    print(f"Example {example['n']}")
    print(f"\tInput: {example['input']}")
    print(f"\tOutput: {example['output']}")
    print(f"\tImg: {example['img']}")
    print(f"\tExplanation: {example['explanation']}")


if __name__ == '__main__':
    main()
