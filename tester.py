#!/usr/bin/python3

import os
import sys
from test_names import get_test_names
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--dir', default='.')
parser.add_argument('-o', '--exec', default='a.out')
parser.add_argument('-i', '--src', default='main.cpp')
parser.add_argument('-t', '--testdir', default='tests')
parser.add_argument('-C', '--compiler', default='g++')
parser.add_argument('-f', '--flags', default='-std=gnu++17 -O2 -static')
parser.add_argument('-s', '--silent', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('--compile', default=True, action=argparse.BooleanOptionalAction)
parser.add_argument('-w', '--warnings', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('--override', default=False, action=argparse.BooleanOptionalAction)

args = vars(parser.parse_args())

exec_path = os.path.join(args['dir'], args['exec'])
warnings = '-Wall -Wextra -Wshadow' if args['warnings'] else '-w'
compile_command = f"{args['compiler']} {args['flags']} {warnings} -o {args['exec']} {args['src']}"

cat_cmd = 'type' if os.name == 'nt' else 'cat'

if args['compile']:
    if os.path.isfile(exec_path):
        os.remove(exec_path)

    print(f'Compiling with: {compile_command}\n')

    os.popen(compile_command).read()

    print()

    if not os.path.isfile(exec_path):
        exit(1)
elif not os.path.isfile(exec_path):
    print('Cant find executable file')
    exit(1)

passed = 0
failed = 0

for in_name, out_name in get_test_names(args['testdir']):
    test_path = os.path.join(args['testdir'], in_name)
    command = f"{cat_cmd} {test_path} | {exec_path}"

    result = os.popen(command).read().strip()

    if args['override']:
        out_name = os.path.splitext(in_name)[0] + '.out'

        print(f'Saving result of {in_name} to {out_name}')

        with open(os.path.join(args['testdir'], out_name), 'w') as out_file:
            out_file.write(result)
        continue

    if out_name:
        with open(os.path.join(args['testdir'], out_name)) as out_file:
            expected_output = out_file.read().strip()

            if result == expected_output:
                passed += 1
                print(f'Test {in_name} PASSED')
            else:
                failed += 1
                print(f'Test {in_name} FAILED')

                if args['silent']:
                    print('Result:')
                else:
                    print('Expected:')
                    print(expected_output)
                    print('Got:')

                print(result)
    else:
        print(f'Test {in_name}')
        print('Result:')
        print(result)

    print('------------------------------------------')

if not args['silent'] and not args['override']:
    print(f'Passed: {passed}')
    print(f'Failed: {failed}')
    print(f'Total: {passed + failed}')
