""" Command to perform code scanning """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import CHAT_LLM, SYSTEM_MESSAGE, print_highlighted


def scan(
    code: Annotated[
        typer.FileText,
        typer.Argument(help="File containing code to scan for vulnerabilities."),
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
    Scan the provided code for security vulnerabilities.

    Args:
        code (typer.FileText): The file containing code to be scanned.
        model (str, optional): The model to run inference with. Defaults to CHAT_LLM.

    Examples:
    ```shell
    # Scan a code file
    code-pilot scan code.py

    # Scan a code file using a specific model
    code-pilot scan code.py -m meta-llama/Llama-3.2-3B-Instruct
    ```
    """

    client = InferenceClient(model)

    try:
        response = client.chat_completion(
            messages=[
                SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": "As a an expert software engineer and cybersecurity engineer "
                    "that puts code into production in large scale systems. Your job is to ensure "
                    "that code runs effectively, quickly, at scale, and securely. Please perform a "
                    "code scan to identify potential security vulnerabilities in the provided code:"
                    f"\n{code.read()}",
                },
            ],
            max_tokens=2048,
        )

        print_highlighted(response.choices[0].message.content)

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
