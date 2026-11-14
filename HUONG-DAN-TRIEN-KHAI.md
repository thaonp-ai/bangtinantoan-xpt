# Bảng tin An toàn – Hướng dẫn triển khai Cloudflare

## Triển khai lần đầu (giống web P&ID)
1. Cloudflare: *Workers & Pages → Create → Import a repository* (Workers Builds), chọn repo `bangtinantoan-xpt`.
   - Project name: `bangtinantoan-xpt`
   - Build command: *để trống*
   - Deploy command: `npx wrangler deploy` (mặc định)
2. Sau ~1 phút web có địa chỉ `https://bangtinantoan-xpt.<tài-khoản>.workers.dev`.
3. (Tùy chọn) Tên miền riêng: project → *Settings → Domains & Routes → Add → Custom domain*, ví dụ `bangtin.tenmien.vn`.

## Cập nhật dữ liệu hàng tuần
1. Nhập dữ liệu tuần mới vào `Bang tin an toan - Du lieu.xlsx` trong OneDrive (thư mục *Bang tin an toan hang tuan*), lưu file.
2. Nhắn Claude: “cập nhật bảng tin lên web”. Claude chép file Excel vào `web/data/bangtin.xlsx` và đẩy lên GitHub → Cloudflare tự triển khai lại trong khoảng 1 phút.
   (Hoặc tự làm: trên GitHub mở `web/data/` → *Add file → Upload files* → tải file Excel lên, đặt tên `bangtin.xlsx`.)

## Xuất PDF
Trên web: chọn tuần → **Xuất PDF** → máy in “Lưu dưới dạng PDF” (A4, dọc). Tên file tự đặt theo tuần.

## Xem trước dữ liệu trước khi đưa lên web
Mở file `Bang tin an toan.html` trên máy (Chrome/Edge) → **Mở file Excel** → bật **Tự động cập nhật**.
