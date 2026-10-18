// Demo only: policy "bad" deliberately ignores a failed step.
package main

import (
	"fmt"
	"os"
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
		status := runStep(python, probe, work, action)
		if status != "OK" {
			fmt.Fprintf(os.Stderr, "%s: %s\n", action, status)
			if policy == "checked" {
				os.Exit(1)
			}
		}
	}
	fmt.Println("DEPLOY_OK")
}
