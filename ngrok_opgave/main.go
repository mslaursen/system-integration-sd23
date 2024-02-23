package main

import (
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/mo", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"data": time.Now().UTC(),
		})
	})

	r.GET("/mo/html", func(c *gin.Context) {
		html := `
		<!DOCTYPE html>
		<html>
		<head>
			<script src="https://unpkg.com/htmx.org"></script>
		</head>
		<body>
			<button hx-get="https://b2b3-195-249-146-100.ngrok-free.app/date" hx-target="#response-data" hx-swap="innerHTML">Get data</button>
			<div id="response-data">Response data will appear here</div>
		</body>
		</html>
		`
		c.Data(200, "text/html; charset=utf-8", []byte(html))
	})

	r.Run()
}
