#!/usr/bin/env python3
"""Test runner for the Life Simulation project."""

import unittest
import sys


def run_tests():
    """Discover and run all tests in the project."""
    # Initialize the test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in the tests directory
    test_suite = loader.discover('tests')
    
    # Initialize the test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(test_suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests()) 