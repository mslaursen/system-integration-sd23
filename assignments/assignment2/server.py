from pathlib import Path
from fastapi import FastAPI
from assignments.assignment1.python_solution.parse_module import (
    parse_csv,
    parse_json,
    parse_text,
    parse_xml,
    parse_yaml,
    PersonDTO,
    PersonDTO_CSV,
)


app = FastAPI()


def _get_path(extension: str) -> Path:
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "assignment1" / "data"
    return data_dir / f"people.{extension}"


@app.get("/csv")
def get_parsed_csv() -> list[PersonDTO_CSV]:
    return parse_csv(path=_get_path("csv"), out_dto=PersonDTO_CSV)


@app.get("/json")
def get_parsed_json() -> list[PersonDTO]:
    return parse_json(path=_get_path("json"), out_dto=PersonDTO)


@app.get("/text")
def get_parsed_text() -> str:
    return parse_text(_get_path("text"))


@app.get("/xml")
def get_parsed_xml() -> list[PersonDTO]:
    return parse_xml(path=_get_path("xml"), out_dto=PersonDTO)


@app.get("/yaml")
def get_parsed_yaml() -> list[PersonDTO]:
    return parse_yaml(path=_get_path("yaml"), out_dto=PersonDTO)
