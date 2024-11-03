package main

import (
	"fmt"

	"example.com/greetings"
)

func main() {
	message := greetings.Hello("Miha")
	fmt.Println(message)
}
