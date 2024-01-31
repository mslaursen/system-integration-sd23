import json
import csv
import yaml
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


def parse_csv(path: Path) -> list[Any]:
    with open(path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        return [row for row in reader]


def parse_json(path: Path) -> list[dict[str, Any]]:
    with open(path, "r") as json_file:
        return json.loads(json_file.read())


def parse_text(path: Path) -> list[str]:
    with open(path, "r") as text_file:
        return [line.strip() for line in text_file.readlines()]


def parse_xml(path: Path) -> list[dict[str, Any]]:
    return [
        {
            "fruit": fruit.find("name").text,  # type: ignore
            "color": fruit.find("color").text,  # type: ignore
        }
        for fruit in ET.parse(path).getroot().findall("fruit")
    ]


def parse_yaml(path: Path) -> list[dict[str, Any]]:
    with open(path, "r") as yaml_file:
        return yaml.safe_load(yaml_file)


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"

    print("---- CSV ----")
    csv_path = data_dir / "csv.csv"
    print(parse_csv(csv_path), "\n")

    print("---- JSON ----")
    json_path = data_dir / "json.json"
    print(parse_json(json_path), "\n")

    print("---- TEXT ----")
    text_path = data_dir / "text.text"
    print(parse_text(text_path), "\n")

    print("---- XML ----")
    xml_path = data_dir / "xml.xml"
    print(parse_xml(xml_path), "\n")

    print("---- YAML ----")
    yaml_path = data_dir / "yaml.yaml"
    print(parse_yaml(yaml_path), "\n")
