# Đầu vào hình V30 — P13.C01.L03

Biểu đồ từ `five_minute.csv` và `monthly.csv`: (1) valid/bad theo ô 5 phút, (2) đường burn 1h và 5m ở cuối fixture, ngưỡng 14,4, (3) tổng 30 ngày: 1.000 budget, 700 đã dùng, 300 còn. Ghi rõ dữ liệu giả định, đơn vị của từng trục, cửa sổ và population. Ở ô mất scrape, vẽ khoảng trống/UNKNOWN thay vì 0 bad. Dataset chỉ hỗ trợ giá trị burn ở cuối giờ; A2 không vẽ đường burn 1h tại các điểm trước khi đủ dữ liệu một giờ. Công thức và kết quả phải lấy từ `verify.py`, không nội suy số liệu ngoài fixture.
