package main

import (
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/csv", func(c *gin.Context) {

		resp, _ := http.Get("http://localhost:8000/csv")

		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		c.JSON(200, gin.H{
			"message": string(body),
		})
	})
	r.Run() // listen and serve on 0.0.0.0:8080
}
