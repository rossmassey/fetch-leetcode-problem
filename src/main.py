from problem_info import get, update_problem_listing
import sys


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        if argument.lower() == 'u':
            print('Updating problem listing...')
            update_problem_listing()
            print('Updated')

        else:
            try:
                num = int(argument)
                info = get(num)
                if info is None:
                    print(f'No problem info returned')
                else:
                    print_info(info)

            except ValueError:
                print(f'Invalid argument: {argument}')
                help()
    else:
        print('No arguments provided.')
        help()


def help():
    print('Usage:')
    print('')
    print('main.py u     -- update the problem index')
    print('main.py <num> -- get problem info for <num>')


def print_info(info):
    title = f'{info['num']} - {info['title']} - {info['difficulty']}'
    print(title)
    print('=' * len(title))
    print(info['description'])
    [print_example(example) for example in info['examples']]
    print('Constraints:')
    [print(f'- {constraint}') for constraint in info['constraints']]
    print('Initial code:')
    print(info['code_snippet'])
    print('Synced code:')
    print(info['code'])

    print('\nraw:\n', info)


def print_example(example):
    print(f'Example {example['n']}')
    print(f'\tInput: {example['input']}')
    print(f'\tOutput: {example['output']}')
    print(f'\tImg: {example['img']}')
    print(f'\tExplanation: {example['explanation']}')


if __name__ == '__main__':
    main()
