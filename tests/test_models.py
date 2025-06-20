"""
Unit tests for the data models
"""

import unittest
import pandas as pd
from stackoverflow_analyzer.models import Question, QuestionType, SurveyData


class TestModels(unittest.TestCase):
    """Test cases for data models"""
    
    def test_question_creation(self):
        """Test Question model creation"""
        question = Question(
            column_name='TestColumn',
            question_text='Test question?',
            question_type=QuestionType.SINGLE_CHOICE,
            options=['Option1', 'Option2']
        )
        
        self.assertEqual(question.column_name, 'TestColumn')
        self.assertEqual(question.question_text, 'Test question?')
        self.assertEqual(question.question_type, QuestionType.SINGLE_CHOICE)
        self.assertEqual(question.options, ['Option1', 'Option2'])
    
    def test_question_string_representation(self):
        """Test Question string representations"""
        question = Question(
            column_name='TestColumn',
            question_text='Test question?',
            question_type=QuestionType.SINGLE_CHOICE
        )
        
        str_repr = str(question)
        self.assertIn('TestColumn', str_repr)
        self.assertIn('Test question?', str_repr)
        self.assertIn('SC', str_repr)
    
    def test_survey_data(self):
        """Test SurveyData model"""
        # Create sample data
        data = pd.DataFrame({
            'Q1': [1, 2, 3],
            'Q2': ['A', 'B', 'C']
        })
        
        questions = [
            Question('Q1', 'Question 1?', QuestionType.NUMERIC),
            Question('Q2', 'Question 2?', QuestionType.SINGLE_CHOICE, ['A', 'B', 'C'])
        ]
        
        survey_data = SurveyData(data, questions)
        
        self.assertEqual(survey_data.respondent_count, 3)
        self.assertEqual(survey_data.question_count, 2)
        
        # Test get_question
        q1 = survey_data.get_question('Q1')
        self.assertIsNotNone(q1)
        self.assertEqual(q1.column_name, 'Q1')
        
        # Test get_questions_by_type
        numeric_questions = survey_data.get_questions_by_type(QuestionType.NUMERIC)
        self.assertEqual(len(numeric_questions), 1)
        self.assertEqual(numeric_questions[0].column_name, 'Q1')


if __name__ == '__main__':
    unittest.main()
