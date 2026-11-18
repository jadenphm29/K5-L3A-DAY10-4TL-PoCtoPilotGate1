# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): 4TL
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-4TL-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Trọng Hưởng | 2A202603626 | Sản phẩm và kinh doanh | x |
|   2 | Trần Minh Tân | 2A202603688 | Kỹ sư cổng 1 | |
|   3 | Phạm Tiến Đạt | | Kỹ sư cổng 2 | |
|   4 | Trần Văn Quân | | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TranMinhTan-2A202603688

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư cổng 1 (Core Guards & Systems).
- Phụ trách chính:
  + Chạy mốc base (Lệnh 2, Lệnh 4): Phiếu B mục B1, B0 dòng 1.
  + Thiết kế và lập trình các cổng phòng ngừa cấp hệ thống trong `lab10/guards.py` (`pre_guard`, `write_gate`): Phiếu B mục B7.1 (Câu 2.6).
  + Xây dựng giải pháp tránh rò rỉ dữ liệu khi phát triển cổng: Phiếu B mục B7.2 (Câu 2.7).
  + Kiểm thử và xác nhận 2 ticket hiểm ad-hoc ở mốc after: Phiếu B mục B7.3 (Câu 2.8).
  + Chốt cổng vòng 1 (Lệnh 5: checkpoint) và đánh giá mốc prepared: Phiếu B mục B0 dòng 2, dòng 3 và mục B8.
  + Sửa code cổng xử lý sự cố ở vòng 2 (Câu 3.5).

### Đóng góp cụ thể

- Chạy đánh giá baseline phát hiện ca lỗi chìm nguy hiểm `T-002@55` (model override số ngày từ DB gây hoàn sai 20.000đ và phạt oan hãng VNX).
- Xây dựng 3 tầng cổng phòng ngừa trong `lab10/guards.py`:
  1. `pre_guard`: Tự động ghim phiên bản chính sách có hiệu lực tại ngày `ctx.as_of`, chống trôi dạt chính sách (policy drift).
  2. `write_gate` (`issue_refund`): Chặn prompt injection chiếm quyền trừ tiền Merchant; đối chiếu quyền lợi bồi hoàn với tracking DB, chặn hoàn tiền sai và chuẩn hóa tiền hoàn về đúng entitlement của DB.
  3. `write_gate` (`file_carrier_fault`): Đối chiếu số ngày trễ và điều kiện phạt hãng với DB, chặn hoàn toàn việc ghi phạt oan đối tác vận chuyển.
- Kết quả: Đưa toàn bộ 110/110 trials bộ nền về trạng thái xanh (pass_rate 1.0, pass_k 1.0, hoàn sai 0đ, lỗi hãng oan 0), giữ ROI 1.24 và không ca nào bị ùn.
- Chốt checkpoint vòng 1 (`113ffb04`) niêm phong cổng vòng 1 và chạy đánh giá mốc `prepared`.

### Bằng chứng

- Mã lần chạy:
  + Baseline: `R-base-before-20261118-171955-ae5895`
  + After: `R-base-after-20261118-172710-f46094`
  + Prepared: `R-base-prepared-20261118-173351-f46094`
- Hash checkpoint mốc prepared: `113ffb04`
- Dòng trong phiếu: B0, B1, B7.1, B7.2, B7.3, B8 trong `templates/form-b-evaluation-gates.md`.

### Exit ticket

- Một điều học được: Cổng phòng ngừa cấp hệ thống (system-level deterministic guards) nằm ngoài prompt và model là chốt chặn phòng thủ thiết yếu nhất để ngăn chặn lỗi chìm và prompt injection trong các ứng dụng AI agent có quyền ghi sổ (write actions).
- Một điều còn chưa chắc: Khi đối mặt với sự cố thực tế ở vòng 2 (phút 125), việc phân định giữa giải pháp sửa bằng code cổng vs sửa bằng cấu hình con người / chính sách vận hành cần cân nhắc kỹ để tránh tăng chi phí hoặc gây ùn tắc hàng chờ duyệt.
