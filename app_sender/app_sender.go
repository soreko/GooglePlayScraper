
package main

import "fmt"
import "os"
import "log"
import "bufio"
import "net/http"

func main() {
	file, err := os.Open("IDs.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		resp, err := http.Get("http://localhost:5000/ScrapApp?id=" + scanner.Text())
		fmt.Println(resp, err)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}
