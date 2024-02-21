package parse_modules

import (
	"encoding/csv"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"reflect"
	"strconv"
	"strings"

	"gopkg.in/yaml.v3"
)

type Path = string

type Address struct {
	City    string `json:"city" xml:"city"`
	Country string `json:"country" xml:"country"`
}

type Person struct {
	Name      string   `json:"name" xml:"name"`
	Age       int      `json:"age" xml:"age"`
	Address   Address  `json:"address" xml:"address"`
	Hobbies   []string `json:"hobbies" xml:"hobbies"`
	IsMarried bool     `json:"isMarried" xml:"isMarried"`
}

type PersonCSV struct {
	Name      string   `csv:"name"`
	Age       int      `csv:"age"`
	City      string   `csv:"city"`
	Country   string   `csv:"country"`
	Hobbies   []string `csv:"hobbies"`
	IsMarried bool     `csv:"isMarried"`
}

type People struct {
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

func ParseCSV[T any](path Path, targetStruct T) ([]T, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	_, err = reader.Read()
	if err != nil {
		return nil, err
	}

	outStructs := make([]T, 0)
	sValue := reflect.ValueOf(&targetStruct).Elem()

	for {
		record, err := reader.Read()
		if err != nil {
			break
		}
		for i, value := range record {
			field := sValue.Field(i)

			switch field.Type().Kind() {
			case reflect.String:
				field.SetString(value)
			case reflect.Int:
				n, _ := strconv.ParseInt(value, 10, 64)
				field.SetInt(n)
			case reflect.Slice:
				field.Set(reflect.ValueOf(strings.Split(value, ";")))
			case reflect.Bool:
				b, _ := strconv.ParseBool(value)
				field.SetBool(b)
			}
		}
		outStructs = append(outStructs, targetStruct)
	}

	return outStructs, nil
}

func ParseJSON[T any](path Path, targetStruct T) ([]T, error) {
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

func ParseTEXT(path Path) (string, error) {
	bytes, err := readFileContent(path)

	if err != nil {
		return "", err
	}

	return string(bytes), nil
}

func ParseYAML[T any](path Path, targetStruct T) ([]T, error) {
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

func ParseXML[T any](path Path, targetStruct T) (T, error) {
	bytes, _ := readFileContent(path)

	var root T
	err := xml.Unmarshal(bytes, &root)

	if err != nil {
		fmt.Println(err)
	}

	return root, nil
}
