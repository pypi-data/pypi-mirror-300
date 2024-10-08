""" Command to perform code reviews """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import CHAT_LLM, SYSTEM_MESSAGE, print_highlighted


def document(
    code: Annotated[
        typer.FileText,
        typer.Argument(help="File containing code to add documentation."),
    ],
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            "-m",
            help="The model to run inference with. Can be a model id hosted on the "
            "Hugging Face Hub, e.g. meta-llama/Meta-Llama-3-8B-Instruct or a URL "
            "to a deployed Inference Endpoint.",
        ),
    ] = CHAT_LLM,
) -> None:
    """
    Add documentation to the provided code.

    Args:
        code (typer.FileText): The file containing code to be documented.

    Examples:
    ```shell
    # Document code.py
    code-pilot document code.py

    # Document code.py using a specific model
    code-pilot document code.py -m meta-llama/Llama-3.2-3B-Instruct
    ```
    """

    client = InferenceClient(model)

    try:
        response = client.chat_completion(
            messages=[
                SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": "As a an expert software engineer and site reliability engineer "
                    "that puts code into production in large scale systems. Your job is to ensure "
                    "that code runs effectively, quickly, at scale, and securely. Please document the "
                    "provided code, including any potential issues or improvements that could be made, "
                    "and provide the updated code with the documentation included. The documentation "
                    "should include docstrings, comments, and any other relevant information that could "
                    "help developers better understand the code's purpose, functionality, and behavior:\n"
                    f"{code.read()}",
                },
            ],
            max_tokens=2048,
        )

        print_highlighted(response.choices[0].message.content)

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
