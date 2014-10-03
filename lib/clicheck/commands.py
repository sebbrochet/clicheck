#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

def run_command(*popenargs, **kwargs):
    try:
        process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
        stdoutdata, stderrdata = process.communicate()
    except OSError, e:
        stdoutdata = ""
        stderrdata = "Command to launch not found!"
    
    return stdoutdata, stderrdata

def check_test(test):
    def check_files_exist(filename_list):
        is_ok = True
        missing_files = []
        import os
        for filename in filename_list:
             if not os.path.exists(filename):
                 is_ok = False
                 missing_files.append(filename) 
        return is_ok, missing_files 

    is_ok_stdout = True
    missing_stdout_files = []
    stdout = test.get("stdout")
    if type(stdout) is list:
        is_ok_stdout, missing_stdout_files = check_files_exist(stdout)

    is_ok_stderr = True
    missing_stderr_files = []
    stderr = test.get("stderr")
    if type(stderr) is list:
        is_ok_stderr, missing_stderr_files = check_files_exist(stderr) 

    command = test.get("command", "")
    wait = test.get("wait", 0)

    is_test_ok = command and type(wait) is int and wait >= 0 and is_ok_stdout and is_ok_stderr

    missing_reference_files = []
    missing_reference_files.extend(missing_stdout_files)
    missing_reference_files.extend(missing_stderr_files)

    return is_test_ok, command, wait, missing_reference_files


def run_test(test):
    is_test_run_ok = True

    import os

    stdout = test.get("stdout", "")
    stderr = test.get("stderr", "")
    command_with_args = test.get("command")

    stdout_reference = []

    if type(stdout) is list:
       for filename in stdout:
           with open (filename, "r") as myfile:
               content = myfile.read()
               stdout_reference.append(content)
    elif type(stdout) is str:
        stdout_reference.append(stdout)
    else:
        assert(False)

    stderr_reference = []

    if type(stderr) is list:
       for filename in stderr:
           with open (filename, "r") as myfile:
               content = myfile.read()
               stderr_reference.append(content)
    elif type(stderr) is str:
        stderr_reference.append(stderr)
    else:
        assert(False)

    command_stdout = ""
    command_stderr = ""

    try:
        command_as_list = [x.strip() for x in command_with_args.split(" ") if x.strip()]
        command_stdout, command_stderr = run_command(command_as_list)
        is_test_run_ok = command_stdout in stdout_reference and command_stderr in stderr_reference
    except subprocess.CalledProcessError, e:
       is_test_run_ok = False
       command_stderr = "Exception %s" % e

    return is_test_run_ok, command_stdout, stdout_reference, command_stderr, stderr_reference

def get_tests(scope, test):
    tests = []
    
    if test:
        tests.append(test)

    if scope:
        f = file(scope, "r")
        lines = f.read().split('\n')
        for line in lines:
            if line.startswith('#'):
                continue
            
            value = line.strip()

            if value:
                tests.append(value)

    return tests

def load_test_suite(args):
    tests = get_tests(args.scope, args.test)

    import yaml

    is_ok = True
    test_suite = []
    error = ""
    filename = args.suite

    f = file(filename, "r")
    try:
        obj = yaml.load(f)

        if not type(obj) is list:
            error = "Test suite configuration should be a list of test"
            is_ok = False
        else:
            for test in obj:
                if tests:
                    test_name = test.get('name')
                    if test_name and test_name in tests:
                        test_suite.append(test)
                else:
                    test_suite.append(test)
                     
    except Exception, e:
        error = "Error while interpreting test suite configuration: %s\nException: %s" % (filename, e)
        is_ok = False

    f.close()

    return is_ok, test_suite, error


def run_test_suite(args):
    is_ok = check_test_suite(args)

    if not is_ok:
       return is_ok

    import time

    is_yaml_ok, test_suite, error = load_test_suite(args)

    print "%d tests to be done" % len(test_suite)
    print "Starting tests..."

    for test in test_suite:
        test_name = test.get("name") or test.get("command")
        display = "%s :" % test_name 
        print display,

        import sys
        sys.stdout.flush()

        is_test_run_ok, command_stdout, stdout_reference, command_stderr, stderr_reference = run_test(test)

        command_with_args = test.get("command")

        if is_test_run_ok:
            print "OK" 
        else:
            print "NOK"
            if not command_stdout in stdout_reference: 
                print "STDOUT is:"
                print command_stdout
                print 80*"-"
                print "Reference is:"
                print stdout_reference
            if not command_stderr in stderr_reference:
                print "STDERR is:"
                print command_stderr
                print 80*"-"
                print "Reference is:"
                print stderr_reference

        wait = test.get("wait", 0) or args.wait

        if wait:
            print "Waiting %d seconds..." % wait
            time.sleep(wait)

def check_test_suite(args):
    is_yaml_ok, test_suite, error = load_test_suite(args)

    is_test_suite_ok = True
    errors = []

    if is_yaml_ok:
        for test in test_suite:
            is_test_ok, command, wait, missing_reference_files_for_test  = check_test(test)

            if not is_test_ok:
                is_test_suite_ok = False

                if not command:
                    test_name = test.get("name") or test.get("command") 
                    error = "Missing 'command' parameter in test: %s" % test_name
                elif not type(wait) is int or (type(wait) is int and wait < 0):
                    test_name = test.get("name") or test.get("command")
                    error = "wait parameter should be a positive number in test: %s" % test_name 
                else:
                    error = "Missing reference files:\n%s" % "\n".join(missing_reference_files_for_test)

                errors.append(error)
    else:
        errors.append(error)

    is_ok = is_yaml_ok and is_test_suite_ok

    if is_ok:
        print "%d tests found" % len(test_suite)
        print "Test suite configuration OK"
    else:
        if is_yaml_ok:
            print "%d tests found" % len(test_suite)
        print "Error: test suite configuration not OK"
        print "%s" % "\n".join(errors)

    return is_ok
