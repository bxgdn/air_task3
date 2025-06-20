"""
Utility functions for loading and preprocessing survey data
"""

import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import re
from .models import Question, QuestionType, SurveyData


def detect_question_type(column_data: pd.Series, column_name: str) -> QuestionType:
    """
    Detect the type of question based on the data in the column
    """
    # Check for numeric data
    if pd.api.types.is_numeric_dtype(column_data):
        return QuestionType.NUMERIC
    
    # Check for multiple choice (semicolon-separated values)
    sample_values = column_data.dropna().head(100)
    if any(';' in str(val) for val in sample_values if pd.notna(val)):
        return QuestionType.MULTIPLE_CHOICE
    
    # Count unique values to determine if it's single choice or text
    unique_count = column_data.nunique()
    total_count = len(column_data.dropna())
    
    # If unique values are less than 20% of total responses, likely single choice
    if total_count > 0 and unique_count / total_count < 0.2 and unique_count < 50:
        return QuestionType.SINGLE_CHOICE
    
    return QuestionType.TEXT


def extract_question_options(column_data: pd.Series, question_type: QuestionType) -> Optional[List[str]]:
    """
    Extract possible options for single choice and multiple choice questions
    """
    if question_type == QuestionType.SINGLE_CHOICE:
        # Get unique non-null values
        options = column_data.dropna().unique().tolist()
        return sorted([str(opt) for opt in options if opt != ''])
    
    elif question_type == QuestionType.MULTIPLE_CHOICE:
        # Split by semicolon and collect all unique options
        all_options = set()
        for value in column_data.dropna():
            if pd.notna(value) and ';' in str(value):
                options = [opt.strip() for opt in str(value).split(';')]
                all_options.update(options)
        return sorted(list(all_options))
    
    return None


def clean_column_name(column_name: str) -> str:
    """
    Clean column names to make them more readable
    """
    # Remove special characters and make more readable
    cleaned = re.sub(r'[^\w\s]', ' ', column_name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def generate_question_text(column_name: str) -> str:
    """
    Generate a readable question text from column name
    """
    # Convert column name to a more readable format
    text = clean_column_name(column_name)
    
    # Add question mark if not present
    if not text.endswith('?'):
        text += '?'
    
    return text


def load_survey_data(file_paths: List[str]) -> SurveyData:
    """
    Load survey data from multiple Excel files and combine them
    
    Args:
        file_paths: List of paths to Excel files
        
    Returns:
        SurveyData object containing the combined data and questions
    """
    all_dataframes = []
    
    # Load each Excel file
    for file_path in file_paths:
        try:
            df = pd.read_excel(file_path)
            all_dataframes.append(df)
            print(f"Loaded {len(df)} rows from {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    if not all_dataframes:
        raise ValueError("No data files could be loaded")
    
    # Combine all dataframes
    combined_df = pd.concat(all_dataframes, ignore_index=True, sort=False)
    print(f"Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
    
    # Create questions from columns
    questions = []
    for column_name in combined_df.columns:
        question_type = detect_question_type(combined_df[column_name], column_name)
        options = extract_question_options(combined_df[column_name], question_type)
        question_text = generate_question_text(column_name)
        
        question = Question(
            column_name=column_name,
            question_text=question_text,
            question_type=question_type,
            options=options
        )
        questions.append(question)
    
    return SurveyData(combined_df, questions)


def search_questions(questions: List[Question], search_term: str) -> List[Question]:
    """
    Search for questions containing the search term
    
    Args:
        questions: List of Question objects
        search_term: Term to search for (case-insensitive)
        
    Returns:
        List of matching questions
    """
    search_term = search_term.lower()
    matching_questions = []
    
    for question in questions:
        # Search in question text and column name
        if (search_term in question.question_text.lower() or 
            search_term in question.column_name.lower()):
            matching_questions.append(question)
            continue
            
        # Search in options if available
        if question.options:
            for option in question.options:
                if search_term in option.lower():
                    matching_questions.append(question)
                    break
    
    return matching_questions


def search_options(questions: List[Question], search_term: str) -> List[Tuple[Question, List[str]]]:
    """
    Search for options containing the search term
    
    Args:
        questions: List of Question objects
        search_term: Term to search for (case-insensitive)
        
    Returns:
        List of tuples (Question, matching_options)
    """
    search_term = search_term.lower()
    results = []
    
    for question in questions:
        if question.options:
            matching_options = [opt for opt in question.options 
                              if search_term in opt.lower()]
            if matching_options:
                results.append((question, matching_options))
    
    return results
