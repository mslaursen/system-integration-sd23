package main

import (
	"log"
	"net/http"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	for {
		_, err := w.Write([]byte("data: " + time.Now().UTC().String() + "\n\n"))
		if err != nil {
			return
		}
		w.(http.Flusher).Flush()
		time.Sleep(1 * time.Second)
	}
}

func main() {
	http.HandleFunc("/sse", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
