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

# Dữ liệu chuẩn xác của 3 nhóm thành phần Đầu vào (Input)
data_input = [
    {
        "STT": 1,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huy162131@gmail.com",
        "IP_Nguon": "185.220.101.5",
        "Quoc_Gia": "Châu Âu (EU - Đức)",
        "Thoi_Gian_Gui": "08:15:20 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "My precious legacy for you",
        "Noi_Dung_Than_Thu": "Doctors told me cancer is incurable. I have decided to travel alone and bid farewell. rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Lừa đảo Crypto / Bẫy chiếm tài khoản User-Pass"
    },
    {
        "STT": 2,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "194.126.177.21",
        "Quoc_Gia": "Châu Âu (EU - Pháp)",
        "Thoi_Gian_Gui": "08:20:11 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Tặng 100k trải nghiệm nhà cái uy tín",
        "Noi_Dung_Than_Thu": "Đăng ký ngay nhận 100k miễn phí vào tài khoản cá cược nạp rút siêu nhanh click tại link https://bet88-bonus.xyz săn thưởng hôm nay!",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Spam quảng cáo cờ bạc / Link độc hại"
    },
    {
        "STT": 3,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huy162131@gmail.com",
        "IP_Nguon": "113.190.234.12",
        "Quoc_Gia": "Việt Nam (VNPT)",
        "Thoi_Gian_Gui": "09:05:40 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Họp nhóm đồ án Python chiều nay",
        "Noi_Dung_Than_Thu": "Chào bạn, chiều nay 14h nhóm mình họp online qua Google Meet để chốt slide báo cáo đồ án và kiểm tra các module nhé.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Slide_Thuyet_Trinh.pdf",
        "Kich_Ban_Thu_Nghiem": "Email công việc / Học tập chuẩn hợp lệ (Ham)"
    },
    {
        "STT": 4,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "185.246.128.80",
        "Quoc_Gia": "Châu Âu (EU - Ba Lan)",
        "Thoi_Gian_Gui": "09:30:01 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Claim your 500 USDT Airdrop Reward! [Dot 1]",
        "Noi_Dung_Than_Thu": "Congratulations! Your email won the lucky draw. Visit metamask-claim.xyz and enter your credentials now to claim reward.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Tấn công dồn dập Flood Attack (Gửi liên tiếp đợt 1)"
    },
    {
        "STT": 5,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "185.246.128.80",
        "Quoc_Gia": "Châu Âu (EU - Ba Lan)",
        "Thoi_Gian_Gui": "09:30:15 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Claim your 500 USDT Airdrop Reward! [Dot 2]",
        "Noi_Dung_Than_Thu": "Congratulations! Your email won the lucky draw. Visit metamask-claim.xyz and enter your credentials now to claim reward.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Tấn công dồn dập Flood Attack (Gửi liên tiếp đợt 2)"
    },
    {
        "STT": 6,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "185.246.128.80",
        "Quoc_Gia": "Châu Âu (EU - Ba Lan)",
        "Thoi_Gian_Gui": "09:30:28 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Claim your 500 USDT Airdrop Reward! [Dot 3]",
        "Noi_Dung_Than_Thu": "Congratulations! Your email won the lucky draw. Visit metamask-claim.xyz and enter your credentials now to claim reward.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Tấn công dồn dập Flood Attack (Gửi liên tiếp đợt 3)"
    },
    {
        "STT": 7,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "185.246.128.80",
        "Quoc_Gia": "Châu Âu (EU - Ba Lan)",
        "Thoi_Gian_Gui": "09:30:42 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Claim your 500 USDT Airdrop Reward! [Dot 4]",
        "Noi_Dung_Than_Thu": "Congratulations! Your email won the lucky draw. Visit metamask-claim.xyz and enter your credentials now to claim reward.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Tấn công dồn dập Flood Attack (Gửi liên tiếp đợt 4)"
    },
    {
        "STT": 8,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huy162131@gmail.com",
        "IP_Nguon": "45.142.214.10",
        "Quoc_Gia": "Châu Âu (EU - Hà Lan)",
        "Thoi_Gian_Gui": "10:12:05 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Cập nhật bảng lương và thưởng nhân viên quý 3",
        "Noi_Dung_Than_Thu": "Phòng nhân sự gửi bảng lương điều chỉnh và tiền thưởng dự án quý 3. Mở tệp đính kèm bên dưới để xem chi tiết danh sách.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Bang_Luong_Q3.pdf.exe",
        "Kich_Ban_Thu_Nghiem": "Phát tán Mã độc thực thi nguy hiểm (.pdf.exe)"
    },
    {
        "STT": 9,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huy162131@gmail.com",
        "IP_Nguon": "14.225.208.15",
        "Quoc_Gia": "Việt Nam (Viettel)",
        "Thoi_Gian_Gui": "10:45:18 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Báo cáo tuần môn Học máy và Thị giác máy tính",
        "Noi_Dung_Than_Thu": "Gửi thầy báo cáo tiến độ tuần 4 của nhóm 3. Em đính kèm file slide trong mail ạ.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Bao_Cao_Tuan_4.pdf",
        "Kich_Ban_Thu_Nghiem": "Email nộp bài tập học phần hợp lệ (Ham)"
    },
    {
        "STT": 10,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "194.36.191.12",
        "Quoc_Gia": "Châu Âu (EU - Thụy Sĩ)",
        "Thoi_Gian_Gui": "11:20:30 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Cảnh báo bảo mật: Tài khoản bị truy cập trái phép",
        "Noi_Dung_Than_Thu": "Tài khoản ngân hàng của bạn đã bị tạm khóa do phát hiện đăng nhập bất thường. Vui lòng truy cập https://fake-ebanking.com/verify để xác minh danh tính ngay lập tức.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Không có",
        "Kich_Ban_Thu_Nghiem": "Giả mạo ngân hàng đánh cắp tài khoản (Phishing)"
    },
    {
        "STT": 11,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huy162131@gmail.com",
        "IP_Nguon": "123.24.180.99",
        "Quoc_Gia": "Việt Nam (FPT)",
        "Thoi_Gian_Gui": "14:10:00 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Biên nhận thanh toán tiền điện tháng 9",
        "Noi_Dung_Than_Thu": "Kính gửi quý khách, hóa đơn điện tử số HD-123456 đã được thanh toán thành công qua cổng ngân hàng. Chi tiết xem tại file hóa đơn.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Hoa_Don_Tien_Dien.pdf",
        "Kich_Ban_Thu_Nghiem": "Email giao dịch hóa đơn hợp lệ (Ham)"
    },
    {
        "STT": 12,
        # Nhóm 1: Siêu dữ liệu mạng
        "Nguoi_Gui": "huyk60049@gmail.com",
        "IP_Nguon": "185.190.140.33",
        "Quoc_Gia": "Châu Âu (EU - Séc)",
        "Thoi_Gian_Gui": "15:05:45 28/09/2026",
        # Nhóm 2: Nội dung văn bản
        "Tieu_De": "Tài liệu hướng dẫn cài đặt phần mềm kích hoạt",
        "Noi_Dung_Than_Thu": "Gửi bạn công cụ bẻ khóa bản quyền phần mềm đồ họa kèm theo trong thư để cài đặt sử dụng miễn phí.",
        # Nhóm 3: Tệp đính kèm
        "Tep_Dinh_Kem": "Crack_Tool_v2.bat",
        "Kich_Ban_Thu_Nghiem": "Phát tán mã độc tệp thực thi Script (.bat)"
    }
]

df = pd.DataFrame(data_input)

# Xuất file CSV với mã hóa UTF-8 with BOM (utf-8-sig) - đảm bảo mở bằng Excel không lỗi font
csv_path = Path("Tap_Tin_Dau_Vao_Chuan.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# Xuất file Excel (.xlsx) với định dạng bảng đẹp và chú thích rõ 3 thành phần
xlsx_path = Path("Tap_Tin_Dau_Vao_Chuan.xlsx")
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Dau_Vao_Email"

# Header dòng 1: Nhóm 3 thành phần lớn
ws.merge_cells("A1:A2")
ws["A1"] = "STT"

ws.merge_cells("B1:E1")
ws["B1"] = "NHÓM 1: SIÊU DỮ LIỆU MẠNG & THỜI GIAN"

ws.merge_cells("F1:G1")
ws["F1"] = "NHÓM 2: NỘI DUNG VĂN BẢN (TEXT)"

ws.merge_cells("H1:H2")
ws["H1"] = "NHÓM 3: TỆP ĐÍNH KÈM"

ws.merge_cells("I1:I2")
ws["I1"] = "KỊCH BẢN THỬ NGHIỆM"

# Header dòng 2: Các cột con
sub_headers = {
    "B2": "Người Gửi (From)",
    "C2": "IP Nguồn (Sender IP)",
    "D2": "Quốc Gia (GeoIP)",
    "E2": "Thời Gian Nhận",
    "F2": "Tiêu Đề (Subject)",
    "G2": "Nội Dung Thân Thư (Body)"
}
for pos, val in sub_headers.items():
    ws[pos] = val

# Style cho Header
fill_meta = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")  # Xanh dương nhạt
fill_text = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")  # Xanh lá nhạt
fill_file = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")  # Vàng nhạt
fill_scen = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")  # Xám nhạt

font_bold = Font(bold=True, size=11, color="000000")
align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Định dạng dòng 1
ws["A1"].font = font_bold
ws["A1"].alignment = align_center

ws["B1"].font = font_bold
ws["B1"].alignment = align_center
ws["B1"].fill = fill_meta

ws["F1"].font = font_bold
ws["F1"].alignment = align_center
ws["F1"].fill = fill_text

ws["H1"].font = font_bold
ws["H1"].alignment = align_center
ws["H1"].fill = fill_file

ws["I1"].font = font_bold
ws["I1"].alignment = align_center
ws["I1"].fill = fill_scen

# Định dạng dòng 2
for col_char, f_color in [("B", fill_meta), ("C", fill_meta), ("D", fill_meta), ("E", fill_meta),
                          ("F", fill_text), ("G", fill_text), ("H", fill_file), ("I", fill_scen)]:
    cell = ws[f"{col_char}2"]
    cell.font = Font(bold=True, size=10)
    cell.alignment = align_center
    cell.fill = f_color

# Đổ dữ liệu từ dòng 3
thin_border = Border(
    left=Side(style='thin', color='D0D0D0'),
    right=Side(style='thin', color='D0D0D0'),
    top=Side(style='thin', color='D0D0D0'),
    bottom=Side(style='thin', color='D0D0D0')
)

for row_idx, item in enumerate(data_input, start=3):
    ws.cell(row=row_idx, column=1, value=item["STT"]).alignment = Alignment(horizontal="center", vertical="top")
    ws.cell(row=row_idx, column=2, value=item["Nguoi_Gui"]).alignment = Alignment(vertical="top")
    ws.cell(row=row_idx, column=3, value=item["IP_Nguon"]).alignment = Alignment(horizontal="center", vertical="top")
    ws.cell(row=row_idx, column=4, value=item["Quoc_Gia"]).alignment = Alignment(vertical="top")
    ws.cell(row=row_idx, column=5, value=item["Thoi_Gian_Gui"]).alignment = Alignment(horizontal="center", vertical="top")
    ws.cell(row=row_idx, column=6, value=item["Tieu_De"]).alignment = Alignment(vertical="top", wrap_text=True)
    ws.cell(row=row_idx, column=7, value=item["Noi_Dung_Than_Thu"]).alignment = Alignment(vertical="top", wrap_text=True)
    ws.cell(row=row_idx, column=8, value=item["Tep_Dinh_Kem"]).alignment = Alignment(vertical="top")
    ws.cell(row=row_idx, column=9, value=item["Kich_Ban_Thu_Nghiem"]).alignment = Alignment(vertical="top", wrap_text=True)

    for col in range(1, 10):
        ws.cell(row=row_idx, column=col).border = thin_border

# Điều chỉnh độ rộng cột
col_widths = {
    "A": 6, "B": 24, "C": 16, "D": 24, "E": 20, "F": 35, "G": 45, "H": 22, "I": 35
}
for col, width in col_widths.items():
    ws.column_dimensions[col].width = width

wb.save(xlsx_path)
print("[+] Đã tạo thành công Tap_Tin_Dau_Vao_Chuan.xlsx và Tap_Tin_Dau_Vao_Chuan.csv!")
