# Stack Overflow Survey Analysis Library

A Python library for analyzing Stack Overflow Survey data. This library provides tools to load, explore, and analyze survey data from Stack Overflow's annual developer survey.

## Features

- Load and integrate multiple Excel survey files
- List survey questions and their types (single-choice or multiple-choice)
- Search for specific questions or answer options
- Filter respondents based on their answers to specific questions
- Display the distribution of answers for any question

## Installation

### Prerequisites

- Python 3.7 or higher
- pandas
- openpyxl

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/stacksurvey.git
cd stacksurvey

# Install the package
pip install -e .
```

### Install dependencies only

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

The library provides a command-line interface for common operations:

#### Load survey data

```bash
python -m stacksurvey load path/to/survey1.xlsx path/to/survey2.xlsx path/to/survey3.xlsx
```

#### List all survey questions

```bash
python -m stacksurvey list-questions
```

#### Search for questions or options

```bash
# Search for questions containing "Python"
python -m stacksurvey search --question "Python"

# Search for options containing "Python"
python -m stacksurvey search --option "Python"
```

#### Filter respondents

```bash
# Find all respondents who selected "Python" for "LanguageWorkedWith"
python -m stacksurvey filter --question "LanguageWorkedWith" --option "Python"

# Save filtered results to a CSV file
python -m stacksurvey filter --question "EdLevel" --option "Bachelor" --output "bachelors.csv"
```

#### Show distribution of answers

```bash
# Show distribution for a single-choice question
python -m stacksurvey distribution --question "EdLevel"

# Show distribution for a multiple-choice question
python -m stacksurvey distribution --question "LanguageWorkedWith"
```

### Python API

You can also use the library directly in your Python code:

```python
from stacksurvey import load_data, list_questions, search, filter_respondents, compute_distribution

# Load survey data
df = load_data(["path/to/survey1.xlsx", "path/to/survey2.xlsx", "path/to/survey3.xlsx"])

# List all questions
questions = list_questions()
for q_id, q_type in questions.items():
    print(f"{q_id} ({q_type})")

# Search for questions or options
results = search(question="Python", option=None)
print(results)

# Filter respondents
python_users = filter_respondents("LanguageWorkedWith", "Python")
print(f"Number of Python users: {len(python_users)}")

# Compute distribution
distribution = compute_distribution("EdLevel")
for option, percentage in distribution.items():
    print(f"{option}: {percentage:.2%}")
```

## Sample Data

If you don't have the Stack Overflow Survey data, you can create sample data for testing:

```bash
cd data
python create_sample_data.py
```

This will create three sample Excel files in the `data/sample_data/` directory.

## Running Tests

To run the test suite:

```bash
pytest
```

For more detailed test output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_core.py
```
