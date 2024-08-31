# Leet-Code-Problem-Solver
## Project Description
This repository features an AI model built using Crew AI, designed to solve competitive programming problems from LeetCode. The model simulates a team of specialized agents, each responsible for a specific part of the problem-solving process. By defining concrete tasks for web scraping, problem simplification, algorithm suggestion, coding, and test case development, the model effectively automates the entire process of solving LeetCode problems. The model was tested on 104 problems and achieved an impressive 93% accuracy.

## Features
Web Scraping: Scrapes LeetCode problem statements directly from the website.

Problem Simplification: Breaks down complex problems into simple, clear tasks.

Problem Classification: Identifies the category of the problem (e.g., dynamic programming, graph theory).

Algorithm Suggestion: Recommends algorithms suited to solving the problem.

Code Generation: Automatically writes code (usually python) to solve the problem.

Test Case Development: Creates comprehensive test cases, including edge cases, to validate the solution.

Code Execution and Validation: Runs the generated code against the test cases to ensure correctness.

## How to Use?
Clone the repository to your local machine.
Ensure you have the required dependencies installed (e.g., Crew AI, Gradio, utils).
Run the main.py file to launch the Gradio interface.
Input the problem either as a link or as text.
Click "Start" to execute the problem-solving process.
The solution will be displayed, and you can download the resulting Python file.

## Code Explanation
The model is structured around agents and tasks, each playing a specific role in the problem-solving process. Below is an explanation of the main components:

#### Agents:
Each agent is responsible for a specific task in the problem solving process:

Scraper: Extracts problem details from the provided link.

Simplifier: Breaks down the problem into goal, input, and output.

Problem Identifier: Classifies the problem into a specific category.

Algorithm Suggester: Suggests suitable algorithms to solve the problem.

Coder: Writes Python code based on the suggested algorithms.

Test Case Developer: Creates test cases to validate the solution.

Code Runner: Executes the code against the test cases and validates the output.

#### Tasks: 
Each task corresponds to an agent's action, linked together in a sequence to form a coherent problem-solving pipeline. For example, the scrap task initializes the scraping process, followed by simplify, which simplifies the problem, and so on until the final validation.

#### Crew: 
The crew is a collection of agents and tasks working together to solve the problem. Depending on the input type (link or text), a different crew configuration is used.

#### Gradio Interface: 
The Gradio interface provides a user-friendly front end for interacting with the model. Users can input problems, start the solving process, view the results, and download the Python code file.

## Results
The model was tested on 104 LeetCode problems with an impressive 93% accuracy. The problems included:

47 hard problems
51 medium problems
5 easy problems. 

These problems covered various topics such as math, dynamic programming, trees, graphs, strings, and more.

## Limitations
The model's performance may vary depending on the complexity and nature of the problem. Moreover, while the accuracy is high, there may be edge cases that the model fails to handle.

## Contributions
Contributions to this project are welcome! If you encounter any bugs, issues, or have ideas for enhancements, feel free to open an issue or submit a pull request. Your input is valuable in improving the model and expanding its capabilities.
