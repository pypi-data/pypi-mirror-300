from .prompt import OSS_problem_prompt, OSS_solution_prompt
from .complex_prompt import OSS_problem_prompt_complex, OSS_solution_prompt_complex
from .complex_brief_prompt import OSS_problem_prompt_complex_brief, OSS_solution_prompt_complex_brief
from .complex_conversational_prompt import OSS_problem_prompt_complex_conversational, OSS_solution_prompt_complex_conversational


prompt_list = [(OSS_problem_prompt, OSS_solution_prompt), (OSS_problem_prompt_complex, OSS_solution_prompt_complex),
               (OSS_problem_prompt_complex_brief, OSS_solution_prompt_complex_brief), (OSS_problem_prompt_complex_conversational, OSS_solution_prompt_complex_conversational)]

probabilities = [0.1, 0.1, 0.6, 0.2]