# NHÍT AI – bản MVP chạy thật

## Yêu cầu
- Python 3.10 trở lên
- Một API key Pollinations (tạo tại https://enter.pollinations.ai)
- Kết nối Internet

## Chạy trên máy tính
1. Giải nén thư mục.
2. Mở terminal trong thư mục `nhit_ai`.
3. Cài thư viện:
   `pip install -r requirements.txt`
4. Sao chép `.env.example` thành `.env`, điền API key:
   `POLLINATIONS_API_KEY=YOUR_KEY`
5. Chạy:
   `uvicorn server:app --host 0.0.0.0 --port 8000`
6. Trên máy tính mở `http://127.0.0.1:8000`.
7. Trên điện thoại Android cùng Wi-Fi, mở `http://IP_MAY_TINH:8000` (thay IP_MAY_TINH bằng địa chỉ LAN của máy tính).

## Đưa lên máy chủ Internet
Đưa toàn bộ thư mục lên một dịch vụ hosting hỗ trợ Python/FastAPI. Đặt biến môi trường `POLLINATIONS_API_KEY` trong phần Environment/Secrets của hosting, không đưa khóa vào HTML hoặc GitHub. Lệnh chạy:
`uvicorn server:app --host 0.0.0.0 --port $PORT`

## Quan trọng về miễn phí
NHÍT AI không thu phí riêng, nhưng nhà cung cấp AI có thể yêu cầu API key, hạn mức, credit hoặc tính phí theo model. Hãy kiểm tra giá/credit và model hiện có trong tài khoản trước khi tạo video. Không có cam kết video AI miễn phí vô hạn.

## Phạm vi bản này
- Kịch bản: gọi API chat completions.
- Ảnh: gọi API image.
- Video: gọi API video, chờ MP4 trả về.
- SRT: tạo phụ đề cơ bản từ từng dòng, thời gian chia đều; phải căn chỉnh lại để khớp tiếng.
- Model: xem danh mục model trực tiếp từ máy chủ.

Đây là bản MVP có kết nối API thật, chưa phải hệ thống dựng phim hoàn chỉnh: chưa có đồng bộ khẩu hình, clone giọng, quản lý nhân vật xuyên cảnh, timeline dựng phim hoặc ghép nhiều clip.


## Cập nhật kết nối Pollinations (14-11-2026)
- Danh mục model dùng `GET https://gen.pollinations.ai/v1/models`.
- API tạo nội dung cần Secret Key `sk_` trong biến môi trường `POLLINATIONS_API_KEY`.
- Chỉ chọn model có giá `0` trong danh mục nếu muốn tránh phí model; một model giá 0 không có nghĩa mọi model hoặc mọi tác vụ đều miễn phí.
- Secret Key là khóa máy chủ: không đưa vào `static/index.html`, ứng dụng Android, ảnh chụp màn hình hoặc kho mã công khai.
- Tạo khóa với quyền model phù hợp (text/image/video), ngân sách và thời hạn nhỏ để kiểm soát chi phí.
- Model IDs có thể thay đổi; dùng danh mục trực tiếp thay vì đoán tên model.
- Tham khảo: https://gen.pollinations.ai/docs và https://enter.pollinations.ai/
