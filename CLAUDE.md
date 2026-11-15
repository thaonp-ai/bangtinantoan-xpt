# Ghi chú cho Claude khi cập nhật repo này

Web tĩnh bảng tin an toàn hàng tuần Xưởng Phụ Trợ. Cloudflare Workers Builds tự triển khai từ nhánh `main` (assets-only, thư mục `web/`). Không có đăng nhập (người dùng chọn 11/2026).

## Cập nhật dữ liệu hàng tuần
- Nguồn: file Excel trên máy người dùng `C:\Users\Admin\OneDrive - PVFCCo\App Xuong Phu tro\Bang tin an toan hang tuan\Bang tin an toan hang tuan.xlsx` (file gốc của người dùng, chọn 14/11/2026; KHÔNG dùng `Bang tin an toan - Du lieu.xlsx``.
- Stage file đó (device_stage_files), chép vào `web/data/bangtin.xlsx`, kiểm tra web đọc được (python3 -m http.server trong `web/` + google-chrome headless `--screenshot`), commit thẳng vào `main` với thông điệp “Cập nhật dữ liệu Tuần NN/YYYY”.
- Không sửa nội dung Excel của người dùng khi chỉ cập nhật dữ liệu.

## Cấu trúc Excel (file gốc, 1 sheet, mỗi tuần một khối dòng)
- Dòng 2–3 là tiêu đề (gộp ô): Tuần | GPLV (Số GPLV, Số GPLV không tuân thủ) | ĐNTĐ chủ trì | ĐNTĐ liên quan (từ Tuần 46) | Sự cố | Nearmiss | Số thẻ STOP (an toàn, KAT khắc phục ngay, KAT chờ khắc phục) | Quy định an toàn | Tồn đọng | Hành động khắc phục | Giải pháp và đề xuất | Biểu dương | Các công việc lưu ý tuần tới.
- Mỗi tuần: số tuần + số liệu ở dòng đầu khối (ô gộp), các danh sách mỗi mục một dòng; tuần mới thêm ngay dưới tuần trước. Web nhận cột theo tên tiêu đề (không phân biệt dấu), `buildFromWide()` trong index.html.
- Dữ liệu trong Excel hiện có Tuần 42–46/2026 (Tuần 42–44 nhập từ PDF cũ ngày 15/11/2026, đã sửa chính tả). Cột Q:R tiêu đề "Ảnh hiện trạng", cột S "Ảnh sau khắc phục": ảnh đặt ở cột nào thì web hiểu theo tiêu đề cột đó (ô gộp → lấy tiêu đề cột gần nhất bên trái); ảnh ở cột Hành động/“sau khắc phục” hiển thị ở ô Hành động khắc phục.
- Ô Hành động khắc phục có mà Tồn đọng trống → nối vào tồn đọng phía trên. Ảnh nổi gắn vào tồn đọng cùng dòng/dòng trên gần nhất trong khối (ảnh ở cột Biểu dương → biểu dương); ảnh lấn lên dòng tiêu đề tính vào dòng dữ liệu đầu tiên.
- Không có cột Năm: năm lấy `MAC_DINH.year`, tự tăng khi số tuần quay về nhỏ hơn. Web luôn hiển thị 2 ô "ĐNTĐ chủ trì" / "ĐNTĐ liên quan" (người dùng yêu cầu 15/11/2026): cột có tiêu đề chứa "chủ trì" / "liên quan" (dòng 3, dưới nhóm ĐNTĐ). Nếu Excel còn 1 cột "ĐNTD" cũ thì số đó tính là chủ trì, liên quan = 0.
- Hằng `MAC_DINH` trong index.html: người ký, thông điệp, số liệu T34–T44/2026 (lấy từ PDF Tuần 45, để vẽ biểu đồ/lũy tiến; tuần có trong Excel thì Excel thắng), `MAC_DINH.anchor` = lũy tiến năm tính đến hết Tuần 46/2026 do người dùng cung cấp 15/11/2026 (GPLV 2292, không tuân thủ 2, ĐNTĐ chủ trì 7, liên quan 7, sự cố 7, nearmiss 1, thẻ an toàn 2949, KAT khắc phục ngay 1405, chờ khắc phục 664). Lũy tiến đầu kỳ tự tính = mốc − tổng các tuần có dữ liệu ≤ tuần mốc, nên tuần sau = lũy tiến tuần trước + số tuần đó. Sang năm mới cần mốc mới (hoặc đặt mốc = 0). Đổi người ký/thông điệp: sửa `MAC_DINH.cfg` ở cả hai bản HTML.
- Lũy tiến = tổng các tuần cùng năm ≤ tuần đang xem + lũy tiến đầu kỳ (suy ra từ mốc).
- Web vẫn đọc được định dạng nhiều sheet (CauHinh/SoLieuTuan/...) nếu sau này dùng.

## Giao diện
- `web/index.html` là bản build của app (logo nhúng base64). Bản dùng offline trên máy người dùng: `Bang tin an toan.html` cùng thư mục OneDrive — giữ hai bản giống nhau khi sửa giao diện.
- Trên web (http/https) app tải `data/bangtin.xlsx`, ẩn nút mở file; Xuất PDF = window.print (CSS @page A4).
- Màu thương hiệu: teal #549B9C / #2F6F70, cam #DF6437, PVFCCo xanh lá #009D48, navy #354085.
