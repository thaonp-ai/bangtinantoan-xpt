# Bảng tin An toàn Vệ sinh Lao động – Xưởng Phụ Trợ (Đạm Phú Mỹ)

Web xem bảng tin an toàn hàng tuần. Dữ liệu lấy trực tiếp từ file Excel `web/data/bangtin.xlsx`.

- `web/index.html` – giao diện (một file, không cần build): chọn tuần, xuất PDF (in A4 từ trình duyệt)
- `web/data/bangtin.xlsx` – dữ liệu (bản sao của file gốc `Bang tin an toan hang tuan.xlsx` trên OneDrive)
- `web/nhansu.html` + `web/data/nhansu.json` – tab Nhân sự (link `#nhan-su`)
- `src/worker.js` – API `/api/nhansu` (lưu chỉnh sửa nhân sự vào Cloudflare KV, mật khẩu quản trị)
- `wrangler.jsonc` – cấu hình Cloudflare (Workers + file tĩnh)

Link từng tuần: thêm `#tuan-45-2026` vào cuối địa chỉ.
