"""Create sample Stack Overflow survey data files for testing."""

import os
import pandas as pd

# Create directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Create sample data for three files

# File 1: Basic demographics
df1 = pd.DataFrame({
    'Respondent': list(range(1, 201)),
    'Country': ['USA', 'India', 'Germany', 'UK', 'Canada'] * 40,
    'EdLevel': ['Bachelor', 'Master', 'PhD', 'High School', 'Some College'] * 40,
    'YearsCodePro': [1, 3, 5, 10, 15] * 40,
    'Age': [25, 30, 35, 40, 45] * 40
})

# File 2: Languages and technologies
df2 = pd.DataFrame({
    'Respondent': list(range(201, 401)),
    'Country': ['Brazil', 'France', 'Australia', 'Japan', 'China'] * 40,
    'EdLevel': ['Bachelor', 'Master', 'PhD', 'High School', 'Some College'] * 40,
    'LanguageWorkedWith': [
        'Python;JavaScript;HTML',
        'Python;Java;C#',
        'JavaScript;TypeScript;HTML;CSS',
        'C++;Java;Python',
        'Go;Rust;C'
    ] * 40,
    'DatabaseWorkedWith': [
        'MySQL;PostgreSQL',
        'MongoDB;Redis',
        'SQLite;MySQL',
        'PostgreSQL;Oracle',
        'SQL Server;Redis'
    ] * 40
})

# File 3: Career and job satisfaction
df3 = pd.DataFrame({
    'Respondent': list(range(401, 601)),
    'Country': ['Mexico', 'Spain', 'Italy', 'Russia', 'Sweden'] * 40,
    'EdLevel': ['Bachelor', 'Master', 'PhD', 'High School', 'Some College'] * 40,
    'JobSatisfaction': ['Very satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very dissatisfied'] * 40,
    'CareerSatisfaction': ['Very satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very dissatisfied'] * 40,
    'DevType': [
        'Full-stack developer',
        'Back-end developer',
        'Front-end developer',
        'Data scientist or machine learning specialist',
        'DevOps specialist'
    ] * 40
})

# Save dataframes to Excel files
df1.to_excel('sample_data/survey_part1.xlsx', index=False)
df2.to_excel('sample_data/survey_part2.xlsx', index=False)
df3.to_excel('sample_data/survey_part3.xlsx', index=False)

print("Sample data created in ./sample_data/ directory")
print("Files:")
print("  - sample_data/survey_part1.xlsx")
print("  - sample_data/survey_part2.xlsx")
print("  - sample_data/survey_part3.xlsx")
