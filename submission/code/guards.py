"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    # Cổng 1: Ghim phiên bản chính sách có hiệu lực tại ngày as_of để phòng ngừa policy drift
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # Cổng 2: Kiểm soát chặt chẽ lệnh hoàn tiền (issue_refund)
    if action.get("tool") == "issue_refund":
        # 2a. Chặn prompt injection ép trừ tiền MERCHANT
        if action.get("payer") == "MERCHANT":
            return Verdict.deny("chặn lệnh hoàn tiền cho Merchant không hợp lệ từ chỉ dẫn người dùng")

        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.deny("không tìm thấy đơn hàng tương ứng")

        # 2b. Đối chiếu quyền lợi bồi hoàn với nguồn sự thật (tracking DB)
        worst = max(order["parcels"], key=lambda p: H.db_delay_days(p, ctx.as_of))
        db_delay = H.db_delay_days(worst, ctx.as_of)
        cause = worst.get("delay_cause") or ("CARRIER" if db_delay > 0 else None)
        pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        final_amount = action.get("amount_vnd", 0)
        if pol:
            entitled_vnd = H.entitlement_vnd(pol, order, db_delay, cause)
            if action.get("amount_vnd", 0) > entitled_vnd:
                if entitled_vnd == 0:
                    return Verdict.deny("đơn hàng không đủ điều kiện bồi hoàn theo dữ liệu tracking thực tế")
                final_amount = entitled_vnd

        # 2c. Kiểm soát trần hoàn tiền tự động trong ngày (ngân sách Finance)
        cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        limit_cap = ctx.tools.ops_limits().get("daily_auto_refund_budget_vnd")
        if limit_cap is not None:
            cap = min(cap, limit_cap) if cap is not None else limit_cap
        if cap is not None:
            spent = ctx.tools.auto_refund_today_vnd()
            if spent + final_amount > cap:
                return Verdict.escalate("vượt trần ngân sách hoàn tự động trong ngày, chuyển người duyệt")

        if final_amount != action.get("amount_vnd", 0):
            return Verdict.modify("điều chỉnh số tiền bồi hoàn theo đúng quyền lợi tracking DB", amount_vnd=final_amount)

    # Cổng 3: Kiểm soát lệnh ghi lỗi hãng vận chuyển (file_carrier_fault)
    if action.get("tool") == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            parcel = next((p for p in order["parcels"] if p["parcel_id"] == action.get("parcel_id")), None)
            if not parcel:
                parcel = max(order["parcels"], key=lambda p: H.db_delay_days(p, ctx.as_of))
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            if pol:
                if not H.carrier_at_fault(pol, parcel, db_delay):
                    return Verdict.deny("không đủ điều kiện ghi phạt lỗi hãng theo dữ liệu tracking thực tế")
                if action.get("delay_days", 0) != db_delay:
                    return Verdict.modify("chuẩn hoá số ngày trễ theo tracking DB", delay_days=db_delay)

    return Verdict.allow()
