import os
import pandas as pd
from ..config.path import path


def save_batch_result_and_concat(dataframe, batch_index):
    """
    Function to save the accumulated processed batches as a single CSV file.
    """
    current_directory = os.getcwd()
    functions_dir = os.path.join(current_directory, 'app', 'functions', 'code_generator', 'generated_data', 'batches')

    # Ensure the folder exists
    os.makedirs(functions_dir, exist_ok=True)
    
    # Save the concatenated DataFrame
    concat_filepath = os.path.join(functions_dir, f'batch_{batch_index}.csv')
    dataframe.to_csv(concat_filepath, index=False, mode='w')
    print(f"Concatenated batches for index {batch_index} saved to {concat_filepath}.")


def save_final(dataframe):
    """
    Function to save the final DataFrame to a CSV file.
    """
    # Ensure the directory exists, create it if it doesn't
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)

    # Save the DataFrame to CSV, overwrite if the file already exists
    dataframe.to_csv(path, index=False, mode='w')
    print(f"Final DataFrame saved to {path}.")  # Print a confirmation message
