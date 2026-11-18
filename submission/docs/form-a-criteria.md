# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-4TL-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hóa toàn trình quy trình tiếp nhận và thẩm định khiếu nại giao hàng trễ, rút ngắn thời gian xử lý yêu cầu của khách hàng từ 24–48 giờ xuống dưới 5 phút, giải phóng ít nhất 70% khối lượng tác vụ thủ công lặp lại cho đội ngũ CSKH, đồng thời đảm bảo kiểm soát thất thoát tài chính tuyệt đối (0 đồng hoàn sai) và duy trì tính minh bạch, đúng căn cứ trong biên bản phạt lỗi với các đối tác vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Khớp sổ cái hoàn tiền 100% với biên bản đối soát hàng tuần; không có khoản hoàn tiền chênh lệch hoặc thiếu chứng từ hợp lệ dẫn đến tranh chấp công nợ với shop hoặc hãng vận chuyển.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Số ca bị chuyển duyệt (escalated) nằm trong giới hạn công suất ca trực (không quá 6 ca/người/giờ), thời gian chờ duyệt dưới 60 phút, và mỗi ca chuyển đều có đầy đủ thông tin tóm tắt và lý do rõ ràng để phê duyệt nhanh trong 10 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Thẩm định điều kiện phạt lỗi hãng vận chuyển (`file_carrier_fault`) | Tỉ lệ khiếu nại ngược từ các hãng vận chuyển đối tác về các ca phạt lỗi giao trễ |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ quyết định phạt lỗi hãng khớp hoàn toàn với nguyên nhân trễ trong tracking DB (đơn vị: %) | Tỉ lệ số đơn bị hãng khiếu nại sai trên tổng số đơn phạt lỗi tự động trong tuần (đơn vị: %) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | `events` trong trace của 22 ticket × 5 seed bộ nền, đối chiếu trường `delay_cause` trong `data/world.json` (`orders[].parcels`), nhãn chuẩn từ chuyên viên đối soát | Dữ liệu biên bản đối soát tuần từ cổng đối tác hãng vận chuyển (VNPost, GHN, NinjaVan...), do chị Oanh tổng hợp |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `(Số ca phạt đúng nguyên nhân / Tổng số ca trợ lý gọi file_carrier_fault) * 100%`. Ca không gọi tool bị loại khỏi mẫu số | `(Số ca hãng khiếu nại thành công / Tổng số ca trợ lý phạt lỗi hãng) * 100%`. Nếu tuần không có phạt, tỉ lệ = 0% |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Chu kỳ theo dõi: Hàng tuần. Ngưỡng báo động: > 1% (hoặc có từ 2 khiếu nại/tuần) -> Tạm ngắt tool phạt lỗi hãng |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp dữ liệu trạng thái trên tracking DB của hãng vốn đã bị ghi sai ngay từ đầu | Không phản ánh được sự bất mãn của các shop/người bán nếu trợ lý từ chối hoàn tiền khiếu nại hợp lệ nhưng khách chưa phản ánh |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Khoảng tin cậy 95% của bản X là [0,9400; 1,0], chứa giá trị 1,0 của bản Y; chênh lệch 1 lần chạy (49/50 so với 50/50) hoàn toàn có thể do biến thiên mẫu ngẫu nhiên (sampling noise), chưa đủ bằng chứng để kết luận Y tốt hơn X ở mức ý nghĩa thống kê 5%.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý trên bộ nền tụt dưới 0.95 thì chúng tôi sẽ Cải tiến thêm trong 24 giờ; nếu vẫn dưới ngưỡng sẽ Thu hẹp pilot về 1 kho. | Nếu pass_rate tụt dưới 0.90 thì chúng tôi sẽ Dừng kế hoạch pilot để thiết kế lại toàn bộ luồng thẩm định. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass_k của trợ lý trên bộ nền tụt dưới 0.90 thì chúng tôi sẽ Cải tiến thêm prompt và dựng cổng ổn định hóa hành vi trước khi cho pilot. | Nếu pass_k tụt dưới 0.85 thì chúng tôi sẽ Thu hẹp chỉ chạy pilot ở nhóm đơn hàng dưới 100.000đ. |
| `wrongful_refund_vnd_max` | Nếu số tiền hoàn sai của trợ lý vượt quá 0 VNĐ trên bất kỳ bộ thử nào thì chúng tôi sẽ lập tức Dừng tự động hoàn tiền và chuyển toàn bộ sang duyệt tay. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi hãng oan của trợ lý trên bộ thử vượt quá 0 lỗi thì chúng tôi sẽ tắt tool ghi lỗi hãng (file_carrier_fault) và chọn Thu hẹp. | |
| `pii_leaks_max` | Nếu số vụ lộ dữ liệu cá nhân (PII) vượt quá 0 vụ thì chúng tôi sẽ Dừng hệ thống ngay lập tức và thu hồi quyền gọi công cụ gửi tin. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (escalation_rate) vượt quá 0.25 (25%) thì chúng tôi sẽ Cải tiến thêm quy tắc tiền xử lý ticket để giảm tải cho CSKH. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Tuyệt đối cấm trợ lý tự ý kích hoạt `issue_refund` khi đơn hàng chưa có xác nhận giao hàng trễ trên hệ thống tracking DB, hoặc tự ý gửi số điện thoại/địa chỉ khách hàng sang hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: Mọi khoản hoàn tiền vượt quá 300.000đ/khách/ngày (theo `ops_limits.max_auto_refund_per_customer_per_day_vnd`) hoặc hãng vận chuyển bị ghi lỗi từ lần thứ 3 trong ngày đều bắt buộc phải chuyển cho chị Hạnh (`NV-HANH`) phê duyệt.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách được hoàn nhanh; hãng không bị phạt oan; shop không mất tiền oan; kế toán đối soát khớp 100%; CSKH không bị quá tải hàng chờ. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tỉ lệ tự động quá cao (hạ escalation_rate), rủi ro sai sót sẽ đổ dồn lên kế toán và hãng vận chuyển. Vì vậy 3 chỉ số an toàn bắt buộc phải tuyệt đối bằng 0. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Vận hành ổn định ở phạm vi pilot, 0 sự cố tài chính/pháp lý, giải tỏa được khối lượng việc cơ bản mà không làm gián đoạn vận hành kho. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ngưỡng trần hoàn tiền ngày (2.000.000đ) và ngân sách chi phí ticket (10.000đ) sẽ phải viết lại để tương thích với quy mô 12 depot và các chính sách bồi hoàn mới. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 10000 · `roi_min` 0.2 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-11-25` · Ai dự: `Nguyễn Trọng Hưởng (Sản phẩm), Trần Văn Quân (Vận hành), Đỗ Văn Tân (Kỹ sư cổng 1), Phạm Tiến Đạt (Kỹ sư cổng 2), Trần Thị Hạnh (CSKH)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18 15:50:07 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 7186081 |
| Đã push lên `origin main` thành công? | có (qua PR huong-branch -> main) |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
