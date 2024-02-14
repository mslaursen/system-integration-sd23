from pathlib import Path
from fastapi import FastAPI
from assignments.assignment1.python_solution.parse_module import (
    parse_csv,
    parse_json,
    parse_text,
    parse_xml,
    parse_yaml,
)

app = FastAPI()


def _get_path(extension: str) -> Path:
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "assignment1" / "data"
    return data_dir / f"fruits.{extension}"


@app.get("/csv")
def get_parsed_csv():
    return parse_csv(_get_path("csv"))


@app.get("/json")
def get_parsed_json():
    return parse_json(_get_path("json"))


@app.get("/text")
def get_parsed_text():
    return parse_text(_get_path("text"))


@app.get("/xml")
def get_parsed_xml():
    return parse_xml(_get_path("xml"))


@app.get("/yaml")
def get_parsed_yaml():
    return parse_yaml(_get_path("yaml"))
