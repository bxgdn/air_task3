#!/usr/bin/env python3
"""
Example usage of the Stack Overflow Survey Analyzer library
"""

from stackoverflow_analyzer import StackOverflowAnalyzer
from stackoverflow_analyzer.models import QuestionType


def main():
    """
    Demonstrate the main features of the analyzer
    """
    # Initialize the analyzer with the data files
    print("Loading Stack Overflow Survey data...")
    analyzer = StackOverflowAnalyzer([
        'data_part_1.xlsx',
        'data_part_2.xlsx', 
        'data_part_3.xlsx'
    ])
    
    print("Data loaded successfully!")
    
    # Display survey summary
    analyzer.display_summary()
    
    # Display survey structure (first 5 questions of each type)
    print("\n" + "="*60)
    print("SURVEY STRUCTURE OVERVIEW")
    print("="*60)
    analyzer.display_survey_structure()
    
    # Search for questions about programming languages
    print("\n" + "="*60)
    print("SEARCHING FOR PROGRAMMING LANGUAGE QUESTIONS")
    print("="*60)
    analyzer.display_search_results('language')
    
    # Search for questions about experience
    print("\n" + "="*60)
    print("SEARCHING FOR EXPERIENCE QUESTIONS")
    print("="*60)
    analyzer.display_search_results('experience')
    
    # Show distribution for a single choice question (if available)
    print("\n" + "="*60)
    print("ANSWER DISTRIBUTIONS")
    print("="*60)
    
    # Find a good single choice question to demonstrate
    sc_questions = [q for q in analyzer.questions 
                   if q.question_type == QuestionType.SINGLE_CHOICE 
                   and q.options and len(q.options) < 20]
    
    if sc_questions:
        sample_question = sc_questions[0]
        print(f"Distribution for: {sample_question.column_name}")
        analyzer.display_answer_distribution(sample_question.column_name, top_n=10)
    
    # Show distribution for a multiple choice question (if available)
    mc_questions = [q for q in analyzer.questions 
                   if q.question_type == QuestionType.MULTIPLE_CHOICE
                   and q.options]
    
    if mc_questions:
        sample_mc_question = mc_questions[0]
        print(f"\nDistribution for: {sample_mc_question.column_name}")
        analyzer.display_answer_distribution(sample_mc_question.column_name, top_n=10)
    
    # Demonstrate subset creation
    if sc_questions:
        print("\n" + "="*60)
        print("SUBSET CREATION EXAMPLE")
        print("="*60)
        
        sample_question = sc_questions[0]
        if sample_question.options:
            # Take first option as an example
            sample_option = sample_question.options[0]
            print(f"Creating subset for {sample_question.column_name} = '{sample_option}'")
            
            subset = analyzer.create_subset(sample_question.column_name, [sample_option])
            print(f"Subset size: {len(subset)} respondents")
            
            # Show distribution in the subset for another question
            if len(sc_questions) > 1:
                other_question = sc_questions[1]
                print(f"\nDistribution of {other_question.column_name} in this subset:")
                analyzer.display_answer_distribution(other_question.column_name, 
                                                   subset_df=subset, top_n=5)


if __name__ == "__main__":
    main()
