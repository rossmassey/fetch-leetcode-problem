from problem_info import get_problem, update_problem_listing
import sys


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        if argument == 'u':
            update_problem_listing()
        else:
            try:
                num = int(argument)
                info = get_problem(num)
                for key, value in info.items():
                    print(f'{key:<{15}} {value}')

            except ValueError:
                print(f'Invalid argument: {argument}')
                help()
    else:
        print('No arguments provided.')
        help()


def help():
    print('Usage:')
    print('')
    print('main.py u        -- update the problem index')
    print('main.py <num>    -- get problem info for <num>')


if __name__ == '__main__':
    main()
