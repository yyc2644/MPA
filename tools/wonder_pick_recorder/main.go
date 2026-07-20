package main

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		fail("usage: wonder_pick_recorder <maa-image> [project-root]")
	}

	source := filepath.Clean(os.Args[1])
	root, err := outputRoot(os.Args)
	if err != nil {
		fail(err.Error())
	}

	now := time.Now()
	directory := filepath.Join(root, "records", "wonder_pick", now.Format("2006-01-02"))
	if err := os.MkdirAll(directory, 0o755); err != nil {
		fail(fmt.Sprintf("create result directory: %v", err))
	}

	extension := strings.ToLower(filepath.Ext(source))
	if extension == "" {
		extension = ".png"
	}
	filename := fmt.Sprintf("wonder-pick-%s%s", now.Format("150405.000"), extension)
	destination := filepath.Join(directory, filename)

	if err := copyFile(source, destination); err != nil {
		fail(fmt.Sprintf("save result screenshot: %v", err))
	}

	fmt.Printf("Wonder Pick result saved: %s\n", destination)
}

func outputRoot(args []string) (string, error) {
	if len(args) >= 3 && strings.TrimSpace(args[2]) != "" {
		return filepath.Abs(filepath.Clean(args[2]))
	}

	executable, err := os.Executable()
	if err != nil {
		return "", fmt.Errorf("resolve executable: %w", err)
	}
	return filepath.Dir(filepath.Dir(executable)), nil
}

func copyFile(source string, destination string) error {
	input, err := os.Open(source)
	if err != nil {
		return err
	}
	defer input.Close()

	output, err := os.OpenFile(destination, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0o644)
	if err != nil {
		return err
	}

	if _, err := io.Copy(output, input); err != nil {
		output.Close()
		_ = os.Remove(destination)
		return err
	}
	return output.Close()
}

func fail(message string) {
	fmt.Fprintln(os.Stderr, message)
	os.Exit(1)
}
