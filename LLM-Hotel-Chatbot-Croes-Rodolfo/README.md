# LLM Chatbot for Divi Resorts Booking

This repository contains an academic project developed as part of the ITNPAI1 assignment (Student No: 3080195). The objective of this project is to design, implement, and evaluate a chatbot using GPT-4 (version 0125-preview) that assists users in booking resort stays and flights with Divi Resorts through natural and engaging dialogue.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing and Evaluation](#testing-and-evaluation)
- [Sample Dialogue](#sample-dialogue)
- [Findings](#findings)
- [Future Improvements](#future-improvements)
- [References](#references)
- [License](#license)

## Overview

This project explores:

- **Prompt Engineering:** Creation and iterative refinement of prompts for GPT-4.
- **Interactive Chatbot:** Development of a chatbot to simulate a friendly resort booking agent.
- **Testing & Evaluation:** Identification and improvement of chatbot performance issues like menu printing, incomplete data collection, and calculation inaccuracies.

Detailed documentation is provided in the project report.

## Project Structure

```
.
├── LLM-Chatbot-Prompt.ipynb                    # Jupyter Notebook: Development and Testing
├── Report-LLM-Chatbot-Resort-Croes-Rodolfo.pdf # Detailed project report
├── Dialogue-Example.txt                        # Complete dialogue example
├── README.md                                   # This documentation
```

## Installation

To replicate this project, you need:

- Python 3.8 or later
- Jupyter Notebook

Install dependencies using pip:

```bash
pip install openai langchain numpy pandas
```

## Usage

### Running Notebook
- Open the notebook `LLM-Chatbot-Prompt.ipynb`.
- Execute cells sequentially to run the chatbot and test the prompts.

### Viewing Documentation
- Refer to `Report-LLM-Chatbot-Resort-Croes-Rodolfo.pdf` for comprehensive details on prompt engineering and results.

## Testing and Evaluation

Testing involved realistic simulations to validate the chatbot's ability to:

- Maintain coherent conversational flow.
- Collect complete and accurate booking information.
- Perform accurate price calculations.

### Improvements from Testing

- **Reduced menu verbosity**: Improved chatbot prompts to avoid lengthy and unnatural menus.
- **Enhanced information collection**: Implemented checkpoint-style prompts ensuring essential details are always captured.
- **Improved calculations**: Used chain-of-thought prompting to significantly enhance accuracy in calculating costs.
- **Stronger persona constraints**: Established clear conversational boundaries preventing engagement in irrelevant or inappropriate topics.

## Sample Dialogue

An excerpt from a complete dialogue:

```
User: Hi
ChatBot: Hello! 🌴😊 Welcome to the booking office at Divi Resorts. How can I assist you with your vacation planning today?
...
```

See the full interaction in `Dialogue-Example.txt`.

## Findings

- **Positives**: Good conversational structure, accurate resort knowledge, robust memory capabilities.
- **Negatives (initially)**: Verbose menus, incomplete data collection, occasional pricing inaccuracies.

Prompt refinements successfully addressed these initial issues.

## Future Improvements

- Integration of live data for dynamic pricing.
- Extensive testing for consistency in non-linear conversation flows.
- Additional practical functionalities like real-time availability checks and booking confirmations.

## References

- Luitse, D., & Denkena, W. (2021). *The great transformer: Examining the role of large language models in the political economy of AI*.
- Mollick, E. (2022). *ChatGPT Is a Tipping Point for AI*. [Harvard Business Review](https://hbr.org/2022/12/chatgpt-is-a-tipping-point-for-ai).
- Divi Resorts. (2024). [Caribbean Island Resorts](https://www.diviresorts.com).
- Cavazza, M. ITNPAI1 Practical notebooks.
- DAIR.AI. (2023). *Elements of a prompt*. [Prompting Guide](https://www.promptingguide.ai/introduction/elements).
- Achiam, J., et al. (2023). *GPT-4 Technical Report*.
- Li, C., et al. (2023). *Large language models understand and can be enhanced by emotional stimuli*.
- Wei, J., et al. (2022). *Chain-of-thought prompting elicits reasoning in large language models*.

Detailed citations and further discussion can be found in the provided project report.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
