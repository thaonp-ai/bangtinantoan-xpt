# Bảng tin An toàn – Hướng dẫn triển khai Cloudflare

## Triển khai lần đầu (giống web P&ID)
1. Cloudflare: *Workers & Pages → Create → Import a repository* (Workers Builds), chọn repo `xuongphutrodpm`.
   - Project name: `xuongphutrodpm` (Worker và repo GitHub cùng đổi từ `bangtinantoan-xpt` ngày 17/11/2026)
   - Build command: *để trống*
   - Deploy command: `npx wrangler deploy` (mặc định)
2. Sau ~1 phút web có địa chỉ `https://xuongphutrodpm.<tài-khoản>.workers.dev`.
3. (Tùy chọn) Tên miền riêng: project → *Settings → Domains & Routes → Add → Custom domain*, ví dụ `bangtin.tenmien.vn`.

## Cập nhật dữ liệu hàng tuần
1. Nhập dữ liệu tuần mới vào file gốc `Bang tin an toan hang tuan.xlsx` trong OneDrive (thư mục *Bang tin an toan hang tuan*): thêm khối Tuần mới ngay dưới tuần trước, lưu file.
2. Nhắn Claude: “cập nhật bảng tin lên web”. Claude chép file Excel vào `web/data/bangtin.xlsx` và đẩy lên GitHub → Cloudflare tự triển khai lại trong khoảng 1 phút.
   (Hoặc tự làm: trên GitHub mở `web/data/` → *Add file → Upload files* → tải file Excel lên, đặt tên `bangtin.xlsx`.)

## Xuất PDF
Trên web: chọn tuần → **Xuất PDF** → máy in “Lưu dưới dạng PDF” (A4, dọc). Tên file tự đặt theo tuần.

## Xem trước dữ liệu trước khi đưa lên web
Mở file `Bang tin an toan.html` trên máy (Chrome/Edge) → **Mở file Excel** → bật **Tự động cập nhật**.

## Tab Nhân sự (thêm 17/11/2026)
Web có 2 tab: **Bảng tin an toàn** và **Nhân sự** (link riêng: thêm `#nhan-su` vào cuối địa chỉ). Tab Nhân sự ai có link cũng xem được; chỉ quản trị viên (có mật khẩu) được thêm/sửa/xóa/nhập dữ liệu.

### Đăng nhập quản trị (dùng chung cả web)
- Nút **🔒 Đăng nhập** ở góc phải thanh *Xưởng Phụ Trợ*. Tài khoản: **admin** (mật khẩu ban đầu Claude gửi trong chat ngày 17/11/2026 — nên đổi ngay: bấm *👤 admin ▾ → Đổi mật khẩu*).
- Chưa đăng nhập: ai cũng xem được, không sửa được. Đăng nhập rồi: hiện các nút Thêm/Sửa/Xóa/Nhập dữ liệu/Khôi phục ở tab Nhân sự. Phiên đăng nhập giữ 7 ngày trên trình duyệt đó.
- Kho lưu dữ liệu (Workers KV) được Cloudflare tự tạo khi triển khai, không cần làm tay.
- Quên mật khẩu: nhờ Claude đặt lại.

### Cập nhật dữ liệu nhân sự
- **Trên web:** bấm *🔒 Đăng nhập* (góc phải thanh trên cùng) → sửa từng người, hoặc *Nhập dữ liệu* (file CSV cùng mẫu "Báo cáo nhân sự" hoặc file JSON backup). Lưu ngay, mọi người thấy.
- **Qua Claude:** gửi file CSV mới → Claude cập nhật `web/data/nhansu.json` và đẩy lên GitHub. File mới sẽ thay cho các chỉnh sửa cũ trên web, nên trước khi gửi hãy *Xuất CSV* từ web, sửa trên file đó rồi gửi.
- *Khôi phục file gốc*: bỏ mọi chỉnh sửa trên web, quay về `web/data/nhansu.json`.
