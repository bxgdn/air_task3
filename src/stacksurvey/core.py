"""Core functionality for Stack Overflow survey analysis."""

import os
from typing import List, Dict, Union, Optional, Tuple
import pandas as pd


# Global variable to store the loaded data
_survey_data = None
_questions_data = None


def load_data(file_paths: List[str]) -> pd.DataFrame:
    """
    Load and integrate multiple Excel survey files into a single DataFrame.
    
    Args:
        file_paths: List of paths to the Excel survey files
        
    Returns:
        DataFrame containing the combined survey data
    """
    global _survey_data, _questions_data
    
    if not file_paths:
        raise ValueError("No file paths provided")
    
    # Check if all files exist
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Survey file not found: {file_path}")
    
    # Load and combine the data from all files
    dfs = []
    for file_path in file_paths:
        df = pd.read_excel(file_path)
        dfs.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Store the data for later use
    _survey_data = combined_df
    
    # Extract the questions (column names) and store them
    _questions_data = {col: _get_question_type(combined_df, col) 
                      for col in combined_df.columns}
    
    return combined_df


def _get_question_type(df: pd.DataFrame, column: str) -> str:
    """
    Determine if a question is single-choice or multiple-choice.
    
    Args:
        df: Survey data DataFrame
        column: Column name representing the question
        
    Returns:
        'SC' for single-choice or 'MC' for multiple-choice
    """
    # Check if any non-null values contain semicolons, which typically
    # indicate multiple selections in Stack Overflow surveys
    values = df[column].dropna()
    if len(values) == 0:
        return 'SC'  # Default to single-choice if no data
    
    # If any value contains a semicolon, it's likely a multiple-choice question
    if any(str(val).find(';') != -1 for val in values):
        return 'MC'
    return 'SC'


def list_questions() -> Dict[str, Dict[str, str]]:
    """
    Get a list of survey questions with their types.
    
    Returns:
        Dictionary mapping question IDs to their details
    """
    if _survey_data is None:
        raise RuntimeError("Survey data not loaded. Call load_data() first.")
    
    return _questions_data


def search(question: str = None, option: str = None) -> Dict[str, Union[List[str], List[Tuple[str, int]]]]:
    """
    Search for specific questions or options in the survey data.
    
    Args:
        question: String to search for in question text/identifiers
        option: String to search for in answer options
        
    Returns:
        Dictionary with matching questions and/or options
    """
    if _survey_data is None:
        raise RuntimeError("Survey data not loaded. Call load_data() first.")
    
    results = {
        'questions': [],
        'options': []
    }
    
    # Search in questions
    if question:
        for col in _survey_data.columns:
            if question.lower() in col.lower():
                results['questions'].append(col)
    
    # Search in options
    if option:
        for col in _survey_data.columns:
            # Get unique values for this column
            unique_values = _get_unique_options(col)
            
            # Check if the option is in any of the unique values
            matches = [(val, i) for i, val in enumerate(unique_values) 
                      if option.lower() in val.lower()]
            
            if matches:
                for match in matches:
                    results['options'].append((col, match[0], match[1]))
    
    return results


def _get_unique_options(column: str) -> List[str]:
    """
    Get unique options for a question, handling both single and multiple-choice.
    
    Args:
        column: Column name representing the question
        
    Returns:
        List of unique options
    """
    if _survey_data is None:
        raise RuntimeError("Survey data not loaded. Call load_data() first.")
    
    values = _survey_data[column].dropna()
    
    if _questions_data.get(column) == 'MC':
        # For multiple-choice, split by semicolon and flatten
        all_options = []
        for val in values:
            if isinstance(val, str):
                all_options.extend(val.split(';'))
        return sorted(list(set(all_options)))
    else:
        # For single-choice, just get unique values
        return sorted(list(set(str(val) for val in values)))


def filter_respondents(question: str, option: str) -> pd.DataFrame:
    """
    Filter survey respondents based on their answer to a specific question.
    
    Args:
        question: Question identifier (column name)
        option: Answer option to filter by
        
    Returns:
        DataFrame containing only respondents who selected the specified option
    """
    if _survey_data is None:
        raise RuntimeError("Survey data not loaded. Call load_data() first.")
    
    if question not in _survey_data.columns:
        raise ValueError(f"Question '{question}' not found in survey data")
    
    question_type = _questions_data.get(question)
    
    if question_type == 'MC':
        # For multiple-choice, need to check if option is in the semicolon-separated list
        return _survey_data[_survey_data[question].apply(
            lambda x: isinstance(x, str) and option in x.split(';')
        )]
    else:
        # For single-choice, simple equality check
        return _survey_data[_survey_data[question] == option]


def compute_distribution(question: str) -> Dict[str, float]:
    """
    Compute the distribution of answers for a question.
    
    Args:
        question: Question identifier (column name)
        
    Returns:
        Dictionary mapping options to their percentage shares
    """
    if _survey_data is None:
        raise RuntimeError("Survey data not loaded. Call load_data() first.")
    
    if question not in _survey_data.columns:
        raise ValueError(f"Question '{question}' not found in survey data")
    
    question_type = _questions_data.get(question)
    
    if question_type == 'MC':
        # For multiple-choice, need to split the semicolon-separated values
        # and count each option separately
        options_series = _survey_data[question].dropna()
        
        # Explode the multiple-choice options
        all_selections = []
        for val in options_series:
            if isinstance(val, str):
                all_selections.extend(val.split(';'))
        
        # Count occurrences and calculate percentages
        option_counts = pd.Series(all_selections).value_counts(normalize=True)
        return option_counts.to_dict()
    else:
        # For single-choice, use value_counts with normalization
        counts = _survey_data[question].value_counts(normalize=True)
        return counts.to_dict()
