# Stack Overflow Survey Data Analysis Library

A comprehensive Python library for analyzing Stack Overflow survey data with support for survey structure display, question/option searching, respondent subsetting, and answer distribution analysis.

## Features

- **Survey Structure Display**: View the complete survey structure with question types and options
- **Search Functionality**: Search for specific questions or options using keywords
- **Respondent Subsetting**: Create subsets of respondents based on question responses
- **Answer Distribution Analysis**: Display distribution of answers for both single choice (SC) and multiple choice (MC) questions
- **Command Line Interface**: Interactive CLI/REPL support for data exploration

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd stackoverflow-survey-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install pandas openpyxl matplotlib seaborn
```

## Project Structure

```
stackoverflow_analyzer/
├── __init__.py              # Package initialization
├── analyzer.py              # Main analyzer class
├── models.py               # Data models (Question, SurveyData, etc.)
├── utils.py                # Utility functions
tests/
├── __init__.py
├── test_analyzer.py        # Tests for main analyzer
├── test_models.py          # Tests for data models
├── test_utils.py           # Tests for utility functions
example_usage.py            # Example usage script
requirements.txt            # Python dependencies
README.md                   # This file
```

## Usage

### Basic Usage

```python
from stackoverflow_analyzer import StackOverflowAnalyzer

# Initialize analyzer with data files
analyzer = StackOverflowAnalyzer([
    'data_part_1.xlsx',
    'data_part_2.xlsx', 
    'data_part_3.xlsx'
])

# Display survey structure
analyzer.display_survey_structure()

# Search for questions
results = analyzer.search_question('programming')
print(f"Found {len(results)} questions about programming")

# Display answer distribution
analyzer.display_answer_distribution('YourQuestionColumn')
```

### Advanced Usage

```python
# Create subset of respondents
subset = analyzer.create_subset('Country', ['USA', 'Canada'])
print(f"Created subset with {len(subset)} respondents")

# Display distribution within subset
analyzer.display_answer_distribution('LanguagePreference', subset_df=subset)

# Search for specific options
option_results = analyzer.search_option('Python')
for question, matching_options in option_results:
    print(f"Found 'Python' in {question.column_name}: {matching_options}")
```

### Command Line Interface

Run the example script to see all features:

```bash
python example_usage.py
```

## API Reference

### StackOverflowAnalyzer

Main class for analyzing survey data.

#### Methods

- `__init__(file_paths: List[str])` - Initialize with Excel file paths
- `display_survey_structure(question_type: Optional[QuestionType] = None)` - Display survey structure
- `search_question(search_term: str) -> List[Question]` - Search for questions
- `search_option(search_term: str) -> List[Tuple[Question, List[str]]]` - Search for options
- `create_subset(question_column: str, option_values: List[str]) -> pd.DataFrame` - Create respondent subset
- `get_answer_distribution(question_column: str, subset_df: Optional[pd.DataFrame] = None) -> Dict` - Get answer distribution
- `display_answer_distribution(question_column: str, subset_df: Optional[pd.DataFrame] = None, top_n: int = 10)` - Display answer distribution

### Question Types

The library supports four question types:

- **SINGLE_CHOICE (SC)**: Questions with one possible answer
- **MULTIPLE_CHOICE (MC)**: Questions allowing multiple answers (semicolon-separated)
- **NUMERIC**: Numeric questions
- **TEXT**: Free-text questions

### Data Models

- **Question**: Represents a survey question with metadata
- **QuestionType**: Enumeration of question types
- **SurveyData**: Container for survey data and questions

## Running Tests

Run all tests:
```bash
python -m pytest tests/
```

Run specific test file:
```bash
python -m pytest tests/test_analyzer.py
```

Run tests with coverage:
```bash
python -m pytest tests/ --cov=stackoverflow_analyzer
```

Or run tests using unittest:
```bash
python -m unittest discover tests/
```

## Data Format

The library expects Excel files (.xlsx) with:
- Each row representing a survey respondent
- Each column representing a survey question
- Multiple choice answers separated by semicolons (;)
- Missing values handled automatically

## Examples

### Display Survey Structure
```python
# Show all questions
analyzer.display_survey_structure()

# Show only single choice questions
from stackoverflow_analyzer.models import QuestionType
analyzer.display_survey_structure(QuestionType.SINGLE_CHOICE)
```

### Search and Filter
```python
# Search for questions about experience
experience_questions = analyzer.search_question('experience')

# Search for options containing 'Python'
python_options = analyzer.search_option('Python')
```

### Create Subsets
```python
# Create subset of developers from specific countries
usa_canada_subset = analyzer.create_subset('Country', ['USA', 'Canada'])

# Create subset of Python developers (multiple choice)
python_devs = analyzer.create_subset('Languages', ['Python'])
```

### Analyze Distributions
```python
# Show distribution for all respondents
analyzer.display_answer_distribution('LanguagePreference')

# Show distribution for subset
analyzer.display_answer_distribution('Experience', subset_df=python_devs)
```

## Requirements

- Python 3.7+
- pandas
- openpyxl
- matplotlib (optional, for future plotting features)
- seaborn (optional, for future plotting features)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure Excel files are in the correct location
2. **Memory issues**: For large datasets, consider processing files individually
3. **Encoding issues**: Ensure Excel files are saved in a compatible format

### Performance Tips

- Use subsets for large datasets to improve performance
- Limit `top_n` parameter when displaying distributions
- Consider filtering questions by type for faster operations
