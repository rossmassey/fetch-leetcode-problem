"""
Main entry point for the program.

Usage:

    * ``u``      -- update the problem index
    * ``c``      -- count number of problems
    * ``<num>``  -- get problem info for <num>

"""
import sys

from . import problem_info


def main():
    """
    Main entry point
    """
    problem_info.load_cookie()

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


if __name__ == '__main__':
    main()
