import sys
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 1. BẢNG TÀI KHOẢN EMAIL
df_emails = pd.DataFrame([
    {"STT": 1, "Vai Trò": "Tài khoản Nhận (Nạn nhân / Receiver)", "Địa Chỉ Gmail": "huymang196@gmail.com", "Chức Năng": "Lắng nghe & tiếp nhận thư (IMAP SSL Inbox & Spam)"},
    {"STT": 2, "Vai Trò": "Tài khoản Gửi 1 (Attacker / Sender 1)", "Địa Chỉ Gmail": "huy162131@gmail.com", "Chức Năng": "Xoay vòng gửi thử nghiệm thư lừa đảo, malware, công việc"},
    {"STT": 3, "Vai Trò": "Tài khoản Gửi 2 (Attacker / Sender 2)", "Địa Chỉ Gmail": "huyk60049@gmail.com", "Chức Năng": "Xoay vòng gửi tấn công dồn dập Flood, mồi nhử USDT"}
])

# 2. BẢNG DANH SÁCH PROXY & QUỐC GIA
df_proxies = pd.DataFrame([
    {"STT": 1, "Proxy Server": "zl47158.ydns.eu:17501", "Quốc Gia (Location)": "Châu Âu (EU - Đức / Hà Lan)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 2, "Proxy Server": "zl47156.ydns.eu:17499", "Quốc Gia (Location)": "Châu Âu (EU - Pháp)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 3, "Proxy Server": "zl47157.ydns.eu:17500", "Quốc Gia (Location)": "Châu Âu (EU - Anh Quốc)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 4, "Proxy Server": "zl47154.ydns.eu:17497", "Quốc Gia (Location)": "Châu Âu (EU - Đức)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 5, "Proxy Server": "zl47163.ydns.eu:17506", "Quốc Gia (Location)": "Châu Âu (EU - Ba Lan)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 6, "Proxy Server": "zl47164.ydns.eu:17507", "Quốc Gia (Location)": "Châu Âu (EU - Séc)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 7, "Proxy Server": "zl47207.ydns.eu:17550", "Quốc Gia (Location)": "Châu Âu (EU - Thụy Điển)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 8, "Proxy Server": "zl47168.ydns.eu:17511", "Quốc Gia (Location)": "Châu Âu (EU - Ý)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 9, "Proxy Server": "zl47166.ydns.eu:17509", "Quốc Gia (Location)": "Châu Âu (EU - Tây Ban Nha)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 10, "Proxy Server": "zl47199.ydns.eu:17542", "Quốc Gia (Location)": "Châu Âu (EU - Thụy Sĩ)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 11, "Proxy Server": "zl47200.ydns.eu:17543", "Quốc Gia (Location)": "Châu Âu (EU - Áo)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 12, "Proxy Server": "zl47162.ydns.eu:17505", "Quốc Gia (Location)": "Châu Âu (EU - Bỉ)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 13, "Proxy Server": "zl47167.ydns.eu:17510", "Quốc Gia (Location)": "Châu Âu (EU - Phần Lan)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 14, "Proxy Server": "zl47170.ydns.eu:17513", "Quốc Gia (Location)": "Châu Âu (EU - Đan Mạch)", "Giao Thức": "HTTP / SSL Port 465"},
    {"STT": 15, "Proxy Server": "zl47151.ydns.eu:17494", "Quốc Gia (Location)": "Châu Âu (EU - Na Uy)", "Giao Thức": "HTTP / SSL Port 465"}
])

# 3. BẢNG CÁC NHÓM NỘI DUNG & DẤU HIỆU NHẬN DIỆN CHÍNH
df_patterns = pd.DataFrame([
    {
        "STT": 1,
        "Nhóm Đặc Trưng Đầu Vào": "Bẫy Tài Khoản (User / Pass / Credentials)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "Username:, Password:, User:, Pass:, Tài khoản bị khóa, Xác minh danh tính, Đăng nhập lại, Login, Credentials",
        "Mục Đích / Phân Loại AI": "Phát hiện tấn công giả mạo (Phishing) chiếm đoạt tài khoản",
        "Trọng Số / Tác Động": "Rất cao (Điểm rủi ro tăng mạnh)"
    },
    {
        "STT": 2,
        "Nhóm Đặc Trưng Đầu Vào": "Mồi Nhử Tiền Ảo (Crypto / USDT / Tài Chính)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "USDT, BTC, Crypto, Balance, Wallet, Legacy, Inheritance, 2,684,742.17 USDT, 5,000,000 USD, Airdrop, Metamask",
        "Mục Đích / Phân Loại AI": "Phát hiện lừa đảo chuyển nhượng tài sản ảo & Rút tiền giả",
        "Trọng Số / Tác Động": "Rất cao"
    },
    {
        "STT": 3,
        "Nhóm Đặc Trưng Đầu Vào": "Tệp Đính Kèm Nguy Hiểm (Malware Extensions)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": ".exe, .scr, .bat, .iso, .cmd, .vbs, .pdf.exe (đuôi kép ngụy trang)",
        "Mục Đích / Phân Loại AI": "Chặn mã độc thực thi, virus gián điệp và trojan",
        "Trọng Số / Tác Động": "Tuyệt đối (Gắn nhãn Spam/Mã độc ngay)"
    },
    {
        "STT": 4,
        "Nhóm Đặc Trưng Đầu Vào": "Đường Link & Tên Miền Rủi Ro Cao (URL Features)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "Nhiều URL trong thư, TLD đuôi lạ (.xyz, .cc, .top, .ru), Dịch vụ rút gọn link (bit.ly, tinyurl), Đường link trỏ về IP thô",
        "Mục Đích / Phân Loại AI": "Phát hiện website lừa đảo, điều hướng trang độc hại",
        "Trọng Số / Tác Động": "Trung bình - Cao"
    },
    {
        "STT": 5,
        "Nhóm Đặc Trưng Đầu Vào": "Tấn Công Dồn Dập (Flood / Sybil Anomaly)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "Gửi > 5 email / 60 giây từ cùng IP hoặc xoay vòng người gửi (Sybil), Tiêu đề trùng lặp nội dung",
        "Mục Đích / Phân Loại AI": "Phát hiện hành vi dội bom thư, phá hoại hạ tầng hòm thư",
        "Trọng Số / Tác Động": "Kích hoạt Cảnh báo Bất thường (Anomaly Alert)"
    },
    {
        "STT": 6,
        "Nhóm Đặc Trưng Đầu Vào": "Email Hợp Lệ (Ham / Thư Chuẩn)",
        "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "Họp nhóm đồ án, Báo cáo tiến độ môn học, Biên nhận tiền điện, Lời mời hội thảo AI, Lịch thi học phần, Slide thuyết trình .pdf",
        "Mục Đích / Phân Loại AI": "Phân loại thư công việc & học tập an toàn",
        "Trọng Số / Tác Động": "Điểm rủi ro thấp (< 50% - Nhãn 0 Sạch)"
    }
])

# 4. BẢNG CÁC TIÊU ĐỀ EMAIL CHỦ YẾU
df_subjects = pd.DataFrame([
    {"STT": 1, "Nhóm Chủ Đề": "Lừa đảo Crypto / Thừa kế", "Tiêu Đề Mẫu Chủ Yếu": "My precious legacy for you", "Đặc Trưng Chính": "Bẫy User/Pass + Số dư 2.6M USDT"},
    {"STT": 2, "Nhóm Chủ Đề": "Spam Quảng cáo Khuyến mãi", "Tiêu Đề Mẫu Chủ Yếu": "Tặng 100k trải nghiệm nhà cái uy tín", "Đặc Trưng Chính": "Chứa link cá cược, khuyến mãi nạp rút"},
    {"STT": 3, "Nhóm Chủ Đề": "Công việc & Học tập Hợp lệ", "Tiêu Đề Mẫu Chủ Yếu": "Họp nhóm đồ án Python chiều nay", "Đặc Trưng Chính": "Trao đổi nhóm, đính kèm file Slide.pdf"},
    {"STT": 4, "Nhóm Chủ Đề": "Tấn công Dồn dập (Flood Attack)", "Tiêu Đề Mẫu Chủ Yếu": "Claim your 500 USDT Airdrop Reward! [Dot 1..4]", "Đặc Trưng Chính": "Bắn dồn 4 đợt liên tục trong 60s"},
    {"STT": 5, "Nhóm Chủ Đề": "Mã độc thực thi (Malware)", "Tiêu Đề Mẫu Chủ Yếu": "Cập nhật bảng lương và thưởng nhân viên quý 3", "Đặc Trưng Chính": "Đính kèm file kép độc hại Bang_Luong.pdf.exe"},
    {"STT": 6, "Nhóm Chủ Đề": "Nộp bài tập học phần", "Tiêu Đề Mẫu Chủ Yếu": "Báo cáo tuần môn Học máy và Thị giác máy tính", "Đặc Trưng Chính": "Đính kèm file báo cáo chuẩn Bao_Cao_Tuan_4.pdf"},
    {"STT": 7, "Nhóm Chủ Đề": "Giả mạo ngân hàng (Phishing)", "Tiêu Đề Mẫu Chủ Yếu": "Cảnh báo bảo mật: Tài khoản bị truy cập trái phép", "Đặc Trưng Chính": "Link giả mạo ebanking dụ đăng nhập"},
    {"STT": 8, "Nhóm Chủ Đề": "Hóa đơn giao dịch hợp lệ", "Tiêu Đề Mẫu Chủ Yếu": "Biên nhận thanh toán tiền điện tháng 9", "Đặc Trưng Chính": "File hóa đơn điện tử chính thống"},
    {"STT": 9, "Nhóm Chủ Đề": "Mã độc dạng Script", "Tiêu Đề Mẫu Chủ Yếu": "Tài liệu hướng dẫn cài đặt phần mềm kích hoạt", "Đặc Trưng Chính": "Đính kèm file script nguy hiểm Crack_Tool.bat"}
])

# Ghi ra file Excel định dạng chuẩn UTF-8
excel_file = Path("Dau_Vao_He_Thong.xlsx")
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df_emails.to_excel(writer, sheet_name="1_Tai_Khoan_Email", index=False)
    df_proxies.to_excel(writer, sheet_name="2_Danh_Sach_Proxy", index=False)
    df_patterns.to_excel(writer, sheet_name="3_Dau_Hieu_Nhan_Dien_Noi_Dung", index=False)
    df_subjects.to_excel(writer, sheet_name="4_DanhMuc_Tieu_De_Mau", index=False)

# Ghi ra file CSV chuẩn UTF-8 with BOM để mở bằng Excel trên Windows không bị lỗi font
csv_summary = pd.concat([
    pd.DataFrame([{"Phần": "=== 1. TÀI KHOẢN EMAIL THAM GIA ===", "Chi Tiết 1": "", "Chi Tiết 2": "", "Chi Tiết 3": ""}]),
    df_emails.rename(columns={"STT": "Phần", "Vai Trò": "Chi Tiết 1", "Địa Chỉ Gmail": "Chi Tiết 2", "Chức Năng": "Chi Tiết 3"}),
    pd.DataFrame([{"Phần": "=== 2. CÁC NHÓM NỘI DUNG & DẤU HIỆU NHẬN DIỆN CHÍNH ===", "Chi Tiết 1": "", "Chi Tiết 2": "", "Chi Tiết 3": ""}]),
    df_patterns.rename(columns={"Nhóm Đặc Trưng Đầu Vào": "Phần", "Các Từ Khóa & Mẫu Nhận Diện Chủ Yếu": "Chi Tiết 1", "Mục Đích / Phân Loại AI": "Chi Tiết 2", "Trọng Số / Tác Động": "Chi Tiết 3"}),
    pd.DataFrame([{"Phần": "=== 3. DANH MỤC TIÊU ĐỀ MẪU CHỦ YẾU ===", "Chi Tiết 1": "", "Chi Tiết 2": "", "Chi Tiết 3": ""}]),
    df_subjects.rename(columns={"Nhóm Chủ Đề": "Phần", "Tiêu Đề Mẫu Chủ Yếu": "Chi Tiết 1", "Đặc Trưng Chính": "Chi Tiết 2", "STT": "Chi Tiết 3"})
], ignore_index=True)

csv_summary.to_csv("Dau_Vao_He_Thong.csv", index=False, encoding="utf-8-sig")
print("[+] Đã tạo thành công Dau_Vao_He_Thong.xlsx và Dau_Vao_He_Thong.csv (UTF-8 chuẩn không lỗi font)!")
