""" Command for natural language interactions like command generation """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import CHAT_LLM, SYSTEM_MESSAGE, print_highlighted


def ai(
    prompt: Annotated[
        str, typer.Argument(help="Natural language prompt for command generation.")
    ],
    code: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--code",
            "-c",
            exists=True,
            help="Code file to include in the prompt.",
            encoding="utf-8",
        ),
    ] = None,
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
    Interact with CodePilot using natural language.

    Args:
        prompt (str): The natural language prompt from which to generate a command.
        code (typer.FileText, optional): The file containing code to be scanned.
        model (str, optional): The model to run inference with. Defaults to CHAT_LLM.

    Examples:
    ```shell
    # Interact with CodePilot
    code-pilot ai "Generate a command to install a package called pandas"

    # Interact with CodePilot using a specific model
    code-pilot ai "Generate a command to install a package called pandas" -m meta-llama/Llama-3.2-3B-Instruct
    ```
    """

    client = InferenceClient(model)

    try:
        response = client.chat_completion(
            messages=[
                SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": (
                        f"{prompt}:\n```\n{code.read()}\n```" if code else prompt
                    ),
                },
            ],
            max_tokens=2048,
        )

        print_highlighted(response.choices[0].message.content)

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
