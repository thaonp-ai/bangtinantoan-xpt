# Ghi chú cho Claude khi cập nhật repo này

Web tĩnh bảng tin an toàn hàng tuần Xưởng Phụ Trợ. Cloudflare Workers Builds tự triển khai từ nhánh `main` (assets-only, thư mục `web/`). Không có đăng nhập (người dùng chọn 11/2026).

## Cập nhật dữ liệu hàng tuần
- Nguồn: file Excel trên máy người dùng `C:\Users\Admin\OneDrive - PVFCCo\App Xuong Phu tro\Bang tin an toan hang tuan\Bang tin an toan - Du lieu.xlsx`.
- Stage file đó (device_stage_files), chép vào `web/data/bangtin.xlsx`, kiểm tra web đọc được (python3 -m http.server trong `web/` + google-chrome headless `--screenshot`), commit thẳng vào `main` với thông điệp “Cập nhật dữ liệu Tuần NN/YYYY”.
- Không sửa nội dung Excel của người dùng khi chỉ cập nhật dữ liệu.

## Cấu trúc Excel (web đọc theo tên sheet/tên cột, không phân biệt dấu)
- `CauHinh` (khóa/giá trị: tiêu đề, đơn vị, người ký, thông điệp mặc định, số tuần trên biểu đồ, lũy tiến đầu kỳ)
- `SoLieuTuan` (mỗi tuần 1 dòng: Năm, Tuần, ngày, GPLV, GPLV không tuân thủ, ĐNTĐ chủ trì/liên quan, Sự cố, Nearmiss, thẻ an toàn / KAT khắc phục ngay / KAT chờ khắc phục, thông điệp)
- `QuyDinh`, `TonDong` (+ảnh theo dòng), `GiaiPhap`, `BieuDuong` (+ảnh), `CongViecTuanToi`: Năm/Tuần chỉ ghi ở dòng đầu mỗi tuần (điền xuống).
- Lũy tiến = tổng các tuần cùng năm ≤ tuần đang xem + lũy tiến đầu kỳ.

## Giao diện
- `web/index.html` là bản build của app (logo nhúng base64). Bản dùng offline trên máy người dùng: `Bang tin an toan.html` cùng thư mục OneDrive — giữ hai bản giống nhau khi sửa giao diện.
- Trên web (http/https) app tải `data/bangtin.xlsx`, ẩn nút mở file; Xuất PDF = window.print (CSS @page A4).
- Màu thương hiệu: teal #549B9C / #2F6F70, cam #DF6437, PVFCCo xanh lá #009D48, navy #354085.
