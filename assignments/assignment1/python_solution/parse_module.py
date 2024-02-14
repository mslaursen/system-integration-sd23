import json
import csv
import yaml
from pathlib import Path
from typing import Any


from pydantic import BaseModel, Field


class _BasePersonDTO(BaseModel):
    name: str
    age: int
    hobbies: list[str] | None = None
    is_married: bool = Field(..., alias="isMarried")


class AddressDTO(BaseModel):
    city: str
    country: str


class PersonDTO(_BasePersonDTO):
    address: AddressDTO


class PersonDTO_CSV(_BasePersonDTO, AddressDTO): ...


def parse_csv[OutDTO: BaseModel](path: Path, out_dto: OutDTO) -> list[OutDTO]:
    with open(path, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        output = []

        for row in reader:
            for key, value in row.items():
                print(key)
                if ";" in value:
                    row[key] = value.split(";")

            print(row)

            # print(out_dto(**row))
            # output.append(out_dto(**row))

        # print(output)
        # return output


def parse_json[OutDTO: BaseModel](path: Path, out_dto: OutDTO) -> list[OutDTO]:
    with open(path, "r") as json_file:
        loaded_json = json.loads(json_file.read())
        for person in loaded_json:
            print(person)
        return [out_dto(**person) for person in loaded_json]


def parse_text(path: Path) -> str:
    with open(path, "r") as text_file:
        return text_file.read()


def parse_xml[OutDTO: BaseModel](path: Path, out_dto: OutDTO) -> list[OutDTO]:
    with open(path, "r") as xml_file:
        print(xml_file.read())


def parse_yaml[OutDTO: BaseModel](path: Path, out_dto: OutDTO) -> list[OutDTO]:
    with open(path, "r") as yaml_file:
        return [out_dto(**person) for person in yaml.safe_load(yaml_file)]


if __name__ == "__main__":
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "data"

    parsers = {
        "csv": (parse_csv, PersonDTO_CSV),
        # "json": parse_json,
        # "text": parse_text,
        # "xml": parse_xml,
        # "yaml": parse_yaml,
    }

    for file_type, (parser, out_dto) in parsers.items():
        print(f"Parsing {file_type}...")
        file_path = data_dir / f"people.{file_type}"
        print(f"{parser(file_path, PersonDTO_CSV)}", "\n")
