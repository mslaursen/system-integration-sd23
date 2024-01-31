package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
)

type ParserFunc[T any] func(path Path) (T, error)

type GenericParser[T any] struct {
	ParseFunc ParserFunc[T]
}

func NewGenericParser[T any](parseFunc ParserFunc[T]) *GenericParser[T] {
	return &GenericParser[T]{ParseFunc: parseFunc}
}

func (gp *GenericParser[T]) Parse(path Path) (T, error) {
	return gp.ParseFunc(path)
}
func JSONParseFunc(path Path) ([]Fruit, error) {
	jsonFile, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()

	jsonBytes, err := io.ReadAll(jsonFile)
	if err != nil {
		return nil, err
	}

	var fruits []Fruit
	err = json.Unmarshal(jsonBytes, &fruits)
	if err != nil {
		return nil, err
	}

	return fruits, nil
}

func TextParseFunc(path Path) (string, error) {
	textFile, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer textFile.Close()

	textBytes, err := io.ReadAll(textFile)
	if err != nil {
		return "", err
	}

	return string(textBytes), nil
}

func CSVParseFunc(path Path) ([][]string, error) {
	csvFile, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer csvFile.Close()

	reader := csv.NewReader(csvFile)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	return records, nil
}

type Path = string
type Fruit struct {
	Fruit string `json:"fruit"`
	Color string `json:"color"`
}

func main() {
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		fmt.Println("Failed to determine current directory")
		return
	}
	currentDir := filepath.Dir(filename)
	dataDir := filepath.Join(currentDir, "data")

	fmt.Println("---- CSV ----")
	csvPath := filepath.Join(dataDir, "csv.csv")
	csvParser := NewGenericParser(CSVParseFunc)
	records, err := csvParser.Parse(csvPath)
	if err != nil {
		fmt.Println("Error parsing file:", err)
		return
	}

	for _, record := range records {
		fmt.Println(record)
	}

	fmt.Println("---- JSON ----")
	jsonPath := filepath.Join(dataDir, "json.json")
	jsonParser := NewGenericParser(JSONParseFunc)
	fruits, err := jsonParser.Parse(jsonPath)
	if err != nil {
		fmt.Println("Error parsing file:", err)
		return
	}

	for _, fruit := range fruits {
		fmt.Printf("Fruit: %s, Color: %s\n", fruit.Fruit, fruit.Color)
	}

	fmt.Println("---- TEXT ----")
	textPath := filepath.Join(dataDir, "text.text")
	textParser := NewGenericParser(TextParseFunc)
	text, err := textParser.Parse(textPath)
	if err != nil {
		fmt.Println("Error parsing file:", err)
		return
	}

	fmt.Println(text)

	// fmt.Println("---- XML ----")
	// xmlPath := filepath.Join(dataDir, "xml.xml")

}
