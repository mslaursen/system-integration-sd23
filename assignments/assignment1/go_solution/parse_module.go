package main

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

type Path = string

type ParserFunc func(string) (any, error)

type Address struct {
	City    string `json:"city"`
	Country string `json:"country"`
}

type Person struct {
	Name      string   `json:"name" xml:"name"`
	Age       int      `json:"age" xml:"age"`
	Address   Address  `json:"address" xml:"address"`
	Hobbies   []string `json:"hobbies" xml:"hobbies>hobby"`
	IsMarried bool     `json:"isMarried" xml:"isMarried"`
}

type Root struct {
	XMLName xml.Name `xml:"root"`
	People  []Person `xml:"row"`
}

func readFileContent(path Path) ([]byte, error) {
	file, err := os.Open(path)

	if err != nil {
		return nil, err
	}
	defer file.Close()

	return io.ReadAll(file)
}

func parseCSV[T any](path Path, targetStruct T) ([]T, error) {
	return nil, nil
}

func parseJSON[T any](path Path, targetStruct T) ([]T, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	var targetStructs []T
	err = json.Unmarshal(bytes, &targetStructs)

	if err != nil {
		return nil, err
	}

	return targetStructs, nil
}

func parseYAML[T any](path Path, targetStruct T) ([]T, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	var targetStructs []T
	err = yaml.Unmarshal(bytes, &targetStructs)

	if err != nil {
		return nil, err
	}

	return targetStructs, nil
}

func parseXML[T any](path Path, targetStruct T) ([]T, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	var root Root
	err = xml.Unmarshal(bytes, &root)

	if err != nil {
		return nil, err
	}

	return root, 

}

func runParser(parser ParserFunc, path Path) (any, error) {
	result, err := parser(path)
	if err != nil {
		return nil, err
	}
	return result, nil
}

func main() {
	wd, _ := os.Getwd()
	dataDir := filepath.Join(filepath.Dir(wd), "data")
	filePath := filepath.Join(dataDir, "people.xml")

	json, _ := parseXML(filePath, Person{})

	fmt.Println(json)

	//parsers := map[string]ParserFunc{
	//	//"csv.csv":   parseCSV,
	//	"json.json": parseJSON,
	//	//"text.text": parseTEXT,
	//	//"xml.xml":   parseXML,
	//	//"yaml.yaml": parseYAML,
	//}
	//
	//for path, parser := range parsers {
	//	fmt.Printf("Parsing %s...\n", path)
	//	fruits, _ := runParser(parser, filepath.Join(dataDir, path))
	//	fmt.Println(fruits)
	//	fmt.Println()
	//}
}
