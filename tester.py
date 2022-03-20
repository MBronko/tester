#!/usr/bin/python3

import os
import sys
from test_names import get_test_names
import argparse
from subprocess import Popen, PIPE

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

if args['compile']:
    if os.path.isfile(exec_path):
        os.remove(exec_path)

    print(f'Compiling with: {compile_command}\n')

    p = Popen(compile_command, shell=True)
    p.wait()

    if p.returncode:
        exit(1)
elif not os.path.isfile(exec_path):
    print('Cant find executable file')
    exit(1)

passed = 0
failed = 0

for in_name, out_name in get_test_names(args['testdir']):
    test_path = os.path.join(args['testdir'], in_name)

    with open(test_path, 'rb') as in_file:
        p = Popen(exec_path, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate(input=in_file.read())

    error = stderr.decode('utf-8')
    output = stdout.decode('utf-8').strip()
    returncode = p.returncode

    if args['override'] and not returncode:
        out_name = os.path.splitext(in_name)[0] + '.out'

        print(f'Saving result of {in_name} to {out_name}')

        with open(os.path.join(args['testdir'], out_name), 'wb') as out_file:
            out_file.write(stdout)
        continue

    test_case_header = f'Test {in_name}'
    test_case_msg = ''

    if out_name:
        with open(os.path.join(args['testdir'], out_name), 'r') as out_file:
            expected_output = out_file.read().strip()

            if output == expected_output:
                passed += 1
                test_case_header += ' PASSED'
            else:
                failed += 1
                test_case_header += ' FAILED\n'

                if args['silent']:
                    test_case_msg = f'Result:\n{output}'
                else:
                    test_case_msg = f'Expected:\n{expected_output}\nGot:\n{output}'
    else:
        test_case_header += '\n'
        test_case_msg = f'Result:\n{output}'

    if error:
        error = f'\nError: {error}\n'

    print(test_case_header + error + test_case_msg)
    print('------------------------------------------')

if not args['silent'] and not args['override']:
    print(f'Passed: {passed}')
    print(f'Failed: {failed}')
    print(f'Total: {passed + failed}')
