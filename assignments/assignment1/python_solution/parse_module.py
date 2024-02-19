import json
import csv
from typing import Any
from pydantic import BaseModel
import yaml
from pathlib import Path
import xmltodict
from typing import Callable

from assignments.assignment1.python_solution.dtos import PersonDTO, PersonDTO_CSV


def parse_csv[T](path: Path, out_dto: type[T]) -> list[T]:
    with path.open() as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            out_dto(**person)
            for person in [
                {k: v.split(";") if ";" in v else v for k, v in row.items() if v}
                for row in reader
            ]
        ]


def parse_json[T](path: Path, out_dto: type[T]) -> list[T]:
    with path.open() as json_file:
        return [out_dto(**person) for person in json.loads(json_file.read())]


def parse_text(path: Path) -> str:
    with path.open() as text_file:
        return text_file.read()


def parse_yaml[T](path: Path, out_dto: type[T]) -> list[T]:
    with path.open() as yaml_file:
        return [out_dto(**person) for person in yaml.safe_load(yaml_file)]


def parse_xml[T](path: Path, out_dto: type[T]) -> list[T]:
    with path.open() as xml_file:
        return [
            out_dto(**person)
            for person in xmltodict.parse(xml_file.read())["root"]["row"]
        ]


def _run_parser(
    parser: Callable[..., Any],
    out_dto: type[BaseModel] | None,
    file_path: Path,
) -> None:

    print(f"Parsing {file_path.name}...")
    result = parser(file_path, out_dto) if out_dto else parser(file_path)
    print(result)


if __name__ == "__main__":
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "data"

    parsers = {
        "csv": (parse_csv, PersonDTO_CSV),
        "json": (parse_json, PersonDTO),
        "text": (parse_text, None),
        "yaml": (parse_yaml, PersonDTO),
        "xml": (parse_xml, PersonDTO),
    }

    for file_type, (parser, out_dto) in parsers.items():
        _run_parser(parser, out_dto, data_dir / f"people.{file_type}")
