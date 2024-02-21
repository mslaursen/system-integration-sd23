from pathlib import Path
from fastapi import FastAPI
from typing import Literal, Any
from assignments.assignment1.python_solution.parse_module import (
    parse_csv,
    parse_json,
    parse_text,
    parse_xml,
    parse_yaml,
)

import requests


from assignments.assignment1.python_solution.dtos import (
    PersonDTO,
    PersonDTO_CSV,
    DataResponse,
    DataValueResponse,
)


app = FastAPI()


def _get_path(extension: str) -> Path:
    current_dir = Path(__file__).parent.parent.parent
    data_dir = current_dir / "assignment1" / "data"
    return data_dir / f"people.{extension}"


@app.get("/csv")
def get_parsed_csv() -> DataResponse[PersonDTO_CSV]:
    return DataResponse(
        data=parse_csv(
            path=_get_path("csv"),
            out_dto=PersonDTO_CSV,
        )
    )


@app.get("/json")
def get_parsed_json() -> DataResponse[PersonDTO]:
    return DataResponse(
        data=parse_json(
            path=_get_path("json"),
            out_dto=PersonDTO,
        )
    )


@app.get("/text")
def get_parsed_text() -> DataValueResponse[str]:
    return DataValueResponse(
        data=parse_text(
            _get_path("text"),
        )
    )


@app.get("/xml")
def get_parsed_xml() -> DataResponse[PersonDTO]:
    return DataResponse(
        data=parse_xml(
            path=_get_path("xml"),
            out_dto=PersonDTO,
        )
    )


@app.get("/yaml")
def get_parsed_yaml() -> DataResponse[PersonDTO]:
    return DataResponse(
        data=parse_yaml(
            path=_get_path("yaml"),
            out_dto=PersonDTO,
        )
    )


@app.get("/")
def fetch_from_go(file_type: Literal["csv", "json", "text", "xml", "yaml"]) -> Any:
    url = f"http://localhost:8080/{file_type}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text
