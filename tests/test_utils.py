"""
Unit tests for utility functions
"""

import unittest
import pandas as pd
import tempfile
import os
from stackoverflow_analyzer.utils import (
    detect_question_type, extract_question_options, 
    clean_column_name, search_questions, search_options
)
from stackoverflow_analyzer.models import Question, QuestionType


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_detect_question_type_numeric(self):
        """Test numeric question type detection"""
        numeric_data = pd.Series([1, 2, 3, 4, 5])
        qtype = detect_question_type(numeric_data, 'TestColumn')
        self.assertEqual(qtype, QuestionType.NUMERIC)
    
    def test_detect_question_type_multiple_choice(self):
        """Test multiple choice question type detection"""
        mc_data = pd.Series(['A;B', 'B;C', 'A;C', 'A'])
        qtype = detect_question_type(mc_data, 'TestColumn')
        self.assertEqual(qtype, QuestionType.MULTIPLE_CHOICE)
    
    def test_detect_question_type_single_choice(self):
        """Test single choice question type detection"""
        sc_data = pd.Series(['A', 'B', 'A', 'B', 'A'] * 10)  # Repeated values
        qtype = detect_question_type(sc_data, 'TestColumn')
        self.assertEqual(qtype, QuestionType.SINGLE_CHOICE)
    
    def test_detect_question_type_text(self):
        """Test text question type detection"""
        text_data = pd.Series(['Unique text 1', 'Unique text 2', 'Unique text 3', 'Unique text 4'])
        qtype = detect_question_type(text_data, 'TestColumn')
        self.assertEqual(qtype, QuestionType.TEXT)
    
    def test_extract_question_options_single_choice(self):
        """Test option extraction for single choice questions"""
        sc_data = pd.Series(['A', 'B', 'C', 'A', 'B'])
        options = extract_question_options(sc_data, QuestionType.SINGLE_CHOICE)
        
        self.assertIsNotNone(options)
        self.assertEqual(set(options), {'A', 'B', 'C'})
    
    def test_extract_question_options_multiple_choice(self):
        """Test option extraction for multiple choice questions"""
        mc_data = pd.Series(['A;B', 'B;C', 'A;C'])
        options = extract_question_options(mc_data, QuestionType.MULTIPLE_CHOICE)
        
        self.assertIsNotNone(options)
        self.assertEqual(set(options), {'A', 'B', 'C'})
    
    def test_extract_question_options_other_types(self):
        """Test option extraction for other question types"""
        numeric_data = pd.Series([1, 2, 3])
        options = extract_question_options(numeric_data, QuestionType.NUMERIC)
        self.assertIsNone(options)
        
        text_data = pd.Series(['Text 1', 'Text 2'])
        options = extract_question_options(text_data, QuestionType.TEXT)
        self.assertIsNone(options)
    
    def test_clean_column_name(self):
        """Test column name cleaning"""
        # Test with special characters
        cleaned = clean_column_name('Test_Column-Name!')
        self.assertEqual(cleaned, 'Test Column Name')
        
        # Test with multiple spaces
        cleaned = clean_column_name('Test   Multiple    Spaces')
        self.assertEqual(cleaned, 'Test Multiple Spaces')
    
    def test_search_questions(self):
        """Test question searching"""
        questions = [
            Question('Q1', 'What is your age?', QuestionType.NUMERIC),
            Question('Q2', 'What programming languages do you use?', QuestionType.MULTIPLE_CHOICE),
            Question('Q3', 'What is your country?', QuestionType.SINGLE_CHOICE)
        ]
        
        # Search for 'age'
        results = search_questions(questions, 'age')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].column_name, 'Q1')
        
        # Search for 'programming'
        results = search_questions(questions, 'programming')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].column_name, 'Q2')
        
        # Case insensitive search
        results = search_questions(questions, 'AGE')
        self.assertEqual(len(results), 1)
    
    def test_search_options(self):
        """Test option searching"""
        questions = [
            Question('Q1', 'Programming languages?', QuestionType.MULTIPLE_CHOICE, 
                    ['Python', 'JavaScript', 'Java']),
            Question('Q2', 'Country?', QuestionType.SINGLE_CHOICE, 
                    ['USA', 'Canada', 'UK'])
        ]
        
        # Search for 'Python'
        results = search_options(questions, 'Python')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].column_name, 'Q1')
        self.assertIn('Python', results[0][1])
        
        # Search for 'Java' (should match 'Java' and 'JavaScript')
        results = search_options(questions, 'Java')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0][1]), 2)  # Should match both Java and JavaScript


if __name__ == '__main__':
    unittest.main()
