"""Command-line interface for Stack Overflow survey analysis."""

import argparse
import sys
from typing import List, Optional
import pandas as pd

from .core import (
    load_data,
    list_questions,
    search,
    filter_respondents,
    compute_distribution
)


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Stack Overflow Survey Analysis Tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # load command
    load_parser = subparsers.add_parser(
        "load", help="Load survey data files"
    )
    load_parser.add_argument(
        "files", nargs="+", help="Paths to survey Excel files"
    )
    
    # list-questions command
    subparsers.add_parser(
        "list-questions", help="List all survey questions"
    )
    
    # search command
    search_parser = subparsers.add_parser(
        "search", help="Search for questions or options"
    )
    search_parser.add_argument(
        "--question", help="Text to search in question identifiers"
    )
    search_parser.add_argument(
        "--option", help="Text to search in answer options"
    )
    
    # filter command
    filter_parser = subparsers.add_parser(
        "filter", help="Filter respondents by question and answer option"
    )
    filter_parser.add_argument(
        "--question", required=True, help="Question identifier"
    )
    filter_parser.add_argument(
        "--option", required=True, help="Answer option to filter by"
    )
    filter_parser.add_argument(
        "--output", help="Path to save filtered data (optional)"
    )
    
    # distribution command
    dist_parser = subparsers.add_parser(
        "distribution", help="Show distribution of answers for a question"
    )
    dist_parser.add_argument(
        "--question", required=True, help="Question identifier"
    )
    
    return parser.parse_args(args)


def handle_load(args: argparse.Namespace) -> int:
    """Handle the load command."""
    try:
        df = load_data(args.files)
        print(f"Successfully loaded {len(df)} respondents from {len(args.files)} files.")
        return 0
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        return 1


def handle_list_questions(args: argparse.Namespace) -> int:
    """Handle the list-questions command."""
    try:
        questions = list_questions()
        for q_id, q_type in questions.items():
            print(f"{q_id} ({q_type})")
        return 0
    except Exception as e:
        print(f"Error listing questions: {e}", file=sys.stderr)
        return 1


def handle_search(args: argparse.Namespace) -> int:
    """Handle the search command."""
    try:
        results = search(question=args.question, option=args.option)
        
        if results['questions']:
            print("Matching questions:")
            for q_id in results['questions']:
                print(f"  {q_id}")
        
        if results['options']:
            print("Matching options:")
            for q_id, option, idx in results['options']:
                print(f"  {q_id}: {option} (index: {idx})")
        
        if not results['questions'] and not results['options']:
            print("No matches found.")
        
        return 0
    except Exception as e:
        print(f"Error searching: {e}", file=sys.stderr)
        return 1


def handle_filter(args: argparse.Namespace) -> int:
    """Handle the filter command."""
    try:
        filtered_df = filter_respondents(args.question, args.option)
        print(f"Filtered data: {len(filtered_df)} respondents")
        
        if args.output:
            filtered_df.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")
        
        return 0
    except Exception as e:
        print(f"Error filtering: {e}", file=sys.stderr)
        return 1


def handle_distribution(args: argparse.Namespace) -> int:
    """Handle the distribution command."""
    try:
        distribution = compute_distribution(args.question)
        
        print(f"Distribution for '{args.question}':")
        for option, percentage in distribution.items():
            print(f"  {option}: {percentage:.2%}")
        
        return 0
    except Exception as e:
        print(f"Error computing distribution: {e}", file=sys.stderr)
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    if args is None:
        args = sys.argv[1:]
    
    parsed_args = parse_args(args)
    
    if parsed_args.command == "load":
        return handle_load(parsed_args)
    elif parsed_args.command == "list-questions":
        return handle_list_questions(parsed_args)
    elif parsed_args.command == "search":
        return handle_search(parsed_args)
    elif parsed_args.command == "filter":
        return handle_filter(parsed_args)
    elif parsed_args.command == "distribution":
        return handle_distribution(parsed_args)
    else:
        print("Please specify a command. Use --help for more information.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
