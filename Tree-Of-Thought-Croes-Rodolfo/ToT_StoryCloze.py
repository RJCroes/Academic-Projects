import os
import re
import io
import json
import time
import random
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from google.colab import files

# Constants
MODEL_GPT4 = "gpt-4o"
MODEL_GPT35 = "gpt-3.5-turbo"
STORYCLOZE_FORMAT = '"The answer is n" where n is either 1 or 2.'

class GPTWrapper:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.completion_tokens = 0
        self.prompt_tokens = 0

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

    def get_usage(self, model: str = MODEL_GPT4) -> Dict[str, float]:
        cost = 0
        if model == MODEL_GPT4:
            cost = self.completion_tokens / 1000 * 0.0050 + self.prompt_tokens / 1000 * 0.0150
        elif model == MODEL_GPT35:
            cost = self.completion_tokens / 1000 * 0.0005 + self.prompt_tokens / 1000 * 0.0015
        return {
            "completion_tokens": self.completion_tokens,
            "prompt_tokens": self.prompt_tokens,
            "cost": cost
        }

class DataLoader:
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

    @staticmethod
    def task_id_selection(data: List[Any], n_tasks: int) -> List[int]:
        if not isinstance(data, (list, dict)):
            raise TypeError(f"Expected data to be list or dict, but got {type(data)}")
        data_length = len(data)
        n_tasks = min(n_tasks, data_length)
        return random.sample(range(data_length), n_tasks)

    @staticmethod
    def find_matching_elements(data_list: List[Dict[str, Any]], target_ids: List[str]) -> List[int]:
        return [index for index, item in enumerate(data_list) if item['InputStoryid'] in target_ids]

class Solver:
    def __init__(self, gpt_wrapper: GPTWrapper):
        self.gpt = gpt_wrapper

    def io_solver(self, prompt: str, input: str, choice1: str, choice2: str, format: str, 
                  model: str = MODEL_GPT4, temperature: float = 0.7, max_tokens: int = 4096, 
                  n: int = 1, stop: List[str] = None) -> List[str]:
        return self.gpt.chat_completion(
            [{"role": "user", "content": prompt.format(input=input, choice1=choice1, choice2=choice2, format=format)}],
            model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop
        )

    def tot_solver(self, solver_type: str, tot_prompt: str, eval_prompt: str, formats: List[str], 
                   input: str, choice1: str, choice2: str, n_generated_samples: int = 5, 
                   n_evaluation: int = 5, percent_selections: float = 0.20, max_depth: int = 2, 
                   max_steps: int = 25, selection_method: str = 'greedy', 
                   model: str = MODEL_GPT4) -> Dict[str, Any]:
        if solver_type == 'bfs':
            return self.tot_bfs_solver(tot_prompt, eval_prompt, formats, input, choice1, choice2, 
                                       n_generated_samples, n_evaluation, percent_selections, 
                                       max_depth, selection_method, model)
        elif solver_type == 'dfs':
            return self.tot_dfs_solver(tot_prompt, eval_prompt, formats, input, choice1, choice2, 
                                       n_generated_samples, n_evaluation, max_steps, max_depth, 
                                       selection_method, model)
        elif solver_type == 'astar':
            return self.tot_astar_solver(tot_prompt, eval_prompt, formats, input, choice1, choice2, 
                                         n_generated_samples, n_evaluation, percent_selections, 
                                         max_depth, selection_method, model)
        else:
            raise ValueError(f"Invalid solver_type: {solver_type}")

    # Implement tot_bfs_solver, tot_dfs_solver, and tot_astar_solver methods here

class Evaluator:
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

    @staticmethod
    def tasks_scorer(tasks: List[Dict[str, Any]], chosen_tasks: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], str]:
        total_inputs = len(chosen_tasks)
        total_score = 0
        analysis = []

        for i in range(total_inputs):
            ground_truth = int(chosen_tasks[i]['truth'])
            solution = Evaluator.extract_solution(tasks[i]['solution'][0])
            score = 1 if int(ground_truth) == int(solution) else 0
            analysis.append({
                'task_id': tasks[i]['task_id'],
                'ground_truth': ground_truth,
                'generated_solution': solution,
                'score': score
            })
            total_score += score

        average_score = total_score / total_inputs if total_inputs > 0 else 0
        return analysis, f"{average_score:.2f}"

class StoryClozeExperiment:
    def __init__(self, gpt_wrapper: GPTWrapper, data_loader: DataLoader, solver: Solver, evaluator: Evaluator):
        self.gpt_wrapper = gpt_wrapper
        self.data_loader = data_loader
        self.solver = solver
        self.evaluator = evaluator

    def run(self, n_tasks: int, methods: List[str], task_ids: List[str] = None, 
            max_depth: int = 2, max_steps: int = 25, model: str = MODEL_GPT4) -> Dict[str, List[Dict[str, Any]]]:
        data = self.data_loader.load_csv('cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv')
        chosen_task_ids = self.data_loader.find_matching_elements(data, task_ids) if task_ids else self.data_loader.task_id_selection(data, n_tasks)
        chosen_tasks = self._prepare_tasks(data, chosen_task_ids)

        results = {}
        for method in methods:
            tasks = self._solve_tasks(method, chosen_tasks, max_depth, max_steps, model)
            self._save_results(method, tasks, chosen_tasks)
            results[method] = tasks

        print("All results have been saved to files.")
        return results

    def _prepare_tasks(self, data: List[Dict[str, Any]], chosen_task_ids: List[int]) -> List[Dict[str, Any]]:
        chosen_tasks = []
        for i in chosen_task_ids:
            try:
                chosen_tasks.append({
                    'task_id': data[i]['InputStoryid'],
                    'task': ' '.join([data[i][f"InputSentence{j}"] for j in range(1, 5)]),
                    'choice1': data[i]["RandomFifthSentenceQuiz1"],
                    'choice2': data[i]["RandomFifthSentenceQuiz2"],
                    'truth': data[i]["AnswerRightEnding"]
                })
            except Exception as e:
                print(f"Error processing task {i}: {str(e)}")
        return chosen_tasks

    def _solve_tasks(self, method: str, chosen_tasks: List[Dict[str, Any]], 
                     max_depth: int, max_steps: int, model: str) -> List[Dict[str, Any]]:
        # Implement task solving logic for different methods
        pass

    def _save_results(self, method: str, tasks: List[Dict[str, Any]], 
                      chosen_tasks: List[Dict[str, Any]]) -> None:
        # Implement result saving logic
        pass

# Usage
api_key = os.environ.get("OPENAI_API_KEY")
gpt_wrapper = GPTWrapper(api_key)
data_loader = DataLoader()
solver = Solver(gpt_wrapper)
evaluator = Evaluator()
experiment = StoryClozeExperiment(gpt_wrapper, data_loader, solver, evaluator)

results = experiment.run(
    n_tasks=20,
    methods=['tot_astar_greedy', 'tot_astar_sample'],
    task_ids=['2685ba6d-8b1c-462c-af50-ae5381d64172', '900e1a7a-c221-4b15-9998-750301bd6a31', ...],
    max_depth=2,
    max_steps=10,
    model=MODEL_GPT35
)