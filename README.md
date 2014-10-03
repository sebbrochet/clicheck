clicheck
========

CLI acceptance testing based on output comparison

Requirements
* linux box
* Python 2.6 or higher
* [argparse](https://docs.python.org/3/library/argparse.html) library
* [pyyaml](http://pyyaml.org/) library

Installation:
-------------
* Clone repository    
`git clone https://github.com/sebbrochet/clicheck.git`
* cd into project directory    
`cd clicheck`
* Install requirements with pip    
`pip install -r requirements.txt`
* Install clicheck binary    
`python setup.py install`

Usage:
------

```
usage: clicheck [-h] [-s SCOPE] [-t TEST] [-u SUITE] [-w WAIT] [-c CONFIG]
                [-v]
                command

CLI acceptance testing based on output comparison.

positional arguments:
  command               Command to execute (check, run)

optional arguments:
  -h, --help            show this help message and exit
  -s SCOPE, --scope SCOPE
                        Limit command to act on scope defined in a file
  -t TEST, --test TEST  Specify the name of a specific test to test
  -u SUITE, --suite SUITE
                        Specify the name of the test suite to test
  -w WAIT, --wait WAIT  Time to wait in seconds between tests (default is 0)
  -c CONFIG, --config CONFIG
                        Configuration file to use
  -v, --version         Print program version and exit.
```

A test suite is described as a list of test defined in YAML format.    
You may have a look on [clicheck own acceptance tests](https://github.com/sebbrochet/clicheck/blob/master/tests/clicheck_test_suite.yaml) made using clicheck (now that's meta!).    

`config` format is one argument by line (i.e argname=value), argument names are the same ones than the CLI (scope, test, suite, wait).
A line starting with a `#` is considered as comment and won't be interpreted.
Don't put quotes between argument values

TEST DEFINITION:
------
<table>
  <tr>
    <th>Parameter</th><th>required</th><th>default</th><th>type</th><th>comments</th>
  </tr>
  <tr>
    <td>name</td><td>no</td><td>""</td><td>string</td><td>name of the test for documentation purpose or use with --scope or --test options</td>
  </tr>
  <tr>
    <td>command</td><td>yes</td><td></td><td>string</td><td>full command with arguments to execute</td>
  </tr>
  <tr>
    <td>stdout</td><td>no</td><td>""</td><td>string or list of strings</td><td>Text pattern or list of filenames with text patterns for comparison against STDOUT of command</td>
  </tr>
  <tr>
    <td>stderr</td><td>no</td><td>""</td><td>string or list of strings</td><td>string or list of strings</td><td>Text pattern or list of filenames with text patterns for comparison against STDERR of command</td>
  </tr>
  <tr>
    <td>wait</td><td>no</td><td>0</td><td>positive int</td><td>Number of seconds to wait after test execution</td>
  </tr>
</table>

TESTS:
------
* `clicheck -u tests/clicheck_test_suite.yaml run`
