# Tree of Thought Experiments

This repository contains implementations of the Tree of Thought (ToT) approach for problem-solving using large language models. The experiments are conducted on two datasets: GSM8K (math word problems) and StoryCloze (story completion tasks).

## Files

1. `tot_gsm8k.py`: Python script implementing ToT for the GSM8K dataset.
2. `tot_storycloze.py`: Python script implementing ToT for the StoryCloze dataset.

## Overview

The Tree of Thought approach is a novel method for enhancing problem-solving capabilities of large language models. It involves generating multiple thought processes, evaluating them, and exploring the most promising paths to find solutions.

### tot_gsm8k.py

This script focuses on solving math word problems from the GSM8K dataset. It implements several ToT variants:

- Input-Output (IO) baseline
- ToT with Breadth-First Search (BFS)
- ToT with Depth-First Search (DFS)
- ToT with A* Search

### tot_storycloze.py

This script applies the ToT approach to the StoryCloze dataset, which involves selecting the most appropriate ending for a given story. It implements:

- Input-Output (IO) baseline
- ToT with BFS, DFS, and A* Search for story completion

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/RJCroes/Tree-Of-Thought-Croes-Rodolfo.git
   cd Tree-Of-Thought-Croes-Rodolfo
   ```

2. Install the required dependencies:
   ```
   pip install openai pandas numpy
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. Ensure you have the necessary dataset files:
   - For GSM8K: `gsm8k.jsonl`
   - For StoryCloze: `cloze_test_val__winter2018-cloze_test_ALL_val.csv`

   Place these files in the same directory as the Python scripts.

## Usage

1. To run the GSM8K experiments:
   ```
   python tot_gsm8k.py
   ```

2. To run the StoryCloze experiments:
   ```
   python tot_storycloze.py
   ```

3. You can modify the parameters in the `run` functions within each script to adjust the number of tasks, methods, or model settings.

## Results

The scripts will generate result files for each method, including:
- A text file with detailed results and analysis
- A JSON file containing the raw data of the experiments

These files will be saved in the same directory as the Python scripts.

## Configuration

Both scripts use a set of constants and prompts that can be adjusted:

- Model types (e.g., `MODEL_GPT4`, `MODEL_GPT35`)
- Formats for answers
- Prompts for different stages of the ToT process

You can modify these in the respective Python files to experiment with different settings.

## Contributing

Contributions to improve the implementations or extend the experiments are welcome. Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This implementation is based on the Tree of Thoughts paper by Yao et al. (2023).
- The GSM8K dataset is from Cobbe et al. (2021).
- The StoryCloze dataset is from Sharma et al. (2018).

## References

```
@misc{yao2023tree,
      title={{Tree of Thoughts}: Deliberate Problem Solving with Large Language Models},
      author={Shunyu Yao and Dian Yu and Jeffrey Zhao and Izhak Shafran and Thomas L. Griffiths and Yuan Cao and Karthik Narasimhan},
      year={2023},
      eprint={2305.10601},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

@article{cobbe2021gsm8k,
  title={Training Verifiers to Solve Math Word Problems},
  author={Cobbe, Karl and Kosaraju, Vineet and Bavarian, Mohammad and Chen, Mark and Jun, Heewoo and Kaiser, Lukasz and Plappert, Matthias and Tworek, Jerry and Hilton, Jacob and Nakano, Reiichiro and Hesse, Christopher and Schulman, John},
  journal={arXiv preprint arXiv:2110.14168},
  year={2021}
}

@inproceedings{sharma-etal-2018-tackling,
    title = "Tackling the Story Ending Biases in The Story Cloze Test",
    author = "Sharma, Rishi  and Allen, James  and Bakhshandeh, Omid  and Mostafazadeh, Nasrin",
    booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
    month = jul,
    year = "2018",
    address = "Melbourne, Australia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P18-2119",
    doi = "10.18653/v1/P18-2119",
    pages = "752--757",
}
```
