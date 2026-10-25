import streamlit as st
import json
import pandas as pd
import datetime
import config
from threat_analyzer import ThreatAnalyzer
from ip_extractor import get_ip_location
from export_excel import export_logs_to_excel
from check_proxies import check_all_proxies

st.set_page_config(page_title="AI Email Spam & Threat Detection", layout="wide", page_icon="🛡️")

st.title("🛡️ HỆ THỐNG PHÁT HIỆN EMAIL SPAM & TẤN CÔNG BẤT THƯỜNG")
st.caption("Ứng dụng học máy Random Forest kết hợp phân tích hành vi & Tần suất gửi (Flood Detection)")

# Load log dữ liệu
def load_logs():
    if config.DATABASE_LOG_PATH.exists():
        try:
            with open(config.DATABASE_LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

logs = load_logs()

# Sidebar: Test thủ công
st.sidebar.header("🧪 Thử nghiệm phân tích Email")
test_sender = st.sidebar.text_input("Người gửi (Sender):", value="unknown_scammer@crypto.xyz")
test_subject = st.sidebar.text_input("Tiêu đề (Subject):", value="My precious legacy for you")
test_body = st.sidebar.text_area(
    "Nội dung Email (Body):",
    value="Doctors told me cancer is incurable. rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)",
    height=150
)

if st.sidebar.button("🔍 Phân tích ngay"):
    analyzer = ThreatAnalyzer()
    res = analyzer.analyze_email(test_sender, test_subject, test_body)
    st.sidebar.divider()
    if res["is_spam"]:
        st.sidebar.error(f"🚨 KẾT QUẢ: SPAM / PHISHING ({res['spam_score']*100:.1f}%)")
    else:
        st.sidebar.success(f"✅ KẾT QUẢ: EMAIL HỢP LỆ ({res['spam_score']*100:.1f}%)")
        
    if res["is_flood_attack"]:
        st.sidebar.warning("⚠️ CẢNH BÁO TẤN CÔNG DỒN DẬP (FLOOD ATTACK)!")
    
    st.sidebar.json(res["indicators"])
    st.rerun()

# Sidebar: Quản lý & Lọc Proxy Đa Luồng Tốc Độ Cao
st.sidebar.divider()
st.sidebar.header("⚡ Bộ Lọc Proxy Đa Luồng Tốc Độ Cao")
st.sidebar.caption("Kiểm tra song song tới Google SMTP và tự động lọc danh sách Proxy sống vào `working_proxies.txt`.")
worker_count = st.sidebar.slider("Số luồng kiểm tra (Threads):", min_value=10, max_value=100, value=50, step=10)
timeout_sec = st.sidebar.slider("Thời gian chờ (Timeout giây):", min_value=2.0, max_value=8.0, value=4.0, step=1.0)

if st.sidebar.button(f"🚀 Bắt đầu Quét ({worker_count} Luồng)"):
    with st.sidebar.status(f"Đang kiểm tra kết nối Proxy ({worker_count} luồng)...", expanded=True) as status_box:
        live_list = check_all_proxies(max_workers=worker_count, timeout=timeout_sec)
        status_box.update(label=f"Hoàn tất! {len(live_list)} Proxy LIVE sẵn sàng!", state="complete", expanded=False)
    st.sidebar.success(f"✅ Đã lọc thành công {len(live_list)} Proxy sống vào `working_proxies.txt`!")

# Phần 1: Thống kê tổng quan
st.subheader("📊 Thống kê Hoạt động")
col1, col2, col3, col4 = st.columns(4)

total_emails = len(logs)
spam_count = sum(1 for e in logs if e.get("is_spam"))
flood_count = sum(1 for e in logs if e.get("is_flood_attack"))
legit_count = total_emails - spam_count

col1.metric("Tổng Email đã phân tích", total_emails)
col2.metric("Email Hợp lệ", legit_count)
col3.metric("Email Spam / Phishing", spam_count, delta=f"{spam_count/total_emails*100:.1f}%" if total_emails else "0%", delta_color="inverse")
col4.metric("Cảnh báo Flood/Sybil Attack", flood_count, delta="Cảnh báo", delta_color="inverse" if flood_count > 0 else "off")

col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("📊 Xuất Báo Cáo Ra File Excel (.xlsx)"):
        excel_path = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
        st.success(f"✅ Đã tạo file Excel thành công tại: `{excel_path}`")
        with open("Bao_Cao_Phat_Hien_Spam.xlsx", "rb") as f:
            st.download_button(
                label="⬇️ Tải Xuống File Báo Cáo Excel",
                data=f,
                file_name="Bao_Cao_Phat_Hien_Spam.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with col_btn2:
    if st.button("🗑️ Xóa Sạch Nhật Ký (Reset Data)"):
        with open(config.DATABASE_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        st.success("✅ Đã dọn sạch toàn bộ nhật ký cũ! Bảng dữ liệu đã được làm mới 100%.")
        st.rerun()

st.divider()



# Phần 2: Bảng chi tiết các email đã xử lý
st.subheader("📥 Nhật ký Email Real-time (Email Feeds)")

if logs:
    df_list = []
    for e in reversed(logs):
        dt_str = datetime.datetime.fromtimestamp(e.get("timestamp", 0)).strftime("%H:%M:%S %d/%m/%Y")
        status = "🚨 SPAM" if e.get("is_spam") else "✅ LEGIT"
        if e.get("is_flood_attack"):
            status += " | ⚠️ FLOOD"
            
        sender_ip = e.get("sender_ip", "Không xác định")
        location = get_ip_location(sender_ip)

        df_list.append({
            "Thời gian": dt_str,
            "Người gửi": e.get("sender"),
            "IP Nguồn (Sender IP)": sender_ip,
            "Vị trí / Quốc gia": location,
            "Tiêu đề": e.get("subject"),
            "File Đính Kèm": ", ".join(e.get("attachments", [])) if e.get("attachments") else "Không",
            "Điểm rủi ro": f"{e.get('spam_score', 0)*100:.1f}%",
            "Trạng thái": status,
            "Nội dung": e.get("body")[:90] + ("..." if len(e.get("body", "")) > 90 else "")
        })

    
    df = pd.DataFrame(df_list)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Chưa có email nào trong nhật ký. Hãy chạy script `python simulate_test.py` hoặc gửi thử qua khung thử nghiệm bên trái!")
