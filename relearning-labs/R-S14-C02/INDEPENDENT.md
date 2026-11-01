# Independent — bảo vệ kết luận từ trạng thái

Với một container health mới do bạn sở hữu, chứng minh process chính, đường stop và trạng thái kết thúc. Chọn thời hạn dừng phù hợp, giải thích vì sao exit code không đủ kết luận OOM hay hoàn tất mọi request. Không dùng fixture có dữ liệu hoặc workload cũ. Không cần gây SIGKILL/OOM để đạt.

Docs: Docker container stop và Dockerfile ENTRYPOINT. Nộp output có thời gian/exit code, State.OOMKilled, command và giải thích scope. Nếu host không có quyền, nộp blocked checkpoint, không tự khai PASS. Tutor đánh giá sau khi bạn nộp, không cung cấp lệnh giải ở đây.
