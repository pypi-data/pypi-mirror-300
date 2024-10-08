from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

#---------------------------------------------------------------------------------------------
# PROBLEM PROMPT
#---------------------------------------------------------------------------------------------

OSS_problem_template_1 = """
You are exceptionally skilled at crafting high-quality programming problems.
Please gain inspiration from the following random code snippet to create a high-quality programming problem.

Present your output in: [Problem Description]
"""

OSS_problem_template_2 = """
Code snippet for inspiration:
```
{code}
```

Guidelines for each section:
[Problem Description]: This should be **completely self-contained**, providing all the contextual information one needs to understand and solve the problem. Assume common programming knowledge, but ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included.
"""

OSS_problem_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_problem_template_1),
        HumanMessagePromptTemplate.from_template(OSS_problem_template_2),
    ]
)

#---------------------------------------------------------------------------------------------
# SOLUTION PROMPT
#---------------------------------------------------------------------------------------------

OSS_solution_template_1 = """
You are exceptionally skilled at offering precise coding solutions to high-quality programming problems.
Inlude necessary comments but avoid introductory phrases such as "Here is the solution."

Present your output in: [Solution]
"""

OSS_solution_template_2 = """
```
{problem}
```

Guidelines for each section:
[Solution]: Offer a comprehensive and **correct** coding solution that accurately addresses the [Problem Description]. Try to solve it with {language}
"""

OSS_solution_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_solution_template_1),
        HumanMessagePromptTemplate.from_template(OSS_solution_template_2),
    ]
)
OSS_solution_prompt