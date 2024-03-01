package main

import (
	"io"
	"log"
	"net/http"
	"os"
	"parse_modules"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

func getPath(extension string) string {
	wd, err := os.Getwd()
	if err != nil {
		log.Fatalf("Failed to get current working directory: %v", err)
	}
	targetPath := filepath.Join(wd, "..", "..", "assignment1", "data", "people."+extension)
	return targetPath
}

func main() {
	r := gin.Default()

	// Parse csv
	r.GET("/csv", func(c *gin.Context) {
		csvPath := getPath("csv")
		csvData, err := parse_modules.ParseCSV(csvPath, parse_modules.PersonCSV{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": csvData})
	})

	// Parse json
	r.GET("/json", func(c *gin.Context) {
		jsonPath := getPath("json")
		jsonData, err := parse_modules.ParseJSON(jsonPath, parse_modules.Person{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": jsonData})
	})

	// Parse text
	r.GET("/text", func(c *gin.Context) {
		textPath := getPath("text")
		textData, err := parse_modules.ParseTEXT(textPath)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": textData})
	})

	// Parse yaml
	r.GET("/yaml", func(c *gin.Context) {
		yamlPath := getPath("yaml")
		yamlData, err := parse_modules.ParseYAML(yamlPath, parse_modules.Person{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": yamlData})
	})

	// Parse xml
	r.GET("/xml", func(c *gin.Context) {
		xmlPath := getPath("xml")
		xmlData, err := parse_modules.ParseXML(xmlPath, parse_modules.People{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": xmlData})
	})

	// Fetch from python
	r.GET("/", func(c *gin.Context) {
		format := c.Query("format")

		resp, err := http.Get("http://localhost:8080/" + format)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, gin.H{"data": body})
	})

	r.Run(":8081")
}
