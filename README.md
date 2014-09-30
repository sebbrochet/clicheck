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
You may have a look on clicheck own acceptance tests made using clicheck (now that's meta!).    

IMPLEMENTED:
------
* check and run command
* --suite option

TODO:
------
* Implement --scope option
* Implement --test option
* Implement --wait option (or add addionnal wait parameter in test configuration?)
* Implement --config option
