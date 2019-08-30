package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

var modifiedFiles map[string]bool

func getFiles(searchpath string, extension string) []string {
	var files []string
	err := filepath.Walk(searchpath, func(path string, info os.FileInfo, err error) error {
		if filepath.Ext(path) == extension {
			files = append(files, path)
		}
		return nil
	})
	if err != nil {
		panic(err)
	}
	return files
}

func findNewFiles(files []string) []string {
	var filesToModify []string
	for _, file := range files {
		_, alreadyModified := modifiedFiles[file]
		if alreadyModified == false {
			modifiedFiles[file] = true
			filesToModify = append(filesToModify, file)
		}
	}
	return filesToModify
}

func modifyFiles(files []string, message string) []string {
	var successfulFiles []string
	for _, f := range files {
		file, err := os.OpenFile(f, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		defer file.Close()
		if err != nil {
			log.Println(err)
		}
		if _, err := file.WriteString(message); err != nil {
			log.Println(err)
		} else {
			successfulFiles = append(successfulFiles, f)
		}
	}
	return successfulFiles
}

func postResults(server string, files []string) {
	address := fmt.Sprintf("%s/sand/results", server)
	for _, f := range files {
		fmt.Println(string(f))
	}
	results := strings.Join(files, ",")
	data, _ := json.Marshal(map[string]string{"modified_files": results})
	request(address, encode(data))
}

func request(address string, data []byte) []byte {
	req, _ := http.NewRequest("POST", address, bytes.NewBuffer(data))
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil
	}
	body, _ := ioutil.ReadAll(resp.Body)
	return decode(string(body))
}

func encode(b []byte) []byte {
	return []byte(base64.StdEncoding.EncodeToString(b))
}

func decode(s string) []byte {
	raw, _ := base64.StdEncoding.DecodeString(s)
	return raw
}

func runMission(server string, extension string, message string, rootDir string) {
	allFiles := getFiles(rootDir, extension)
	newFiles := findNewFiles(allFiles)
	successfulFiles := modifyFiles(newFiles, message)
	postResults(server, successfulFiles)
}

func main() {
	server := flag.String("server", "http://localhost:8888", "The FQDN of the server")
	duration := flag.String("duration", "60", "How long the mission should run (seconds)")
	extension := flag.String("extension", ".caldera", "What extension are we searching for")
	message := flag.String("message", "caldera wuz here", "What message should be inserted into the files")
	dir := flag.String("dir", "/", "Where should CALDERA start looking for files")
	flag.Parse()
	modifiedFiles = make(map[string]bool)
	fmt.Printf("Running mission for %s seconds, posting results to %s\n", *duration, *server)
	i, _ := strconv.Atoi(*duration)
	expires := time.Now().Add(time.Duration(i) * time.Second)
	for time.Now().Sub(expires) < 0 {
		fmt.Println("In mission loop...")
		runMission(*server, *extension, *message, *dir)
	}
	fmt.Println("Done with mission")
}

var key = "L26FTC4BJ8U0IMJ6SFLS0961ZGQJKA"
