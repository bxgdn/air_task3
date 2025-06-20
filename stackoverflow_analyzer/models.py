"""
Data models for the Stack Overflow survey analyzer
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import pandas as pd


class QuestionType(Enum):
    """Enumeration of question types in the survey"""
    SINGLE_CHOICE = "SC"
    MULTIPLE_CHOICE = "MC"
    TEXT = "TEXT"
    NUMERIC = "NUMERIC"


@dataclass
class Question:
    """
    Represents a survey question
    """
    column_name: str
    question_text: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    description: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.column_name}: {self.question_text} ({self.question_type.value})"
    
    def __repr__(self) -> str:
        return f"Question(column_name='{self.column_name}', question_type={self.question_type})"


@dataclass
class SurveyResponse:
    """
    Represents a single survey response/respondent
    """
    respondent_id: int
    responses: Dict[str, Any]
    
    def get_response(self, question_column: str) -> Any:
        """Get response for a specific question"""
        return self.responses.get(question_column)


class SurveyData:
    """
    Container for survey data and metadata
    """
    
    def __init__(self, data: pd.DataFrame, questions: List[Question]):
        self.data = data
        self.questions = questions
        self._question_map = {q.column_name: q for q in questions}
    
    def get_question(self, column_name: str) -> Optional[Question]:
        """Get question by column name"""
        return self._question_map.get(column_name)
    
    def get_questions_by_type(self, question_type: QuestionType) -> List[Question]:
        """Get all questions of a specific type"""
        return [q for q in self.questions if q.question_type == question_type]
    
    @property
    def respondent_count(self) -> int:
        """Get total number of respondents"""
        return len(self.data)
    
    @property
    def question_count(self) -> int:
        """Get total number of questions"""
        return len(self.questions)
