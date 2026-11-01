package main
import ("context"; "fmt"; "os"; "os/signal"; "syscall")
// Checkpoint nền chỉ có một event trong bộ nhớ; chưa claim durable idempotency.
func handle(ctx context.Context, id string, seen map[string]bool) bool {
    if ctx.Err()!=nil || seen[id] { return false }; seen[id]=true; return true
}
func main() {
    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM); defer stop()
    fmt.Println("Worker checkpoint: no database consumer configured")
    <-ctx.Done()
}
