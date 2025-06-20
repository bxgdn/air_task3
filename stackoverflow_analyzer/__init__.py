"""
Stack Overflow Survey Data Analysis Library

A Python library for analyzing Stack Overflow survey data with support for:
- Survey structure display
- Question/option searching
- Respondent subsetting
- Answer distribution analysis
"""

from .analyzer import StackOverflowAnalyzer
from .models import Question, QuestionType
from .utils import load_survey_data

__version__ = "1.0.0"
__all__ = ["StackOverflowAnalyzer", "Question", "QuestionType", "load_survey_data"]
