package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"

	"gopkg.in/yaml.v3"
)

type Path = string

type ParserFunc func(string) (any, error)

type XMLFruits struct {
	XMLName xml.Name `xml:"fruits"`
	Fruits  []Fruit  `xml:"fruit"`
}

type Fruit struct {
	Name  string `json:"fruit" xml:"name" yaml:"fruit"`
	Color string `json:"color" xml:"color" yaml:"color"`
}

func openFile(path Path) (*os.File, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	return file, nil
}

func readFileContent(path Path) ([]byte, error) {
	file, err := openFile(path)

	if err != nil {
		return nil, err
	}
	defer file.Close()

	return io.ReadAll(file)
}

func parseCSV(path Path) (any, error) {
	file, err := openFile(path)

	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	reader.Read() // skip header

	fruits, err := reader.ReadAll()

	if err != nil {
		return nil, err
	}

	return fruits, nil
}

func parseJSON(path Path) (any, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	fruits := []Fruit{}
	err = json.Unmarshal(bytes, &fruits)

	if err != nil {
		return nil, err
	}

	return fruits, nil
}

func parseTEXT(path Path) (any, error) {
	file, err := openFile(path)

	if err != nil {
		return "", err
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	fruits := []string{}

	for {
		line, err := reader.ReadString('\n')

		if err != nil {
			if err == io.EOF {
				break
			}
			return nil, err
		}

		fruits = append(fruits, line)
	}

	return fruits, nil
}

func parseXML(path Path) (any, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	fruits := &XMLFruits{}
	err = xml.Unmarshal(bytes, &fruits)

	if err != nil {
		return nil, err
	}

	return fruits, nil
}

func parseYAML(path Path) (any, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return nil, err
	}

	fruits := []Fruit{}
	err = yaml.Unmarshal(bytes, &fruits)

	if err != nil {
		return nil, err
	}

	return fruits, nil
}

func runParser(parser ParserFunc, path Path) (any, error) {
	result, err := parser(path)
	if err != nil {
		return nil, err
	}
	return result, nil
}

func main() {
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		fmt.Println("Error")
		return
	}
	currentDir := filepath.Dir(filename)
	dataDir := filepath.Join(currentDir, "data")

	parsers := map[string]ParserFunc{
		"csv.csv":   parseCSV,
		"json.json": parseJSON,
		"text.text": parseTEXT,
		"xml.xml":   parseXML,
		"yaml.yaml": parseYAML,
	}

	for path, parser := range parsers {
		fmt.Printf("Parsing %s...\n", path)
		fruits, _ := runParser(parser, filepath.Join(dataDir, path))
		fmt.Println(fruits)
		fmt.Println()
	}
}
