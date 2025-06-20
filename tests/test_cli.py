"""Tests for the stacksurvey CLI."""

import os
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
import sys

from stacksurvey.__main__ import main


class TestCLI(unittest.TestCase):
    """Test case for CLI functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary Excel files with test data
        self.test_files = []
        
        # Create test data for file 1
        df1 = pd.DataFrame({
            'Respondent': [1, 2, 3],
            'Country': ['USA', 'Canada', 'UK'],
            'EdLevel': ['Bachelor', 'Master', 'PhD'],
            'LanguageWorkedWith': ['Python;JavaScript', 'Python;Java', 'C++;Java']
        })
        
        # Save test data to temporary Excel file
        fd, path = tempfile.mkstemp(suffix='.xlsx')
        os.close(fd)
        df1.to_excel(path, index=False)
        self.test_files.append(path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary Excel files
        for path in self.test_files:
            if os.path.exists(path):
                os.unlink(path)
    
    @patch('sys.stdout')
    def test_load_command(self, mock_stdout):
        """Test the load command."""
        exit_code = main(['load'] + self.test_files)
        self.assertEqual(exit_code, 0)
    
    @patch('sys.stdout')
    def test_list_questions_command(self, mock_stdout):
        """Test the list-questions command."""
        # First, load the data
        main(['load'] + self.test_files)
        
        # Then list the questions
        exit_code = main(['list-questions'])
        self.assertEqual(exit_code, 0)
    
    @patch('sys.stdout')
    def test_search_command(self, mock_stdout):
        """Test the search command."""
        # First, load the data
        main(['load'] + self.test_files)
        
        # Then search for questions
        exit_code = main(['search', '--question', 'Level'])
        self.assertEqual(exit_code, 0)
        
        # Then search for options
        exit_code = main(['search', '--option', 'Python'])
        self.assertEqual(exit_code, 0)
    
    @patch('sys.stdout')
    def test_filter_command(self, mock_stdout):
        """Test the filter command."""
        # First, load the data
        main(['load'] + self.test_files)
        
        # Then filter respondents
        exit_code = main(['filter', '--question', 'Country', '--option', 'USA'])
        self.assertEqual(exit_code, 0)
        
        # Then filter respondents with output
        fd, output_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        try:
            exit_code = main(['filter', '--question', 'LanguageWorkedWith', 
                              '--option', 'Python', '--output', output_path])
            self.assertEqual(exit_code, 0)
            
            # Check that the output file exists and contains data
            self.assertTrue(os.path.exists(output_path))
            df = pd.read_csv(output_path)
            self.assertGreater(len(df), 0)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    @patch('sys.stdout')
    def test_distribution_command(self, mock_stdout):
        """Test the distribution command."""
        # First, load the data
        main(['load'] + self.test_files)
        
        # Then compute distribution for single-choice question
        exit_code = main(['distribution', '--question', 'EdLevel'])
        self.assertEqual(exit_code, 0)
        
        # Then compute distribution for multiple-choice question
        exit_code = main(['distribution', '--question', 'LanguageWorkedWith'])
        self.assertEqual(exit_code, 0)


if __name__ == '__main__':
    unittest.main()
