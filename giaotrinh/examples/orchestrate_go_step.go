package main

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"io"
	"os/exec"
	"strings"
	"time"
)

func runStep(python, probe, work, action string) string {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	cmd := exec.CommandContext(ctx, python, probe, action, work)
	input, err := cmd.StdinPipe()
	if err != nil {
		return "START_ERROR"
	}
	output, err := cmd.StdoutPipe()
	if err != nil {
		return "START_ERROR"
	}
	cmd.Stderr = io.Discard
	if err = cmd.Start(); err != nil {
		return "START_ERROR"
	}
	ready := make(chan string, 1)
	go func() {
		line, _ := bufio.NewReader(output).ReadString('\n')
		ready <- line
	}()
	select {
	case line := <-ready:
		if strings.TrimSpace(line) != "READY" {
			cancel()
			cmd.Wait()
			return "START_ERROR"
		}
	case <-time.After(10 * time.Second):
		cancel()
		cmd.Wait()
		return "START_TIMEOUT"
	}
	if _, err = io.WriteString(input, "go\n"); err != nil {
		cancel()
		cmd.Wait()
		return "IO_ERROR"
	}
	input.Close()
	done := make(chan error, 1)
	go func() { done <- cmd.Wait() }()
	select {
	case err = <-done:
		if err == nil {
			return "OK"
		}
		var exit *exec.ExitError
		if errors.As(err, &exit) {
			return fmt.Sprintf("EXIT %d", exit.ExitCode())
		}
		return "IO_ERROR"
	case <-time.After(500 * time.Millisecond):
		cancel()
		<-done
		return "TIMEOUT"
	}
}
