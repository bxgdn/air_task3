"""
Unit tests for the StackOverflowAnalyzer class
"""

import unittest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from stackoverflow_analyzer import StackOverflowAnalyzer
from stackoverflow_analyzer.models import QuestionType


class TestStackOverflowAnalyzer(unittest.TestCase):
    """Test cases for StackOverflowAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create sample data
        self.sample_data = pd.DataFrame({
            'Age': [25, 30, 35, 28, 32],
            'Country': ['USA', 'Canada', 'UK', 'USA', 'Germany'],
            'Languages': ['Python;JavaScript', 'Java;C++', 'Python;R', 'JavaScript', 'Python;Java;C++'],
            'Salary': [70000, 80000, 65000, 75000, 85000],
            'Experience': [3, 5, 8, 4, 6]
        })
        
        # Create temporary Excel files
        self.temp_files = []
        for i in range(2):
            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            self.sample_data.to_excel(temp_file.name, index=False)
            self.temp_files.append(temp_file.name)
        
        # Initialize analyzer
        self.analyzer = StackOverflowAnalyzer(self.temp_files)
    
    def tearDown(self):
        """Clean up test fixtures"""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer.survey_data)
        self.assertIsNotNone(self.analyzer.data)
        self.assertIsNotNone(self.analyzer.questions)
        
        # Should have data from both files combined
        expected_rows = len(self.sample_data) * 2
        self.assertEqual(len(self.analyzer.data), expected_rows)
    
    def test_question_detection(self):
        """Test question type detection"""
        questions_by_name = {q.column_name: q for q in self.analyzer.questions}
        
        # Age should be detected as numeric
        self.assertEqual(questions_by_name['Age'].question_type, QuestionType.NUMERIC)
        
        # Country should be detected as single choice
        self.assertEqual(questions_by_name['Country'].question_type, QuestionType.SINGLE_CHOICE)
        
        # Languages should be detected as multiple choice (contains semicolons)
        self.assertEqual(questions_by_name['Languages'].question_type, QuestionType.MULTIPLE_CHOICE)
    
    def test_search_question(self):
        """Test question searching functionality"""
        # Search for 'age' should return Age question
        results = self.analyzer.search_question('age')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].column_name, 'Age')
        
        # Search for 'language' should return Languages question
        results = self.analyzer.search_question('language')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].column_name, 'Languages')
        
        # Search for non-existent term
        results = self.analyzer.search_question('nonexistent')
        self.assertEqual(len(results), 0)
    
    def test_search_option(self):
        """Test option searching functionality"""
        # Search for 'Python' in options
        results = self.analyzer.search_option('Python')
        self.assertGreater(len(results), 0)
        
        # Should find it in Languages question
        found_in_languages = any(q.column_name == 'Languages' for q, options in results)
        self.assertTrue(found_in_languages)
    
    def test_create_subset(self):
        """Test subset creation functionality"""
        # Create subset for USA respondents
        subset = self.analyzer.create_subset('Country', ['USA'])
        
        # Should have 4 USA respondents (2 from each file)
        self.assertEqual(len(subset), 4)
        
        # All should be from USA
        self.assertTrue(all(subset['Country'] == 'USA'))
    
    def test_create_subset_multiple_choice(self):
        """Test subset creation for multiple choice questions"""
        # Create subset for Python users
        subset = self.analyzer.create_subset('Languages', ['Python'])
        
        # Should include respondents who selected Python
        self.assertGreater(len(subset), 0)
        
        # Verify that all respondents in subset actually selected Python
        for idx, row in subset.iterrows():
            languages = str(row['Languages']).split(';')
            self.assertIn('Python', [lang.strip() for lang in languages])
    
    def test_get_answer_distribution(self):
        """Test answer distribution calculation"""
        # Test single choice question
        dist = self.analyzer.get_answer_distribution('Country')
        
        self.assertIn('distribution', dist)
        self.assertIn('percentages', dist)
        self.assertIn('total_responses', dist)
        self.assertIn('valid_responses', dist)
        
        # Should have USA with highest count
        self.assertEqual(dist['distribution']['USA'], 4)  # 2 from each file
    
    def test_get_answer_distribution_multiple_choice(self):
        """Test answer distribution for multiple choice questions"""
        dist = self.analyzer.get_answer_distribution('Languages')
        
        self.assertIn('distribution', dist)
        
        # Python should appear in multiple responses
        self.assertIn('Python', dist['distribution'])
        self.assertGreater(dist['distribution']['Python'], 1)
    
    def test_get_question_summary(self):
        """Test question summary generation"""
        summary = self.analyzer.get_question_summary()
        
        self.assertIn('SC', summary)  # Single Choice
        self.assertIn('MC', summary)  # Multiple Choice
        self.assertIn('NUMERIC', summary)  # Numeric
        
        # Should have expected counts
        self.assertGreater(summary['SC'], 0)
        self.assertGreater(summary['MC'], 0)
        self.assertGreater(summary['NUMERIC'], 0)
    
    @patch('builtins.print')
    def test_display_methods(self, mock_print):
        """Test display methods don't crash"""
        # Test display_survey_structure
        self.analyzer.display_survey_structure()
        mock_print.assert_called()
        
        mock_print.reset_mock()
        
        # Test display_search_results
        self.analyzer.display_search_results('python')
        mock_print.assert_called()
        
        mock_print.reset_mock()
        
        # Test display_answer_distribution
        self.analyzer.display_answer_distribution('Country')
        mock_print.assert_called()
        
        mock_print.reset_mock()
        
        # Test display_summary
        self.analyzer.display_summary()
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()
