# Imports
import os
import re
import io
import json
import time
import random
import numpy as np
import pandas as pd
import math
import heapq
from openai import OpenAI
from typing import List, Dict, Any, Tuple

# Constants
MODEL_GPT4 = "gpt-4o"
MODEL_GPT35 = "gpt-3.5-turbo"

# Prompts
# Answer format of new tasks
STORYCLOZE_FORMAT = '"The answer is n" where n is either 1 or 2.'
# Zero-shot IO prompt
IO_PROMPT ='''Given a body of text with an open ending,
determine which of the two endings makes the most sense to complete the text.
Example input structure:
Body of Text: {input}
Choice 1: {choice1}
Choice 2: {choice2}
Example output sturcture:
Answer:
Your answer after analyzing each choice. The last line should end with {format}.
Do not add any more text after this.
'''
# Thought prompt for zero-shot tot
TOT_PROMPT ='''Given a body of text with an open ending,
Analyse two endings to the text and determine which one makes the most sense to complete the text with.
Example input structure:
Body of Text: {input}
Choice 1: {choice1}
Choice 2: {choice2}
Your output should be of the following format: \n{format}
'''
# Formats for ToT with storycloze
ANALYSIS_FORMAT = '''Analysis:
Your analysis from each choice mentioned with respect to the input. You should not mention your selection, only the analysis of each choice.
'''
ANSWER_FORMAT = '''Answer:
Your answer to the question using the given analysis. It should end with {format}.
Do not add any more text after this
'''
# Zero-shot voting used for tot bfs
VOTE_PROMPT = '''Given an instruction and several thoughts,
decide which choice is most promising.
Critically analyze each choice in detail, then conclude in the last line
"The best choice is {s}", where s the integer id of the choice.
Do not add any more text after this.
'''
# Few-shot valuation prompt used for tot dfs
VALUE_PROMPT = '''Given an instruction and several thoughts, independently evaluate how well the given thoughts could potentially lead to selecting the correct solution.
For each thought and only thoughts, provide an analysis of how confident the thought sounds when answering the instruction.
Then conclude in the last line:
a single-word evaluation. Use only one of these evaluations: IMPOSSIBLE, MAYBE, SURE, or SOLUTION.
Only use SOLUTION if the thought contains the exact solution in this format: {format}

Example output structure:
Thought 1: [Your analysis here]
MAYBE

Thought 2: [Your analysis here]
IMPOSSIBLE

Thought 3: [Your analysis here]
SURE

Thought 4: [Your analysis here]
SOLUTION
Thought 5: [Your analysis here]
SURE

Ensure that your response ends with one of the four evaluation words on its own line for each choice.
'''
# Few-shot Heuristic prompt
HEURISTIC_PROMPT = ''' Given a task and a thought,
Value how close the thought is to a complete solution of the task from a scale of 0 to 1.
The score should also consider if the logical steps taken by the thought are correct and in line with the task's logical steps.
conclude your answer in the last line
"s", where s the numerical value you gave the thought as a float with 2 decimal point.
Do not add any more text after this.

Example input structure:
Task: [inputted task here]
Thought: [inputed thought here]

Example output structure:
0.25

Task: {task}
Thought: {thought}
'''

# Setup Tools & Functions for OpenAI API usage
class GPTWrapper:
    # Self Initialization
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.completion_tokens = 0
        self.prompt_tokens = 0
    # Chat Completion & Token usage updater
    def chat_completion(self, messages: List[Dict[str, str]], model: str = MODEL_GPT4, 
                        temperature: float = 0.7, max_tokens: int = 4096, n: int = 1, 
                        stop: List[str] = None) -> List[str]:
        outputs = []
        for _ in range(0, n, 20):
            cnt = min(n - len(outputs), 20)
            res = self.client.chat.completions.create(
                model=model, messages=messages, temperature=temperature,
                max_tokens=max_tokens, n=cnt, stop=stop
            )
            outputs.extend([choice.message.content for choice in res.choices])
            self.prompt_tokens += res.usage.prompt_tokens
            self.completion_tokens += res.usage.completion_tokens
        return outputs
    # Cost Determination (updated 27/03/2025)
    def get_usage(self, model: str = MODEL_GPT4) -> Dict[str, float]:
        cost = 0
        if model == MODEL_GPT4:
            cost = self.completion_tokens / 1000000 * 2.50 + self.prompt_tokens / 1000000 * 10.00
        elif model == MODEL_GPT35:
            cost = self.completion_tokens / 1000000 * 0.50 + self.prompt_tokens / 1000000 * 1.50
        return {
            "completion_tokens": self.completion_tokens,
            "prompt_tokens": self.prompt_tokens,
            "cost": cost
        }
# Task Solvers
class TaskSolver:
    # Self Initialization
    def __init__(self, gpt_wrapper: GPTWrapper):
        self.gpt = gpt_wrapper

    # General Solving for multiple Tasks
    def solve(self, method: str, tasks: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        global MODEL_GPT4, IO_PROMPT, STORYCLOZE_FORMAT, TOT_PROMPT, VOTE_PROMPT, VALUE_PROMPT, ANALYSIS_FORMAT, ANSWER_FORMAT
        outputs = []
        # Determine the solver function and add appropriate prompt/template parameters.
        for task_info in tasks:
            # Based on the method, select the solver and inject needed prompts/templates.
            if method == "io":
                solver_func = self.io_solver
                kwargs.setdefault("prompt", IO_PROMPT)
                kwargs.setdefault("format", STORYCLOZE_FORMAT)
            elif method == "tot_bfs":
                solver_func = self.tot_bfs_solver
                kwargs.setdefault("tot_prompt", TOT_PROMPT)
                kwargs.setdefault("eval_prompt", VOTE_PROMPT)
                kwargs.setdefault("formats", [ANALYSIS_FORMAT, ANSWER_FORMAT.format(format=STORYCLOZE_FORMAT)])
            elif method == "tot_dfs":
                solver_func = self.tot_dfs_solver
                kwargs.setdefault("tot_prompt", TOT_PROMPT)
                kwargs.setdefault("eval_prompt", VALUE_PROMPT)
                kwargs.setdefault("formats", [ANALYSIS_FORMAT, ANSWER_FORMAT.format(format=STORYCLOZE_FORMAT)])
            elif method == "tot_astar":
                solver_func = self.tot_astar_solver
                kwargs.setdefault("tot_prompt", TOT_PROMPT)
                kwargs.setdefault("eval_prompt", VOTE_PROMPT)
                kwargs.setdefault("formats", [ANALYSIS_FORMAT, ANSWER_FORMAT.format(format=STORYCLOZE_FORMAT)])
            else:
                raise ValueError(f"Unknown solving method: {method}")
            
            # Call the appropriate solver for the current task.
            solution = solver_func(task_info['task'], task_info['choice1'], task_info['choice2'], **kwargs)
            # Handle the solution generated
            outputs.append({
                'task_id': task_info['task_id'],
                'task': task_info['task'],
                'choice1': task_info['choice1'],
                'choice2': task_info['choice2'],
                'solution': solution,
                'usage_so_far': self.gpt.get_usage(kwargs.get('model', MODEL_GPT4))
            })
        return outputs

    # Input-Output Prompt
    def io_solver(self, input: str, choice1: str, choice2: str, prompt: str, format: str, 
                  model: str = MODEL_GPT4, temperature: float = 0.7, max_tokens: int = 4096, 
                  n: int = 1, stop: List[str] = None) -> List[str]:
        return self.gpt.chat_completion(
            [{"role": "user", "content": prompt.format(input=input, choice1=choice1, choice2=choice2, format=format)}],
            model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop
        )

    # Tree of Thought using Breadth First Search
    def tot_bfs_solver(self, input_text: str, choice1: str, choice2: str, tot_prompt: str, eval_prompt: str, formats: List[str],
                       n_generated_samples: int = 5, n_evaluation: int = 5, percent_selections: float = 0.20,
                       max_depth: int = 2, selection_method: str = 'greedy', model: str = MODEL_GPT4,
                       temperature: float = 0.7, max_tokens: int = 4096, stop: List[str] = None) -> Dict[str, Any]:
        outputs = {"steps": [], "solution": [], "reached_max_depth": True}
        current_outputs = ['']
        step = 0

        while step < max_depth:
            # Update prompt format to match step in solving problem
            current_format = formats[step] if current_outputs[0] != '' else formats[0]
            current_prompt = tot_prompt.format(input=input_text, choice1=choice1, choice2=choice2, format=current_format)

            # Generate thoughts using GPT
            thoughts = self.gpt.chat_completion(
                [{"role": "user", "content": current_prompt}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_generated_samples, stop=stop
            )
            
            # Self evaluate thoughts
            eval_prompt_full = eval_prompt + f'\nInstruction: {input_text}\n' + "\n".join(
                [f'Choice {i+1}:\n{thought}' for i, thought in enumerate(thoughts)]
            )
            votes = self.gpt.chat_completion(
                [{"role": "user", "content": eval_prompt_full}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_evaluation, stop=stop
            )
            # Extract votes from generated thoughts
            vote_results = self.extract_votes(votes, n_generated_samples)
            # Thoughts selected for next exploration
            selected_new_thoughts = self.select_thoughts(thoughts, vote_results, percent_selections, selection_method)
            
            # Save the current selected thoughts to the current output
            outputs['steps'].append({
                'step': step,
                'input': input_text,
                'choice1': choice1,
                'choice2': choice2,
                'current_thoughts': current_outputs,
                'generated_thoughts': thoughts,
                'vote_results': vote_results,
                'selected_new_thoughts': selected_new_thoughts
            })
            
            current_outputs = selected_new_thoughts
            step += 1

        outputs['solution'] = current_outputs
        return outputs

    # Tree of Thought using Depth First Search    
    def tot_dfs_solver(self, input_text: str, choice1: str, choice2: str, tot_prompt: str, eval_prompt: str, formats: List[str],
                       n_generated_samples: int = 5, n_evaluation: int = 5, max_steps: int = 25,
                       max_depth: int = None, selection_method: str = 'greedy', model: str = MODEL_GPT4,
                       temperature: float = 0.7, max_tokens: int = 4096, stop: List[str] = None) -> Dict[str, Any]:
        outputs = {"steps": [], "solution": [], "deepest_depth": -1, "steps_taken": 0}
        deepest_state = {"depth": -1, "thought": "", "step": -1}
        steps_taken = 0
        unanimous_solution = None
        # Depth First Search Recursion
        def dfs(depth: int, current_output: str):
            nonlocal steps_taken, deepest_state, unanimous_solution
            # Return if we reached max depth or if max steps are exhausted
            if steps_taken >= max_steps or (max_depth is not None and depth >= max_depth) or unanimous_solution is not None:
                return
            # Update prompt format to match depth in solving problem
            current_format = current_output + formats[min(depth, len(formats)-1)] if current_output else formats[0]
            current_prompt = tot_prompt.format(input=input_text, choice1=choice1, choice2=choice2, format=current_format)
            # Thought Generation
            thoughts = self.gpt.chat_completion(
                [{"role": "user", "content": current_prompt}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_generated_samples, stop=stop
            )
            # Self Evaluation
            eval_prompt_full = eval_prompt + f'\nInstruction: {input_text}\n\nChoice 1: {choice1}\nChoice 2: {choice2}' + "\n".join(
                [f'Thought {i+1}:\n{thought}' for i, thought in enumerate(thoughts)]
            )
            values = self.gpt.chat_completion(
                [{"role": "user", "content": eval_prompt_full}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_evaluation, stop=stop
            )
            # Extract and sum values from generated evaluations
            value_results, unanimous_solution = self.extract_values(values, n_generated_samples)
            # Save current step
            outputs['steps'].append({
                'depth': depth,
                'input': input_text,
                'choice1': choice1,
                'choice2': choice2,
                'current_thought': current_output,
                'generated_thoughts': thoughts,
                'values': value_results,
                'unanimous_solution': unanimous_solution
            })
            # Update Deepest State Explored
            if depth > deepest_state['depth']:
                deepest_state.update({'depth': depth, 'thought': thoughts[0], 'step': steps_taken})
            # Determine the order of exploration based on the selection method
            if selection_method == 'greedy':
                exploration_order = sorted(range(len(thoughts)), key=lambda i: value_results[i], reverse=True)
            else:
                value_results_array = np.array(value_results, dtype=float)
                probabilities = (value_results_array + 1e-8) / np.sum(value_results_array + 1e-8)
                exploration_order = np.random.choice(len(thoughts), len(thoughts), p=probabilities, replace=False).tolist()
            # Explore thoughts in the determined order (DFS characteristic)
            for i in exploration_order:
                if value_results[i] > 1e-8 and steps_taken < max_steps:
                    steps_taken += 1
                    dfs(depth + 1, thoughts[i])
        
        dfs(0, '')
        outputs['solution'] = [deepest_state['thought']]
        outputs['deepest_depth'] = deepest_state['depth']
        outputs['steps_taken'] = steps_taken
        return outputs

    # Tree of Thought using A* Search
    def tot_astar_solver(self, input_text: str, choice1: str, choice2: str, tot_prompt: str, eval_prompt: str, formats: List[str],
                         n_generated_samples: int = 5, n_evaluation: int = 5, percent_selections: float = 0.20,
                         max_depth: int = 2, selection_method: str = 'greedy', model: str = MODEL_GPT4,
                         temperature: float = 0.7, max_tokens: int = 4096, stop: List[str] = None) -> Dict[str, Any]:
        outputs = {}
        tot_outputs = []
        open_list = [(0, 0, '', 0)] # Cells to be visited (f_cost, g_cost, thought, step)
        closed_set = set() # Visited Nodes
        n_selections = math.ceil(percent_selections * n_generated_samples)
        best_solutions = [] # Store the best thoughts at max_depth
        # Search continues until open list is empty
        while open_list:
            # Pop the cell with the smallest f cost (cell potentially has solution)
            f, g, current_thought, step = heapq.heappop(open_list)
            # Save a thought as a potential solution when a max depth is reached
            if step == max_depth:
                best_solutions.append((f, current_thought))
                continue
            # Ensure for no double checking states
            if (current_thought, step) in closed_set:
                continue
            # Add the current thought to the visited nodes
            closed_set.add((current_thought, step))
            # Expand node from here
            # Update prompt format to match step in solving problem
            current_format = current_thought + formats[min(step, len(formats)-1)] if current_thought else formats[0]
            current_prompt = tot_prompt.format(input=input_text, choice1=choice1, choice2=choice2, format=current_format)
            # Thoughts Generation
            thoughts = self.gpt.chat_completion(
                [{"role": "user", "content": current_prompt}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_generated_samples, stop=stop
            )
            # Self Evaluation
            eval_prompt_full = eval_prompt + f'\nInstruction: {input_text}\n\nChoice 1: {choice1}\nChoice 2: {choice2}' + "\n".join(
                [f'Thought {i+1}:\n{thought}' for i, thought in enumerate(thoughts)]
            )
            votes = self.gpt.chat_completion(
                [{"role": "user", "content": eval_prompt_full}],
                model=model, temperature=temperature, max_tokens=max_tokens, n=n_evaluation, stop=stop
            )
            # Extract votes from generated thoughts
            vote_results = self.extract_votes(votes, n_generated_samples)
            # Thoughts selected for next exploration
            selected_new_thoughts = self.select_thoughts(thoughts, vote_results, percent_selections, selection_method)
            
            tot_outputs.append({
                'step': step,
                'input': input_text,
                'choice1': choice1,
                'choice2': choice2,
                'current thought': current_thought,
                'generated thoughts': thoughts,
                'values': vote_results,
                'selected_new_thoughts': selected_new_thoughts
            })
            # If a state is not in the visited steps, add it to the current stack
            for thought in selected_new_thoughts:
                if (thought, step + 1) not in closed_set:
                    # Calculate f, g and h values for new unexplored thought
                    new_g = g + self.a_cost(thought, step)
                    new_h = self.a_heuristic(input_text, thought, model=model)
                    new_f = new_g + new_h
                    # Put the new thought(s) into the heap for further exploration
                    heapq.heappush(open_list, (new_f, new_g, thought, step + 1))
        # Save the output
        outputs['steps'] = tot_outputs
        if best_solutions:
            # Sort the best solutions by f_cost and select the best one
            best_solutions.sort(key=lambda x: x[0])
            best_final_solution = best_solutions[0][1]
            outputs['solution'] = [best_final_solution]
            outputs['reached_max_depth'] = True
        else:
            # No solution found within max_depth
            outputs['solution'] = ''
            outputs['reached_max_depth'] = False
        return outputs

    # Extracts numerical votes from GPT output using regex pattern matching.
    def extract_votes(self, votes: List[str], n_strategies: int) -> List[int]:
        pattern = r".*best choice is .*(\d+).*"
        vote_results = [0] * n_strategies  # Initialize vote_results with n_strategies elements
        
        for v in votes:
            match = re.match(pattern, v, re.DOTALL)  # Pattern matching using regex
            if match:
                try:
                    vote = int(match.groups()[0]) - 1  # Convert to 0-indexed integer
                    if 0 <= vote < n_strategies:
                        vote_results[vote] += 1
                    else:
                        print(f"Invalid vote index: {vote + 1} (0-indexed: {vote}) in response: {v}")
                except ValueError:
                    print(f"Invalid vote format in response: {v}")
            else:
                print(f"No match found in {v}")
        
        return vote_results

    # Extract the value results defined in the map from generated evaluations
    def extract_values(self, evaluations: List[str], n_strategies: int):
        value_map = {"impossible": 0, "maybe": 3, "sure": 6, "solution": 9}
        # Initialize all choices
        summed_values = {i: 0 for i in range(1, n_strategies + 1)}
        solution_counts = {i: 0 for i in range(1, n_strategies + 1)}
        total_evaluations = len(evaluations)
        # Regex to extract all values
        for evaluation in evaluations:
            choices = re.findall(r'Choice (\d+):.*?\n(IMPOSSIBLE|MAYBE|SURE|SOLUTION)', evaluation, re.DOTALL | re.IGNORECASE)
            for choice_num, choice_eval in choices:
                choice_num = int(choice_num)
                if 1 <= choice_num <= n_strategies: # Ensure choice_num is within valid range
                    summed_values[choice_num] += value_map.get(choice_eval.lower(), 0) # Assing valuation from map
                    if choice_eval.lower() == "solution":
                        solution_counts[choice_num] += 1
        # Convert the dictionary to a list, ensuring all choices are represented
        value_results = [summed_values[i] for i in range(1, n_strategies + 1)]
        # Check if any solution was unanimously found (if all evaluation runs determine that this is a solution)
        unanimous_solution = next((i for i in range(1, n_strategies + 1) if solution_counts[i] == total_evaluations), None)
        return value_results, unanimous_solution

    # Selects thoughts based on voting results and selection strategy.
    def select_thoughts(self, thoughts: List[str], vote_results: List[int], percent_selections: float, 
                        selection_method: str) -> List[str]:
        
        n_selections = max(1, math.ceil(percent_selections * len(thoughts)))
        ids = list(range(len(thoughts)))
        # Best stays
        if selection_method == 'greedy':
            select_ids = sorted(ids, key=lambda x: vote_results[x], reverse=True)[:n_selections]
        # Controlled randomness 
        elif selection_method == 'sample':
            # Ensure non-zero probabilities by introducing epsilon
            # If Impossible states are explored because of this,
            # they can be pruned with the next evaluations
            adjusted_votes = np.array(vote_results) + 1e-8
            # Probability Calculations
            probabilities = adjusted_votes / adjusted_votes.sum()
            # Controlled random selection
            select_ids = np.random.choice(ids, n_selections, p=probabilities, replace=False).tolist()
        else:
            raise ValueError("Invalid selection method")
        return [thoughts[i] for i in select_ids]

    # Cost function for A star using lenght of text and step count
    def a_cost(self, thought: str, step: int) -> float:
        return step * 0.5 + len(thought.split()) * 0.05

    # Heuristic function for A star using GPT valuation
    def a_heuristic(self, task: str, thought: str, model: str = MODEL_GPT4, temperature: float = 0.7, 
                max_tokens: int = 4096, stop: List[str] = None) -> float:
        # Evaluation Generation
        global HEURISTIC_PROMPT
        heuristic_prompt_full = HEURISTIC_PROMPT.format(task=task, thought=thought)
        prompt_result = self.gpt.chat_completion(
            [{"role": "user", "content": heuristic_prompt_full}],
            model=model, temperature=temperature, max_tokens=max_tokens, n=1, stop=stop
        )
        response = prompt_result[0].strip()
        # Use regex to extract the numeric value at the end of the response.
        match = re.search(r"([-+]?\d*\.\d+|\d+)\.?$", response)
        if match:
            try:
                score = float(match.group(1))
            except ValueError:
                print(f"Error converting extracted number '{match.group(1)}' to float from response: {response}")
                score = 0.0
        else:
            print(f"No numeric score found in response: {response}")
            score = 0.0

        return 1 - score

class Evaluator:
    # Self Initialization
    def __init__(self, gpt_wrapper: GPTWrapper):
        self.gpt = gpt_wrapper
    # Function to Log Results and Metrics
    # Writes out data to JSON file and results to TXT file
    def print_results(self, start_t: float, end_t: float, chosen_tasks: List[Dict[str, Any]],
                      solved_tasks: List[Dict[str, Any]], filename: str = 'results.txt',
                      model: str = MODEL_GPT4):
        output = io.StringIO()

        print(f"Number of tasks: {len(chosen_tasks)}", file=output)
        print(f"Number of solved tasks: {len(solved_tasks)}", file=output)
        for i in solved_tasks:
            print(f"Story {i.get('task_id')}: {i.get('task')}", file=output)
            print(f"Choice 1: {i.get('choice1')}", file=output)
            print(f"Choice 2: {i.get('choice2')}", file=output)
            print(f"Solution: {i.get('solution')}", file=output)
        print(f"Run time: {end_t - start_t} seconds", file=output)
        print(f"GPT usage cost so far: {self.gpt.get_usage(model=model)}", file=output)

        accuracy = Evaluator.tasks_scorer(solved_tasks, chosen_tasks)
        print(f"Solutions accuracy: {accuracy}", file=output)
        print("\n", file=output)

        output_str = output.getvalue()

        # Reset tokens on the GPTWrapper instance before self-evaluation
        self.gpt.completion_tokens = 0
        self.gpt.prompt_tokens = 0

        with open(filename, 'w') as f:
            f.write(output_str)

        # Optional: if running in an environment (e.g., Colab) that supports file downloads
        try:
            from google.colab import files
            files.download(filename)
        except ImportError:
            pass

    # Function that extracts the answer from a generated solution    
    @staticmethod
    def extract_solution(response: str) -> int:
        pattern = r".*answer is .*(\\d+).*"
        match = re.match(pattern, response, re.DOTALL)
        if match:
            extracted = match.groups()[0]
            score = int(extracted)
            if 1 <= score <= 2:
                return score
        return None
        
    # Comparison Evaluation as Metric
    @staticmethod
    def tasks_scorer(tasks: List[Dict[str, Any]], chosen_tasks: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], str]:
        total_inputs = len(chosen_tasks)
        total_score = 0
        analysis = []

        for i in range(total_inputs):
            try:
                # Attempt to convert the truth value to int
                truth_value = chosen_tasks[i].get('truth')
                if truth_value is None:
                    raise TypeError("Truth value is None")
                ground_truth = int(truth_value)
            except (TypeError, ValueError):
                # Set a default value if conversion fails
                ground_truth = 0

            # Safely retrieve solution_raw:
            solution_raw = None
            solution_field = tasks[i].get('solution')
            if isinstance(solution_field, list) and solution_field:
                solution_raw = solution_field[0]
            # If 'solution' might be stored differently (e.g., as a dict), add handling here:
            elif isinstance(solution_field, dict):
                # Try to retrieve using key 0, or adjust based on your data structure.
                solution_raw = solution_field.get(0)

            try:
                solution = Evaluator.extract_solution(solution_raw)
                solution_int = int(solution)
            except (TypeError, ValueError):
                solution_int = 0
                solution = None

            score = 1 if ground_truth == solution_int else 0
            analysis.append({
                'task_id': tasks[i].get('task_id'),
                'ground_truth': ground_truth,
                'generated_solution': solution,
                'score': score
            })
            total_score += score

        average_score = total_score / total_inputs if total_inputs > 0 else 0
        return analysis, f"{average_score:.2f}"


# Data Loader and Task Allocation
class DataLoader:
    # Load in csv file
    @staticmethod
    def load_csv(file_name: str) -> List[Dict[str, Any]]:
        df = pd.read_csv(file_name, dtype={
            "InputStoryId": str,
            "InputSentence1": str,
            "InputSentence2": str,
            "InputSentence3": str,
            "InputSentence4": str,
            "RandomFifthSentenceQuiz1": str,
            "RandomFifthSentenceQuiz2": str,
            "AnswerRightEnding": int
        })
        return df.to_dict(orient='records')

    # Task selection
    @staticmethod
    def task_id_selection(data: List[Any], n_tasks: int) -> List[int]:
        if not isinstance(data, (list, dict)):
            raise TypeError(f"Expected data to be list or dict, but got {type(data)}")
        data_length = len(data)
        n_tasks = min(n_tasks, data_length)
        return random.sample(range(data_length), n_tasks)
    
    # Find the matching element in data that corresponds with story id
    @staticmethod
    def find_matching_elements(data_list: List[Dict[str, Any]], target_ids: List[str]) -> List[int]:
        return [index for index, item in enumerate(data_list) if item['InputStoryid'] in target_ids]

    # Reformat raw data into a chosen tasks list, differing by dataset type
    @staticmethod
    def prepare_tasks(data: List[Dict[str, Any]], chosen_task_ids: List[int]) -> List[Dict[str, Any]]:
        chosen_tasks = []
        for i in chosen_task_ids:
            try:
                chosen_tasks.append({
                    'task_id': data[i]['InputStoryid'],
                    'task': data[i]["InputSentence1"] + " " + data[i]["InputSentence2"] + " " + data[i]["InputSentence3"] + " " + data[i]["InputSentence4"],
                    'choice1': data[i]["RandomFifthSentenceQuiz1"],
                    'choice2': data[i]["RandomFifthSentenceQuiz2"],
                    'truth': data[i]["AnswerRightEnding"]
                })
            except Exception as e:
                print(f"Error processing task {i}: {str(e)}")
                print(f"Data at index {i}: {data[i] if i < len(data) else 'Index out of range'}")
        return chosen_tasks

# run_experiment Function
def run_experiment(n_tasks: int, 
                   methods: List[str] = ['io', 'tot_bfs_greedy', 'tot_bfs_sample', 
                                         'tot_dfs_greedy', 'tot_dfs_sample', 
                                         'tot_astar_greedy', 'tot_astar_sample'],
                   task_ids: List[int] = None, max_depth: int = 2, max_steps: int = 25, 
                   model: str = MODEL_GPT4, return_results: bool = False):
    # Load in dataset
    data = DataLoader.load_csv('cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv')
    # Decide which task IDs to use
    if task_ids is not None:
        chosen_task_ids = DataLoader.find_matching_elements(data, task_ids)
        n_tasks = len(chosen_task_ids)
    else:
        if n_tasks == 0 or n_tasks > len(data):
            n_tasks = len(data)
        
    chosen_task_ids = DataLoader.task_id_selection(data, n_tasks)

    # Prepare chosen tasks in the required structure
    chosen_tasks = DataLoader.prepare_tasks(data, chosen_task_ids)

    # Dictionary to store results for each method
    results = {}

    # For each method, run the appropriate solver
    for method in methods:
        # Reset token counters (if applicable)
        # (Assuming token counters are reset within the solver functions or via a GPTWrapper instance)
        start_t = time.time()
    
        if method.startswith('io'):
            solver_method = "io"
            filename = 'io_results.txt'
            json_filename = 'io_data.json'
            # IO solver does not require a selection method
            solved_tasks = task_solver.solve(solver_method, chosen_tasks, model=model)
        elif method.startswith('tot_bfs'):
            solver_method = "tot_bfs"
            selection_method = "greedy" if method.endswith("greedy") else "sample"
            filename = f'tot_bfs_{selection_method}_results.txt'
            json_filename = f'tot_bfs_{selection_method}_data.json'
            solved_tasks = task_solver.solve(solver_method, chosen_tasks,
                                         selection_method=selection_method,
                                         max_depth=max_depth,
                                         model=model)
        elif method.startswith('tot_dfs'):
            solver_method = "tot_dfs"
            selection_method = "greedy" if method.endswith("greedy") else "sample"
            filename = f'tot_dfs_{selection_method}_results.txt'
            json_filename = f'tot_dfs_{selection_method}_data.json'
            solved_tasks = task_solver.solve(solver_method, chosen_tasks,
                                         selection_method=selection_method,
                                         max_depth=max_depth,
                                         max_steps=max_steps,
                                         model=model)
        elif method.startswith('tot_astar'):
            solver_method = "tot_astar"
            selection_method = "greedy" if method.endswith("greedy") else "sample"
            filename = f'tot_astar_{selection_method}_results.txt'
            json_filename = f'tot_astar_{selection_method}_data.json'
            solved_tasks = task_solver.solve(solver_method, chosen_tasks,
                                         selection_method=selection_method,
                                         max_depth=max_depth,
                                         model=model)
        else:
            print(f"Unknown method: {method}")
            continue

        end_t = time.time()
        # Log and evaluate results 
        evaluator.print_results(start_t, end_t, chosen_tasks, solved_tasks, filename=filename)
        
        # Save results to JSON
        with open(json_filename, "w") as final:
            json.dump(solved_tasks, final)
        try:
            from google.colab import files
            files.download(json_filename)
        except ImportError:
            pass

        results[method] = solved_tasks

    print("All results have been saved to files.")
    if return_results:
        return results

# Usage
if __name__ == "__main__":
    # Create the GPTWrapper instance using your API key.
    api_key = os.environ.get("OPENAI_API_KEY")
    # Initializations of classes
    gpt_wrapper = GPTWrapper(api_key)
    task_solver = TaskSolver(gpt_wrapper)
    evaluator = Evaluator(gpt_wrapper)
    # Run the experiment with the desired parameters.
    run_experiment(1, model=MODEL_GPT35, max_depth=2, max_steps=10)