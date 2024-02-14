import json
import csv
import yaml
from pathlib import Path


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


def parse_csv[OutDTO: BaseModel](path: Path, out_dto: type[OutDTO]) -> list[OutDTO]:
    with open(path, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        return [
            out_dto(**person)
            for person in [
                {k: v.split(";") if ";" in v else v for k, v in row.items() if v}
                for row in reader
            ]
        ]


def parse_json[OutDTO: BaseModel](path: Path, out_dto: type[OutDTO]) -> list[OutDTO]:
    with open(path, "r") as json_file:
        return [out_dto(**person) for person in json.loads(json_file.read())]


def parse_text(path: Path) -> str:
    with open(path, "r") as text_file:
        return text_file.read()


def parse_xml[OutDTO: BaseModel](path: Path, out_dto: type[OutDTO]) -> list[OutDTO]:
    with open(path, "r") as xml_file:
        print(xml_file.read())


def parse_yaml[OutDTO: BaseModel](path: Path, out_dto: type[OutDTO]) -> list[OutDTO]:
    with open(path, "r") as yaml_file:
        return [out_dto(**person) for person in yaml.safe_load(yaml_file)]


if __name__ == "__main__":
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "data"

    parsers = {
        # "csv": (parse_csv, PersonDTO_CSV),
        # "json": parse_json,
        # "text": parse_text,
        # "xml": parse_xml,
        # "yaml": parse_yaml,
    }

    for file_type, (parser, out_dto) in parsers.items():
        print(f"Parsing {file_type}...")
        file_path = data_dir / f"people.{file_type}"
        print(f"{parser(file_path, PersonDTO_CSV)}", "\n")
