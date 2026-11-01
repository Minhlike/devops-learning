package main
import ("context"; "testing")
func TestReplay(t *testing.T) {
    seen:=map[string]bool{}
    if !handle(context.Background(),"e1",seen) || handle(context.Background(),"e1",seen) { t.Fatal("replay") }
}
func TestCancel(t *testing.T) {
    ctx,cancel:=context.WithCancel(context.Background());cancel()
    if handle(ctx,"e1",map[string]bool{}) { t.Fatal("cancelled work executed") }
}
