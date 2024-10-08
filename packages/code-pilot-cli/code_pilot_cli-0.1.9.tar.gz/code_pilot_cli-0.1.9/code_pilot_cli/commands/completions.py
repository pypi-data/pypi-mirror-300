""" Command to generate shell commands """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import COMPLETION_LLM, print_highlighted


def completions(
    code: Annotated[str, typer.Argument(help="Code snippet to complete.")],
    language: Annotated[
        Optional[str],
        typer.Option(
            "--lang",
            "-l",
            help="Programming language of the code snippet.",
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
    ] = COMPLETION_LLM,
) -> None:
    """
    Generate code completions based on the provided code snippet.

    Args:
        code (str): The code to complete.
        language (str, optional): The programming language of the code snippet.
        model (str, optional): The model to run inference with. Defaults to COMPLETION_LLM.

    Examples:
    ```shell
    # Generate code completions
    code-pilot completions "def hello_world() -> None:"

    # Generate code completions with a specific language
    code-pilot completions "def hello_world() -> None:" -l python

    # Change the model
    code-pilot completions "def hello_world() -> None:" -m meta-llama/Llama-3.2-3B-Instruct
    ```
    """

    client = InferenceClient(model)

    try:
        response = client.text_generation(
            f"```{language if language else ''}\n{code}",
            max_new_tokens=256,
        )

        print_highlighted(f"```{language if language else ''}\n{code + response}")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
