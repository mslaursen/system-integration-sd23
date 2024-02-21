package main

import (
	"fmt"
	"myapp/parse_modules"
	"os"
	"path/filepath"
)

func main() {
	wd, _ := os.Getwd()
	dataDir := filepath.Join(filepath.Dir(wd), "data")

	fmt.Println(parse_modules.ParseXML(filepath.Join(dataDir, "people.xml"), parse_modules.People{}))
	fmt.Println(parse_modules.ParseJSON(filepath.Join(dataDir, "people.json"), parse_modules.Person{}))
	fmt.Println(parse_modules.ParseYAML(filepath.Join(dataDir, "people.yaml"), parse_modules.Person{}))
	fmt.Println(parse_modules.ParseCSV(filepath.Join(dataDir, "people.csv"), parse_modules.PersonCSV{}))
	//fmt.Println(parse_modules.ParseTEXT(filepath.Join(dataDir, "people.text")))

}
