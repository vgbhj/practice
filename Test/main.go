package main

import (
	"fmt"
	"slices"
)

func carFleet(target int, position []int, speed []int) int {
	m := make(map[int]int)

	for i := range len(position) {
		m[position[i]] = speed[i]
	}

	slices.Sort(position)

	var stack []int

	var tmp_arr []int // float ???

	for _, value := range position {
		tmp_arr = append(tmp_arr, (target-value)/m[value])
	}

	for _, value := range tmp_arr {
		for len(stack) != 0 && value >= stack[len(stack)-1] {
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, value)
	}

	return len(stack)
}

func main() {
	t := 10
	arr1 := []int{6, 8}
	arr2 := []int{3, 2}

	fmt.Println(carFleet(t, arr1, arr2))
}
