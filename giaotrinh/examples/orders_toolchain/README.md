# orders-api: một hợp đồng tích hợp cục bộ

Đây là ví dụ học tập một host, Python 3.12+ và SQLite. Không cần cloud. Không sử dụng trên dữ liệu thật. `ci.yml` là ví dụ workflow cho **repository mẫu độc lập**; copy vào `.github/workflows/orders.yml` ở repository đó nếu muốn chạy GitHub Actions. Workflow trong thư mục này không chạy tự động trong repository giáo trình.

## Đường không cần Docker

Trong thư mục này, chạy `python -m unittest -v test_app.py`. Muốn chạy server, đặt `ORDERS_DB` tới một tệp trong thư mục thử nghiệm, `APP_REVISION` tới mã commit của ví dụ và chạy `python app.py`; sau đó chạy `python smoke.py` ở cửa sổ khác. Server mặc định chỉ nghe `127.0.0.1:8080`; trong container `HOST=0.0.0.0` để cổng xuất bản tới host loopback. `smoke.py` kiểm tạo rồi đọc lại một đơn và đối chiếu revision. Nó tạo một record thật trong fixture bạn đã chọn; đừng hướng nó vào dịch vụ sản xuất.

## Đường Compose cục bộ

Nếu có Docker Engine và Compose plugin: `docker compose up --build -d --wait`, sau đó `python smoke.py`. `docker compose down` chỉ dừng/xóa container/network; volume `orders-data` còn. **Không chạy `down -v` nếu muốn giữ dữ liệu**. Dùng `docker compose ps`, `docker compose logs api` và `docker volume ls` để kiểm từng vòng đời. Có thể đặt `FAIL_READINESS=1` khi tạo lại container để thấy `/healthz` vẫn 200 còn `/readyz` 503; sau thử nghiệm trả về `0` và dựng lại. Không sử dụng biến đó trong sản xuất.

## Hợp đồng và giới hạn

`POST /orders` nhận JSON `{"item":"Bút","quantity":1}` và trả 201 cùng ID; `GET /orders/{id}` đọc lại. `/healthz` chứng minh process trả lời HTTP; `/readyz` thử truy vấn database; `/metrics` cho hai counter trong **bộ nhớ một process**, reset khi khởi động lại. `X-App-Revision` và log JSON giúp nối request với revision, không chứng minh image digest. SQLite file nằm trong named volume ở Compose và trong đường `ORDERS_DB` ở local. Một process trên một host, không có TLS, xác thực, rate limit, backup, external secret store, high availability hay điều phối nhiều node. Trước khi dùng cho hệ thật, phải thiết kế các năng lực đó theo yêu cầu cụ thể.

Workflow chặn publish khi test và smoke thất bại (`needs: verify`). `publish` dùng quyền `packages: write` của `GITHUB_TOKEN`, push tag bằng commit SHA rồi đọc manifest digest. Tag là tên có thể đổi; khi đưa vào môi trường thực cần ghi digest bất biến, xác minh image runtime và tách quyền publish/deploy. `docker image inspect` trả image ID local, **không đồng nhất** với registry manifest digest. Bản ví dụ chưa có job triển khai; không được diễn giải CI xanh thành ứng dụng đã triển khai.
