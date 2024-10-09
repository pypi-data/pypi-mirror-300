import json
import re
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from promptulate.error import OutputParserError
from promptulate.output_formatter.prompt import OUTPUT_FORMAT
from promptulate.pydantic_v1 import BaseModel

T = TypeVar("T", bound=BaseModel)


def _get_schema(pydantic_obj: Type[BaseModel]) -> dict:
    """Get reduced schema from pydantic object.

    Args:
        pydantic_obj: The pydantic object to get schema from.

    Returns:
        Dict: The reduced schema, which is without title and type fields.
    """

    # Remove useless fields.
    # Compatibility with Pydantic v2 model_json_schema method.
    if hasattr(pydantic_obj, "model_json_schema"):
        return pydantic_obj.model_json_schema()
    else:
        reduced_schema = pydantic_obj.schema()

    if "title" in reduced_schema:
        del reduced_schema["title"]
    if "type" in reduced_schema:
        del reduced_schema["type"]
    for k, v in reduced_schema["properties"].items():
        if "title" in v:
            del v["title"]

    return reduced_schema


class OutputFormatter:
    """
    Class for formatting the output of a Pydantic object.

    This class provides methods for getting formatted instructions and formatting the
    result of a Pydantic object.
    """

    def __init__(
        self,
        pydantic_obj: Type[BaseModel],
        examples: Optional[List[BaseModel]] = None,
        **kwargs,
    ):
        """
        Initialize the OutputFormatter class.

        Args:
            pydantic_obj (type(BaseModel)): The Pydantic object to format.
            examples (List[BaseModel], optional): Examples of the Pydantic object.
        """
        super().__init__(**kwargs)

        self.pydantic_obj: Type[BaseModel] = pydantic_obj
        self.examples: Optional[List[BaseModel]] = examples

    def get_formatted_instructions(self) -> str:
        return get_formatted_instructions(self.pydantic_obj, self.examples)

    def formatting_result(self, llm_output: str) -> T:
        return formatting_result(self.pydantic_obj, llm_output)


def get_formatted_instructions(
    json_schema: Union[Type[BaseModel], Dict[str, Any]],
    examples: List[BaseModel] = None,
) -> str:
    """
    Get formatted instructions for a JSON schema or Pydantic object.

    Args:
        json_schema (Union[Dict, type(BaseModel)]): The JSON schema or Pydantic object
            to get instructions for.
        examples (List[BaseModel], optional): Examples of the JSON schema or Pydantic
            object. Defaults to None.

    Returns:
        str: The formatted instructions.
    """
    # If a Pydantic model is passed, extract the schema from it.
    if not isinstance(json_schema, dict):
        json_schema: dict = _get_schema(json_schema)

    # Ensure json with double quotes.
    schema_str = json.dumps(json_schema)

    instructions: str = OUTPUT_FORMAT.format(schema=schema_str)
    if examples:
        instructions += "\nExamples:\n"
        for example in examples:
            example_str = json.dumps(example.dict())
            instructions += f"{example_str}\n"
    return instructions


def formatting_result(pydantic_obj: type(BaseModel), llm_output: str) -> T:
    """
    Parse llm_output and instantiate the result as provided pydantic_obj.

    Args:
        pydantic_obj (type(BaseModel)): The Pydantic object to instantiate the result
            as.
        llm_output (str): The output to parse.

    Returns:
        T: The instantiated result.

    Raises:
        OutputParserError: If the output cannot be parsed.
    """
    try:
        match = re.search(
            r"\{.*\}", llm_output.strip(), re.MULTILINE | re.IGNORECASE | re.DOTALL
        )
        json_str = match.group() if match else ""
        json_object = json.loads(json_str, strict=False)

        # Compatibility with Pydantic v2 model_validate method.
        if hasattr(pydantic_obj, "model_validate"):
            return pydantic_obj.model_validate(json_object)
        else:
            return pydantic_obj.parse_obj(json_object)

    except Exception as e:
        name = pydantic_obj.__name__
        msg = f"Failed to parse {name} from completion {llm_output}. Got: {e}"
        raise OutputParserError(msg, llm_output)
