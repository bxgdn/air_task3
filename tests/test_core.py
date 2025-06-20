"""Tests for the stacksurvey.core module."""

import os
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np

from stacksurvey.core import (
    load_data,
    list_questions,
    search,
    filter_respondents,
    compute_distribution,
    _get_question_type
)


class TestCore(unittest.TestCase):
    """Test case for core functionality."""
    
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
        
        # Create test data for file 2
        df2 = pd.DataFrame({
            'Respondent': [4, 5],
            'Country': ['Germany', 'France'],
            'EdLevel': ['Bachelor', 'Master'],
            'LanguageWorkedWith': ['Python;C#', 'JavaScript;TypeScript']
        })
        
        # Create test data for file 3
        df3 = pd.DataFrame({
            'Respondent': [6],
            'Country': ['Japan'],
            'EdLevel': ['PhD'],
            'LanguageWorkedWith': ['Java;Kotlin']
        })
        
        # Save test data to temporary Excel files
        for i, df in enumerate([df1, df2, df3]):
            fd, path = tempfile.mkstemp(suffix='.xlsx')
            os.close(fd)
            df.to_excel(path, index=False)
            self.test_files.append(path)
        
        # Load test data
        self.test_data = load_data(self.test_files)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary Excel files
        for path in self.test_files:
            if os.path.exists(path):
                os.unlink(path)
    
    def test_load_data(self):
        """Test loading and integrating Excel files."""
        # Check that the combined data has the correct number of rows
        self.assertEqual(len(self.test_data), 6)
        
        # Check that all columns are present
        expected_columns = ['Respondent', 'Country', 'EdLevel', 'LanguageWorkedWith']
        for col in expected_columns:
            self.assertIn(col, self.test_data.columns)
    
    def test_get_question_type(self):
        """Test determining question type."""
        # Test single-choice question
        self.assertEqual(_get_question_type(self.test_data, 'Country'), 'SC')
        
        # Test multiple-choice question
        self.assertEqual(_get_question_type(self.test_data, 'LanguageWorkedWith'), 'MC')
    
    def test_list_questions(self):
        """Test listing survey questions."""
        questions = list_questions()
        
        # Check that all expected questions are present
        expected_questions = ['Respondent', 'Country', 'EdLevel', 'LanguageWorkedWith']
        for q in expected_questions:
            self.assertIn(q, questions)
        
        # Check that question types are correct
        self.assertEqual(questions['Country'], 'SC')
        self.assertEqual(questions['LanguageWorkedWith'], 'MC')
    
    def test_search_question(self):
        """Test searching for questions."""
        results = search(question='Level')
        
        # Check that 'EdLevel' is in the results
        self.assertIn('EdLevel', results['questions'])
    
    def test_search_option(self):
        """Test searching for options."""
        results = search(option='Python')
        
        # Check that 'LanguageWorkedWith' and 'Python' are in the results
        found = False
        for q_id, option, _ in results['options']:
            if q_id == 'LanguageWorkedWith' and 'Python' in option:
                found = True
                break
        
        self.assertTrue(found)
    
    def test_filter_respondents_single_choice(self):
        """Test filtering respondents by single-choice question."""
        filtered = filter_respondents('Country', 'USA')
        
        # Check that there is exactly 1 respondent from USA
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]['Country'], 'USA')
    
    def test_filter_respondents_multiple_choice(self):
        """Test filtering respondents by multiple-choice question."""
        filtered = filter_respondents('LanguageWorkedWith', 'Python')
        
        # Check that there are exactly 3 respondents who use Python
        self.assertEqual(len(filtered), 3)
    
    def test_compute_distribution_single_choice(self):
        """Test computing distribution for single-choice question."""
        distribution = compute_distribution('EdLevel')
        
        # Check that the distribution has all expected options
        expected_options = ['Bachelor', 'Master', 'PhD']
        for option in expected_options:
            self.assertIn(option, distribution)
        
        # Check that percentages sum to approximately 1
        self.assertAlmostEqual(sum(distribution.values()), 1.0, places=5)
    
    def test_compute_distribution_multiple_choice(self):
        """Test computing distribution for multiple-choice question."""
        distribution = compute_distribution('LanguageWorkedWith')
        
        # Check that the distribution has all expected options
        expected_options = ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'TypeScript', 'Kotlin']
        for option in expected_options:
            self.assertIn(option, distribution)
        
        # Check Python percentage - should be 3 out of 12 total selections
        python_count = sum(1 for row in self.test_data['LanguageWorkedWith'] 
                         if isinstance(row, str) and 'Python' in row.split(';'))
        expected_python_percentage = python_count / 12  # Total 12 selections across all respondents
        self.assertAlmostEqual(distribution['Python'], expected_python_percentage, places=5)


if __name__ == '__main__':
    unittest.main()
