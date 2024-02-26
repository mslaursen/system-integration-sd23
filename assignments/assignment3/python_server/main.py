import requests

from pathlib import Path
from fastapi import FastAPI
from typing import Any, Literal


from assignments.assignment1.python_solution.parse_module import (
    parse_csv,
    parse_json,
    parse_text,
    parse_xml,
    parse_yaml,
)


from assignments.assignment1.python_solution.dtos import (
    PersonDTO,
    PersonDTO_CSV,
    DataResponse,
    DataValueResponse,
)


app = FastAPI()


def _get_path(format: str) -> Path:
    current_dir = Path(__file__).parent.parent.parent
    data_dir = current_dir / "assignment1" / "data"
    return data_dir / f"people.{format}"


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


GoDataResponse = DataResponse[Any] | DataValueResponse[str]


@app.get("/")
def fetch_from_go(
    format: Literal["csv", "json", "text", "xml", "yaml"]
) -> GoDataResponse:
    url = f"http://localhost:8080/{format}"
    response = requests.get(url)
    response.raise_for_status()

    if format == "text":
        return DataValueResponse(data=response.text)

    return DataResponse(
        data=[
            format_dto_mapping[format].model_validate(data)
            for data in response.json()["data"]
        ]
    )


format_dto_mapping = {
    "csv": PersonDTO_CSV,
    "json": PersonDTO,
    "xml": PersonDTO,
    "yaml": PersonDTO,
}
