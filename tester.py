#!/usr/bin/python3

import os
import sys
from test_names import get_test_names
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dir', default='.')
parser.add_argument('--exec', default='a.out')
parser.add_argument('--src', default='main.cpp')
parser.add_argument('--testdir', default='tests')

args = vars(parser.parse_args())

exec_path = os.path.join(args['dir'], args['exec'])
compile_command = f"g++ {args['src']} -o {args['exec']}"

cat_cmd = 'type' if os.name == 'nt' else 'cat'

if os.path.isfile(exec_path):
    os.remove(exec_path)

os.popen(compile_command).read()

if not os.path.isfile(exec_path):
    exit(1)

passed = 0
failed = 0

for in_name, out_name in get_test_names(args['testdir']):
    test_path = os.path.join(args['testdir'], in_name)
    command = f"{cat_cmd} {test_path} | {exec_path}"

    result = os.popen(command).read().strip()

    if out_name:
        with open(os.path.join(args['testdir'], out_name)) as out_file:
            expected_output = out_file.read().strip()

            if result == expected_output:
                passed += 1
                print(f'Test {in_name} PASSED')
            else:
                failed += 1
                print(f'Test {in_name} FAILED')
                print('Expected:')
                print(expected_output)
                print('Got:')
                print(result)
    else:
        print(f'Test {in_name}')
        print('Result:')
        print(result)

    print('------------------------------------------')
print(f'Passed: {passed}')
print(f'Failed: {failed}')
print(f'Total: {passed + failed}')
