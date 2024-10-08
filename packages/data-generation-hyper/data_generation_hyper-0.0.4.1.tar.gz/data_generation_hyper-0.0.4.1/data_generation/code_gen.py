from typing import List, Optional, Union, Dict
from pandas import DataFrame
import json
import pandas as pd
import regex as re
import random
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

from .code_generator.prompts.prompt_list_and_probabilities import prompt_list, probabilities
from .code_generator.dataframe_generation.get_seed import get_seed
from .code_generator.helpers.generator_helper import fun, problem_text, solution_text
from .code_generator.helpers.save_batches import save_batch_result_and_concat
from .code_generator.config.parameters import default_parameters



class code_generator:

    '''Class that takes various parameters and return a list of synthetically generated scripts of code in various programming languages
    
    custom_prompts : List[str] = problem prompt and solution prompt used to make an LLM generate the scripts. This parameter is used to input custom prompts to use in place of the standard ones.
    prob : List[int] = there are four types of prompts. This parameter is used to change the proportion of the different types.
    share : List[int] = For each of the supported languages, set the proportion of generated snippets of code. It must sum up to 1.
    model : str = LLM model to use in the script generation, the default one is llama 3.1 70b.
    temperatures : List[ int, int] = temperature for problem and solution generation.
    batch_size : int = size of each batch.'''

    def __init__(self, custom_prompts : List[str] = [None, None],
                 prob : List[int] = None,
                  share : List[int] = None,
                  Total_number : int = None,
                    model : str = 'llama-70b',
                      temperatures : List[int] = [None, None],
                        batch_size : int = None,
                        api_key : str = None) -> List[str]:
        
        self.custom_problem_prompt = custom_prompts[0]
        self.custom_solution_prompt = custom_prompts[1]
        self.prob = prob
        self.share = share
        self.Total_number = Total_number
        self.model = model
        self.temperature_problem = temperatures[0]
        self.temperature_solution = temperatures[1]
        self.api_key = api_key
        self.batch_size = batch_size

        #default values of some parameters
        args = default_parameters

        for param, value in vars(self).items():
            if not value:
                if args.get(param, None):
                    setattr(self, param, args[param])

    def change_params(self, prompts: List[str] = [None, None], 
                prob : List[int] = [None, None],
                  share : List[int] = None,
                  Total_number : int = None,
                    model : str = None,
                      temperatures : List[ int] = [None, None],
                        batch_size : int = None,
                        api_key = None):
        '''Changes the values of parameters assigned during the class creation. Parameters that are not inserted will not be changed, so to leave a parameter unchanged either use None as argument
        or do not include the parameter in the function call'''

        for param, value in locals():
            if value:
                setattr(self, param, value)


    def post_process(self, input_string : str) -> str:
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

    def generator(self, batch) -> List[str]:
        """
        Function to generate problem and solution texts along with their tokens for a given batch of data.
        """
        # Create a copy of the batch to avoid SettingWithCopyWarning
        batch = batch.copy()

        if self.custom:
            OSS_problem_prompt, OSS_solution_prompt = self.custom_problem_prompt, self.custom_solution_prompt

        else:
            if self.prob: 
                OSS_problem_prompt, OSS_solution_prompt = random.choices(prompt_list, self.prob)[0]

            else:
                OSS_problem_prompt, OSS_solution_prompt = random.choices(prompt_list, probabilities)[0]

        # Generate problem and solution texts
        batch['problem_text'] = batch['string'].apply(lambda x: problem_text(fun(x), self.api_key, OSS_problem_prompt, 
                                                    model=self.model, temperature=self.temperature_problem))

        batch['solution_text'] = batch.apply(lambda x: solution_text(x['problem_text'], self.api_key, x['language'], OSS_solution_prompt, 
                                            model=self.model, temperature=self.temperature_solution), axis=1)

        # Extract tokens from the generated texts
        batch['problem_tokens'] = batch['problem_text'].apply(lambda x: x[1])
        batch['solution_tokens'] = batch['solution_text'].apply(lambda x: x[1])

        # Extract only the text part, discard the tokens
        batch['problem_text'] = batch['problem_text'].apply(lambda x: x[0])
        batch['solution_text'] = batch['solution_text'].apply(lambda x: x[0])

        # Apply post-processing to extract the main content
        batch['problem_text'] = batch['problem_text'].apply(lambda x: self.post_process(x))
        batch['solution_text'] = batch['solution_text'].apply(lambda x: self.post_process(x))

        return batch

    def generate_training(self, n_jobs : int =None, 
                        test : bool =False) -> DataFrame:
        """
        Main function to generate training data by processing batches of code snippets.
        """
        # Get the initial dataset and preprocess it
        snippets_dataset = get_seed(self.share, self.Total_number)
        snippets_dataset = snippets_dataset.dropna()
        snippets_dataset['string'] = snippets_dataset['string'].apply(lambda x: fun(x))
        snippets_dataset = snippets_dataset.dropna().drop_duplicates(subset='string')

        print("snippets_dataset--->", len(snippets_dataset))

        # Split the dataset into batches
        batch_list = [snippets_dataset[i:i+self.batch_size] for i in range(0, len(snippets_dataset), self.batch_size)]

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
                result = self.generator(batch=batch)
                
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


    def generate(self, custom : bool = False, n_jobs : int = None, test : bool = False) -> DataFrame:

        '''generate a dataframe with code scripts in various languages given the parameter assigned'''

        self.custom = custom

        return self.generate_training(n_jobs, test)
