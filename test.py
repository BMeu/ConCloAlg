#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    ConCloAlg - Tests
    ~~~~~~~~~~~~~~~~~

    Runs all tests found in the current directory and all its subdirectories.
    all files ending with '_test.py' are considered tests. Run
        ./test.py
    to see the test results and generate a coverage report.
"""

from coverage import coverage
import os
import unittest

# Record a coverage report for all files.
cov = coverage(branch = True, source = ['.'], include = ['./*/*.py'],
               omit = ['tests.py', '*_test.py'])
cov.start()

# noinspection PyBroadException
try:
    # Starting from the current directory, all files ending with '_test.py' are
    # considered test files and therefore evaluated.
    tests = unittest.defaultTestLoader.discover('.', '*_test.py')
    test_runner = unittest.TextTestRunner(verbosity = 2)
    test_runner.run(tests)
except:
    # If exceptions were not caught and passed the coverage report could not be
    # generated.
    pass

# Stop recording the coverage report and save it.
cov.stop()
cov.save()

# Print the report.
print('\n\nCoverage Report:\n')
cov.report()

# Save the report as HTML.
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
report_path = 'htmlcov'
cov.html_report(directory = report_path)
print('HTML version: ' + os.path.join(basedir, report_path + '/index.html'))

# Delete the original report.
cov.erase()
