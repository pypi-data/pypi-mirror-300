import pandas as pd
import regex as re
import random
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

from code_generator.prompts.prompt_list_and_probabilities import prompt_list, probabilities
from code_generator.dataframe_generation.get_seed import get_seed
from code_generator.helpers.generator_helper import fun, problem_text, solution_text
# from functions.code_generator.prompts.prompt import OSS_problem_prompt, OSS_solution_prompt
from code_generator.helpers.save_batches import save_batch_result_and_concat, save_final



def post_process(input_string):
    """
    Post-processes the input string to extract the main content after 'Problem Description:' or 'Solution:'.
    """
    # Initialize an empty list to store non-empty lines without the specified strings
    output = []

    if len(input_string) != 0 and input_string is not None:
        # Split the input string into lines
        lines = input_string.splitlines()

        # Iterate through each line starting from the second line
        if "Problem Description:" in input_string or "[Problem Description]" in input_string or "**Problem Description" in input_string:
            for index in range(len(lines)):
                if "Problem Description:" in lines[index] or "[Problem Description]" in lines[index] or "**Problem Description" in lines[index]:
                    for sub_index in range(index + 1, len(lines)):
                        if lines[sub_index].strip():
                            output.append(lines[sub_index])
        elif "Solution:" in input_string or "[Solution]" in input_string or "**Solution" in input_string:
            for index in range(len(lines)):
                if "Solution:" in lines[index] or "[Solution]" in lines[index] or "**Solution" in lines[index]:
                    for sub_index in range(index + 1, len(lines)):
                        if lines[sub_index].strip():
                            output.append(lines[sub_index])

        # Join the cleaned non-empty lines to form the new string
        output = '\n'.join(output)            

    return output

def generator(batch, api_key, share, Total_number, 
              model='meta-llama/Llama-3-70b-chat-hf', 
              temperature_problem=0.7, temperature_solution=0.5):
    """
    Function to generate problem and solution texts along with their tokens for a given batch of data.
    """
    # Create a copy of the batch to avoid SettingWithCopyWarning
    batch = batch.copy()

    OSS_problem_prompt, OSS_solution_prompt = random.choices(prompt_list, probabilities)[0]

    # Generate problem and solution texts
    batch['problem_text'] = batch['string'].apply(lambda x: problem_text(fun(x), api_key, OSS_problem_prompt, 
                                                  model=model, temperature=temperature_problem))

    batch['solution_text'] = batch.apply(lambda x: solution_text(x['problem_text'], api_key, x['language'], OSS_solution_prompt, 
                                          model=model, temperature=temperature_solution), axis=1)

    # Extract tokens from the generated texts
    batch['problem_tokens'] = batch['problem_text'].apply(lambda x: x[1])
    batch['solution_tokens'] = batch['solution_text'].apply(lambda x: x[1])

    # Extract only the text part, discard the tokens
    batch['problem_text'] = batch['problem_text'].apply(lambda x: x[0])
    batch['solution_text'] = batch['solution_text'].apply(lambda x: x[0])

    # Apply post-processing to extract the main content
    batch['problem_text'] = batch['problem_text'].apply(lambda x: post_process(x))
    batch['solution_text'] = batch['solution_text'].apply(lambda x: post_process(x))

    return batch

def generate_training(api_key=None, share=None, Total_number=None, batch_size=3, n_jobs=None, 
                      model='meta-llama/Llama-3-70b-chat-hf', temperature_problem=0.7, temperature_solution=0.5, 
                      test=False):
    """
    Main function to generate training data by processing batches of code snippets.
    """
    # Get the initial dataset and preprocess it
    snippets_dataset = get_seed(share, Total_number)
    snippets_dataset = snippets_dataset.dropna()
    snippets_dataset['string'] = snippets_dataset['string'].apply(lambda x: fun(x))
    snippets_dataset = snippets_dataset.dropna().drop_duplicates(subset='string')

    print("snippets_dataset--->", len(snippets_dataset))

    # Split the dataset into batches
    batch_list = [snippets_dataset[i:i+batch_size] for i in range(0, len(snippets_dataset), batch_size)]

    if test:
        batch_list = batch_list[:2]  # Use only a few batches for testing purposes
    
    if not n_jobs:
        n_jobs = min(multiprocessing.cpu_count(), 20)  # Set the number of jobs for parallel processing

    results = []

    def process_and_save(batch, index):
        """
        Function to process a batch and save the result with tqdm progress tracking.
        """
        with tqdm(total=1, desc=f"Processing Batch {index}") as pbar:
            result = generator(batch=batch, api_key=api_key, share=share, 
                               Total_number=Total_number, model=model, 
                               temperature_problem=temperature_problem, 
                               temperature_solution=temperature_solution)
            
            results.append(result)
            pbar.update(1)  # Update the progress bar to indicate completion of the batch
            
        save_batch_result_and_concat(result, index)  # Save the processed batch and concatenate with previous batches
        return result

    print("generation process started")
    # Use parallel processing to process and save each batch
    Parallel(n_jobs=n_jobs, prefer="threads")(
        delayed(process_and_save)(batch, index) for index, batch in enumerate(tqdm(batch_list))
    )

    # Concatenate all results into a single DataFrame
    final_df = pd.concat(results, ignore_index=True)

    return final_df

