"""
Main analyzer class for Stack Overflow survey data
"""

import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from .models import Question, QuestionType, SurveyData
from .utils import load_survey_data, search_questions, search_options


class StackOverflowAnalyzer:
    """
    Main class for analyzing Stack Overflow survey data
    """
    
    def __init__(self, file_paths: List[str]):
        """
        Initialize the analyzer with survey data files
        
        Args:
            file_paths: List of paths to Excel files containing survey data
        """
        self.survey_data = load_survey_data(file_paths)
        self.data = self.survey_data.data
        self.questions = self.survey_data.questions
    
    def display_survey_structure(self, question_type: Optional[QuestionType] = None) -> None:
        """
        Display the survey structure (list of questions) to CLI
        
        Args:
            question_type: Optional filter by question type
        """
        questions_to_display = self.questions
        if question_type:
            questions_to_display = self.survey_data.get_questions_by_type(question_type)
        
        print(f"\n=== SURVEY STRUCTURE ===")
        print(f"Total Questions: {len(questions_to_display)}")
        print(f"Total Respondents: {self.survey_data.respondent_count}")
        print("=" * 50)
        
        # Group by question type
        by_type = {}
        for question in questions_to_display:
            if question.question_type not in by_type:
                by_type[question.question_type] = []
            by_type[question.question_type].append(question)
        
        for qtype, questions_list in by_type.items():
            print(f"\n{qtype.value} Questions ({len(questions_list)}):")
            print("-" * 30)
            for i, question in enumerate(questions_list, 1):
                print(f"{i:2d}. {question.column_name}")
                print(f"    {question.question_text}")
                if question.options and len(question.options) <= 10:
                    print(f"    Options: {', '.join(question.options[:5])}" + 
                          ("..." if len(question.options) > 5 else ""))
                elif question.options:
                    print(f"    Options: {len(question.options)} available")
                print()
    
    def search_question(self, search_term: str) -> List[Question]:
        """
        Search for specific questions containing the search term
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching questions
        """
        return search_questions(self.questions, search_term)
    
    def search_option(self, search_term: str) -> List[Tuple[Question, List[str]]]:
        """
        Search for specific options containing the search term
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of tuples (Question, matching_options)
        """
        return search_options(self.questions, search_term)
    
    def display_search_results(self, search_term: str) -> None:
        """
        Display search results for questions and options
        
        Args:
            search_term: Term to search for
        """
        print(f"\n=== SEARCH RESULTS FOR: '{search_term}' ===")
        
        # Search questions
        question_results = self.search_question(search_term)
        print(f"\nMatching Questions ({len(question_results)}):")
        print("-" * 40)
        for i, question in enumerate(question_results, 1):
            print(f"{i}. {question}")
            if question.options and len(question.options) <= 5:
                print(f"   Options: {', '.join(question.options)}")
            elif question.options:
                print(f"   Options: {len(question.options)} available")
            print()
        
        # Search options
        option_results = self.search_option(search_term)
        print(f"\nMatching Options ({len(option_results)}):")
        print("-" * 40)
        for i, (question, matching_options) in enumerate(option_results, 1):
            print(f"{i}. Question: {question.column_name}")
            print(f"   Matching options: {', '.join(matching_options)}")
            print()
    
    def create_subset(self, question_column: str, option_values: List[str]) -> pd.DataFrame:
        """
        Create a subset of respondents based on question and option values
        
        Args:
            question_column: Column name of the question
            option_values: List of option values to filter by
            
        Returns:
            DataFrame containing the subset of respondents
        """
        question = self.survey_data.get_question(question_column)
        if not question:
            raise ValueError(f"Question '{question_column}' not found")
        
        if question_column not in self.data.columns:
            raise ValueError(f"Column '{question_column}' not found in data")
        
        # Handle different question types
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            # For multiple choice, check if any of the option_values are in the response
            mask = pd.Series([False] * len(self.data))
            for idx, value in enumerate(self.data[question_column]):
                if pd.notna(value):
                    response_options = [opt.strip() for opt in str(value).split(';')]
                    if any(opt in option_values for opt in response_options):
                        mask.iloc[idx] = True
            subset = self.data[mask]
        else:
            # For single choice, numeric, or text questions
            subset = self.data[self.data[question_column].isin(option_values)]
        
        return subset
    
    def get_answer_distribution(self, question_column: str, 
                              subset_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Get the distribution of answers for a question
        
        Args:
            question_column: Column name of the question
            subset_df: Optional subset of data to analyze
            
        Returns:
            Dictionary containing distribution statistics
        """
        question = self.survey_data.get_question(question_column)
        if not question:
            raise ValueError(f"Question '{question_column}' not found")
        
        data_to_analyze = subset_df if subset_df is not None else self.data
        
        if question_column not in data_to_analyze.columns:
            raise ValueError(f"Column '{question_column}' not found in data")
        
        total_responses = len(data_to_analyze)
        valid_responses = data_to_analyze[question_column].notna().sum()
        
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            # Handle multiple choice questions
            all_options = []
            for value in data_to_analyze[question_column].dropna():
                if pd.notna(value) and ';' in str(value):
                    options = [opt.strip() for opt in str(value).split(';')]
                    all_options.extend(options)
            
            option_counts = Counter(all_options)
            distribution = {opt: count for opt, count in option_counts.items()}
            percentages = {opt: (count / valid_responses) * 100 
                          for opt, count in option_counts.items()}
        
        else:
            # Handle single choice, numeric, or text questions
            value_counts = data_to_analyze[question_column].value_counts()
            distribution = value_counts.to_dict()
            percentages = (value_counts / valid_responses * 100).to_dict()
        
        return {
            'question': question,
            'total_responses': total_responses,
            'valid_responses': valid_responses,
            'response_rate': (valid_responses / total_responses) * 100 if total_responses > 0 else 0,
            'distribution': distribution,
            'percentages': percentages
        }
    
    def display_answer_distribution(self, question_column: str, 
                                  subset_df: Optional[pd.DataFrame] = None,
                                  top_n: int = 10) -> None:
        """
        Display the distribution of answers for a question to CLI
        
        Args:
            question_column: Column name of the question
            subset_df: Optional subset of data to analyze
            top_n: Number of top answers to display
        """
        try:
            dist_data = self.get_answer_distribution(question_column, subset_df)
            
            print(f"\n=== ANSWER DISTRIBUTION ===")
            print(f"Question: {dist_data['question'].column_name}")
            print(f"Type: {dist_data['question'].question_type.value}")
            print(f"Total Responses: {dist_data['total_responses']}")
            print(f"Valid Responses: {dist_data['valid_responses']}")
            print(f"Response Rate: {dist_data['response_rate']:.1f}%")
            print("=" * 50)
            
            # Sort by count and take top N
            sorted_items = sorted(dist_data['distribution'].items(), 
                                key=lambda x: x[1], reverse=True)[:top_n]
            
            print(f"\nTop {len(sorted_items)} Answers:")
            print("-" * 60)
            print(f"{'Answer':<40} {'Count':<8} {'Percentage'}")
            print("-" * 60)
            
            for answer, count in sorted_items:
                percentage = dist_data['percentages'][answer]
                # Truncate long answers
                display_answer = str(answer)[:37] + "..." if len(str(answer)) > 40 else str(answer)
                print(f"{display_answer:<40} {count:<8} {percentage:.1f}%")
            
            if len(dist_data['distribution']) > top_n:
                remaining = len(dist_data['distribution']) - top_n
                print(f"... and {remaining} more answers")
                
        except Exception as e:
            print(f"Error displaying distribution: {e}")
    
    def get_question_summary(self) -> Dict[str, int]:
        """
        Get a summary of questions by type
        
        Returns:
            Dictionary with question type counts
        """
        summary = {}
        for question in self.questions:
            qtype = question.question_type.value
            summary[qtype] = summary.get(qtype, 0) + 1
        
        return summary
    
    def display_summary(self) -> None:
        """
        Display a summary of the survey data
        """
        summary = self.get_question_summary()
        
        print(f"\n=== SURVEY SUMMARY ===")
        print(f"Total Respondents: {self.survey_data.respondent_count}")
        print(f"Total Questions: {self.survey_data.question_count}")
        print("\nQuestion Types:")
        for qtype, count in summary.items():
            print(f"  {qtype}: {count}")
        print("=" * 30)
