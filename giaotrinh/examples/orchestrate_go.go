// Demo only: policy "bad" deliberately ignores a failed step.
package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"time"
)

func main() {
	if len(os.Args) != 6 {
		fmt.Fprintln(os.Stderr, "usage: app bad|checked ok|fail|slow python probe workdir")
		os.Exit(2)
	}
	policy, mode := os.Args[1], os.Args[2]
	if (policy != "bad" && policy != "checked") ||
		(mode != "ok" && mode != "fail" && mode != "slow") {
		os.Exit(2)
	}
	python, probe, work := os.Args[3], os.Args[4], os.Args[5]
	for _, action := range []string{"precheck", "apply_" + mode, "verify"} {
		ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
		cmd := exec.CommandContext(ctx, python, probe, action, work)
		cmd.Stdout, cmd.Stderr = io.Discard, io.Discard
		err := cmd.Run()
		timedOut := errors.Is(ctx.Err(), context.DeadlineExceeded)
		cancel()
		if err != nil {
			reason := "START_OR_IO_ERROR"
			var exit *exec.ExitError
			if timedOut {
				reason = "TIMEOUT"
			} else if errors.As(err, &exit) {
				reason = fmt.Sprintf("EXIT %d", exit.ExitCode())
			}
			fmt.Fprintf(os.Stderr, "%s: %s\n", action, reason)
			if policy == "checked" {
				os.Exit(1)
			}
		}
	}
	fmt.Println("DEPLOY_OK")
}
