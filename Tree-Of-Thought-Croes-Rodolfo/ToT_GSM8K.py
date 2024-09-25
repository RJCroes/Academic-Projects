# Imports
import os
import re
import json
import time
import random
import numpy as np
from openai import OpenAI
from typing import List, Dict, Any, Tuple

# Constants
MODEL_GPT4 = "gpt-4o"
MODEL_GPT35 = "gpt-3.5-turbo"

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
    def load_jsonlines(file_name: str) -> List[Dict[str, Any]]:
        with open(file_name, 'r') as f:
            return [json.loads(line) for line in f]

    @staticmethod
    def rank_questions(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        def analyze_question(question_data: Dict[str, str]) -> float:
            question = question_data["question"]
            answer = question_data["answer"]
            score = (len(question.split()) * 0.1 +
                     len(re.findall(r'\d+', question)) * 0.5 +
                     len(answer.split()) * 0.05 +
                     len(re.findall(r'\d+', answer)) * 0.25 +
                     len(re.findall(r'[+\-*/]', answer)) * 1)
            return score

        scored_questions = [(i, q, analyze_question(q)) for i, q in enumerate(questions)]
        return [q for _, q, _ in sorted(scored_questions, key=lambda x: x[2], reverse=True)]

    @staticmethod
    def task_id_selection(data: List[Any], n_tasks: int) -> List[int]:
        if not isinstance(data, (list, dict)):
            raise TypeError(f"Expected data to be list or dict, but got {type(data)}")
        data_length = len(data)
        n_tasks = min(n_tasks, data_length)
        return random.sample(range(data_length), n_tasks)

class Solver:
    def __init__(self, gpt_wrapper: GPTWrapper):
        self.gpt = gpt_wrapper

    def io_solver(self, prompt: str, input: str, format: str, model: str = MODEL_GPT4, 
                  temperature: float = 0.7, max_tokens: int = 4096, n: int = 1, 
                  stop: List[str] = None) -> List[str]:
        return self.gpt.chat_completion(
            [{"role": "user", "content": prompt.format(input=input, format=format)}],
            model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop
        )

    # Implement other solver methods (tot_bfs_solver, tot_dfs_solver, tot_astar_solver) here

class Evaluator:
    @staticmethod
    def extract_solution(response: str) -> float:
        pattern = r".*answer is\s*([-+]?\d*\.?\d+)"
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                print(f"Error converting '{match.group(1)}' to float")
        print("Error when extracting solution")
        return None

    @staticmethod
    def comparison_scorer(tasks: List[Dict[str, Any]], chosen_tasks: List[Dict[str, Any]], 
                          data: str) -> Tuple[List[Dict[str, Any]], str]:
        total_inputs = len(chosen_tasks)
        total_score = 0
        analysis = []

        for i in range(total_inputs):
            task = chosen_tasks[i]['task']
            ground_truth = float(chosen_tasks[i]['truth']) if data == 'gsmhard' else int(chosen_tasks[i]['truth'].split()[-1])
            solution = Evaluator.extract_solution(tasks[i]['solution'][0])

            if solution is None:
                print(f"Error: Solution is none instead of a number for: {task}")
                continue

            score = 1 if abs(ground_truth - solution) <= 0.1 else 0
            analysis.append({
                'task_id': tasks[i]['task_id'],
                'ground_truth': ground_truth,
                'generated_solution': solution,
                'score': score
            })
            total_score += score

        accuracy = f"{total_score / total_inputs:.2f}" if total_inputs > 0 else "0.00"
        return analysis, accuracy

# Main execution function
def run_experiment(dataset: str, n_tasks: int, ranked: bool = False, 
                   methods: List[str] = ['io', 'tot_bfs_greedy', 'tot_bfs_sample', 
                                         'tot_dfs_greedy', 'tot_dfs_sample', 
                                         'tot_astar_greedy', 'tot_astar_sample'],
                   task_ids: List[int] = None, max_depth: int = 2, max_steps: int = 25, 
                   model: str = MODEL_GPT4):
    # Implementation of the main experiment runner
    pass

# Example usage
if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY")
    gpt_wrapper = GPTWrapper(api_key)
    run_experiment("gsm8k", 20, ranked=True, methods=['tot_astar_greedy', 'tot_astar_sample'], 
                   model=MODEL_GPT35, max_depth=2, max_steps=10)