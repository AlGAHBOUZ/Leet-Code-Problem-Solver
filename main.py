import os
import warnings

from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, CodeInterpreterTool
from utils import get_openai_api_key
import gradio as gr

# Suppress warnings
warnings.filterwarnings('ignore')

# Set environment variables
openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
code_interpreter = CodeInterpreterTool()

# Create agents
def create_agents():
    """Initialize all agents with specific roles, goals, and tools."""
    scraper = Agent(
        role="Competitive Programming Problem Scraper",
        goal="Scrape competitive programming problems from provided links and gather necessary information.",
        tools=[scrape_tool],
        verbose=True,
        backstory=(
            "Expert web scraper specialized in extracting essential details from competitive programming problems."
        ),
        allow_delegation=False
    )

    simplifier = Agent(
        role="Problem Simplifier",
        goal="Simplify the problem by breaking it down into a clear goal, input, and output.",
        tools=[],
        verbose=True,
        backstory=(
            "Master problem simplifier, converting complex problems into clear tasks with a defined goal."
        ),
        allow_delegation=False
    )

    problem_identifier = Agent(
        role="Problem Family Identifier",
        goal="Identify the problem's category (e.g., dynamic programming, graph theory).",
        tools=[],
        verbose=True,
        backstory=(
            "Expert in classifying problems into categories based on deep algorithmic knowledge."
        ),
        allow_delegation=False
    )

    algorithm_suggester = Agent(
        role="Algorithm Suggester",
        goal="Suggest algorithms to solve the problem based on its category and simplified statement.",
        tools=[],
        verbose=True,
        backstory=(
            "Encyclopedic knowledge of algorithms, suggesting the best approach for problem-solving."
        ),
        allow_delegation=False
    )

    coder = Agent(
        role="Code Writer",
        goal="Write code to solve the problem using the suggested algorithm(s).",
        tools=[],
        verbose=True,
        backstory=(
            "Skilled coder capable of translating problem-solving strategies into efficient, optimized code."
        ),
        allow_delegation=False
    )

    test_case_developer = Agent(
        role="Test Case Developer",
        goal="Develop comprehensive test cases, including edge cases, to validate the solution.",
        tools=[],
        verbose=True,
        backstory=(
            "Detail-oriented developer, ensuring code correctness through rigorous test case development."
        ),
        allow_delegation=False
    )

    code_runner = Agent(
        role="Code Runner and Validator",
        goal="Run the code against test cases and validate the solution.",
        tools=[code_interpreter],
        verbose=True,
        backstory=(
            "Responsible for executing code and verifying its correctness against expected outputs."
        ),
        allow_delegation=False
    )

    return {
        "scraper": scraper,
        "simplifier": simplifier,
        "problem_identifier": problem_identifier,
        "algorithm_suggester": algorithm_suggester,
        "coder": coder,
        "test_case_developer": test_case_developer,
        "code_runner": code_runner
    }

# Create tasks
def create_tasks(agents):
    """Initialize tasks and assign corresponding agents."""
    scrap = Task(
        description="Scrape the provided competitive programming problem link to gather necessary information.",
        expected_output="A dictionary containing the problem statement, input, output, and other relevant details.",
        agent=agents["scraper"]
    )

    simplify = Task(
        description="Simplify the problem into a clear goal, input, and output.",
        expected_output="A simplified problem statement with a clearly defined goal, input, and output.",
        agent=agents["simplifier"],
        context=[scrap]
    )

    identify = Task(
        description="Identify the problem's family or category based on the simplified problem statement.",
        expected_output="A classification of the problem's family or category.",
        agent=agents["problem_identifier"],
        context=[simplify]
    )

    suggest_algorithm = Task(
        description="Suggest algorithms to solve the problem based on its category and simplified statement.",
        expected_output="A list of suggested algorithms with explanations.",
        agent=agents["algorithm_suggester"],
        context=[simplify, identify]
    )

    write_code = Task(
        description=(
            "Write the code to solve the problem using the suggested algorithms. "
            "Revise the code if necessary to ensure correctness."
        ),
        expected_output="A code solution that solves the problem.",
        agent=agents["coder"],
        context=[simplify, identify, suggest_algorithm]
    )

    develop_tests = Task(
        description="Develop test cases, including edge cases, to validate the correctness of the solution.",
        expected_output="A set of test cases, including inputs and expected outputs.",
        agent=agents["test_case_developer"],
        context=[simplify, identify]
    )

    run_and_validate = Task(
        description=(
            "Run the code against the developed test cases and validate the solution. "
            "Ensure that all test cases pass before finalizing the code."
        ),
        expected_output="A report on the correctness of the solution based on test case results.",
        agent=agents["code_runner"],
        context=[write_code, develop_tests]
    )

    return {
        "scrap": scrap,
        "simplify": simplify,
        "identify": identify,
        "suggest_algorithm": suggest_algorithm,
        "write_code": write_code,
        "develop_tests": develop_tests,
        "run_and_validate": run_and_validate
    }

# Crew creation
def create_crew(input_type, input_value=None):
    """Create a Crew based on the input type, with or without a scraper agent."""
    agents = create_agents()
    tasks = create_tasks(agents)

    if input_type == "link":
        return Crew(
            agents=[agents["scraper"], agents["simplifier"], agents["problem_identifier"],
                    agents["algorithm_suggester"], agents["coder"], agents["test_case_developer"], agents["code_runner"]],
            tasks=[tasks["scrap"], tasks["simplify"], tasks["identify"], tasks["suggest_algorithm"],
                   tasks["write_code"], tasks["develop_tests"], tasks["run_and_validate"]],
            verbose=True
        )
    else:
        tasks["simplify"].description = f"Simplify the following problem:\n\n{input_value}\n\nBreak it down into a clear goal, input, and output."
        return Crew(
            agents=[agents["simplifier"], agents["problem_identifier"],
                    agents["algorithm_suggester"], agents["coder"], agents["test_case_developer"], agents["code_runner"]],
            tasks=[tasks["simplify"], tasks["identify"], tasks["suggest_algorithm"],
                   tasks["write_code"], tasks["develop_tests"], tasks["run_and_validate"]],
            verbose=True
        )

# Run the crew
def run_crew(input_type, input_value):
    """Execute the crew based on the provided input type and value."""
    crew = create_crew(input_type, input_value)
    result = crew.kickoff(inputs={'link': input_value} if input_type == "link" else None)
    
    file_path = 'solution.py'
    try:
        with open(file_path, 'w') as file:
            file.write(result)
    except IOError as e:
        print(f"Error writing to file: {e}")
    
    return result, file_path

# Gradio interface
def build_gradio_interface():
    """Build and launch the Gradio interface."""
    with gr.Blocks() as demo:
        with gr.Column():
            input_type = gr.Radio(["link", "text"], label="Input Type")
            link_input = gr.Textbox(label="Enter the problem link", visible=False)
            text_input = gr.Textbox(label="Enter the problem text", visible=False, lines=10)
            start_button = gr.Button("Start")
            markdown_output = gr.Markdown()
            download_button = gr.File(label="Download the resulting Python file")

            def update_input_visibility(choice):
                return gr.update(visible=choice == "link"), gr.update(visible=choice == "text")

            input_type.change(update_input_visibility, inputs=[input_type], outputs=[link_input, text_input])

            def start_process(input_type, link, text):
                input_value = link if input_type == "link" else text
                result, file_path = run_crew(input_type, input_value)
                return result, file_path

            start_button.click(start_process, inputs=[input_type, link_input, text_input], outputs=[markdown_output, download_button])

    demo.launch(share=True)

if __name__ == "__main__":
    build_gradio_interface()
