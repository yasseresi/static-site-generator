#!/usr/bin/env python3
"""Run just the failing test"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import unittest
from test_markdown_parser import TestSplitNodesDelimiter

if __name__ == "__main__":
    # Create a test suite with just the failing test
    suite = unittest.TestSuite()
    suite.addTest(TestSplitNodesDelimiter('test_empty_delimited_text'))
    
    # Run the test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
