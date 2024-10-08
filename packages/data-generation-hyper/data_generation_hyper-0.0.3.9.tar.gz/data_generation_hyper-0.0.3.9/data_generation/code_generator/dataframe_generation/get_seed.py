import os
import pandas as pd
import re

from datasets import load_dataset
from ..languages.languages_class import languages_dict
from ..helpers.seed_helper import map_to_standard


def get_seed(share, Total_number):
    """
    Function to retrieve code snippets dataset based on specified share and total number.

    Args:
    - share (dict): A dictionary specifying the share of snippets for each language.
    - Total_number (int): Total number of snippets to consider.

    Returns:
    - DataFrame: The processed code snippets dataset.
    """
    # Load the dataset from glaiveai/glaive-code-assistant-v3
    ds = load_dataset('glaiveai/glaive-code-assistant-v3')
    ds = ds['train']['answer']
    ds = pd.DataFrame(ds, columns=['string'])

    # Define regex pattern and lambda function to extract code snippets
    pattern = r'```(.*?)```'
    lambda_fun = lambda x: re.findall(pattern, x, re.DOTALL)
    ds['string'] = ds['string'].map(lambda_fun)

    # Filter out empty and short snippets
    ds = ds[ds['string'].apply(lambda x: x != [])]
    Series = ds[ds['string'].apply(lambda x: len(x) > 1)]
    ds.loc[Series.index, 'string'] = Series['string'].apply(lambda x: [''.join(x)])
    ds = ds[ds['string'].apply(lambda x: len(x[0]) > 30)]

    # Flatten the list of code snippets and drop duplicates
    ds['string'] = ds['string'].apply(lambda x: x[0])
    ds = ds.drop_duplicates()
    ds.reset_index(drop=True, inplace=True)

    # Define the source languages
    source = [
        "C",
        "C++",
        "C#",
        "CMake",
        "Dockerfile",  # Solutions are to require Dockerfile
        "Go",
        "HTML",
        "Java",
        "JavaScript",
        "Kotlin",
        "Makefile",  # Solutions are to require Makefile
        "PHP",
        "Python",
        "R",
        "Ruby",
        "Rust",
        "Shell",
        "Swift",
        "SQL",
        "Typescript"
    ]  # Language you want to check

    # Extract language from snippets and standardize language names
    ds['language'] = ds['string'].apply(lambda x: re.findall(r'(\S+)', x)[0]) 
    ds['string'] = ds['string'].apply(lambda x: '\n'.join([i for i in re.split(r'\n(?!$)', x)[1:] if i != ''])) 
    ds['language'] = ds['language'].apply(lambda x: map_to_standard(x, source))

    # Sort by language and drop duplicates again
    ds.sort_values(by='language', ascending=False, inplace=True)
    ds.drop_duplicates(subset='string', inplace=True)
    ds.dropna(inplace=True)

    # Create languages_dict object to process and extract snippets
    languages = languages_dict(ds, share=share, Total_number=Total_number)
    snippets_dataset = languages.seeds()

    return snippets_dataset
