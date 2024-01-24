from problem_info import get_problem, update_problem_listing
import sys


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        # fetch all the leetcode problems and store in local sqlite
        if argument.lower() == 'u':
            print('Updating problem listing...')
            update_problem_listing()
            print('Updated')

        else:
            try:
                # fetch info for single problem
                info = get_problem(int(argument))

                if info is None:
                    print(f'No problem info returned')
                else:
                    print_info(info)

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

    print('\nraw:\n', info)

def print_example(example):
    print(f"Example {example['n']}")
    print(f"\tInput: {example['input']}")
    print(f"\tOutput: {example['output']}")
    print(f"\tImg: {example['img']}")
    print(f"\tExplanation: {example['explanation']}")


if __name__ == '__main__':
    main()
