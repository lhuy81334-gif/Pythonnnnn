import time
import sys
from threat_analyzer import ThreatAnalyzer
from export_excel import export_logs_to_excel

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_full_suite():
    print("="*70)
    print("🚀 TIẾN HÀNH THU THẬP & TRÍCH XUẤT ĐẶC TRƯNG HỌC MÁY TOÀN BỘ CÁC KỊCH BẢN")
    print("="*70)
    
    analyzer = ThreatAnalyzer()
    
    # 1. Kịch bản 1: Lừa đảo Crypto / Thừa kế (Ảnh bạn gửi)
    print("[1/6] Trích xuất Kịch bản 1: Lừa đảo Crypto Phishing...")
    analyzer.analyze_email(
        sender="scam_legacy_99@crypto-fraud.xyz",
        subject="My precious legacy for you",
        body="Doctors told me cancer is incurable. I have decided to travel alone and bid farewell. rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)",
        sender_ip="116.98.238.72"
    )

    # 2. Kịch bản 2: Spam quảng cáo cá cược / khuyến mãi
    print("[2/6] Trích xuất Kịch bản 2: Spam Quảng cáo Khuyến mãi...")
    analyzer.analyze_email(
        sender="promo@nhacai-uytin.cc",
        subject="Tặng 100k trải nghiệm nhà cái uy tín hôm nay",
        body="Đăng ký tài khoản ngay hôm nay để nhận 100k vào tài khoản nạp rút siêu nhanh không cần điều kiện! Nhấp tại đây: http://nhacai88.vip",
        sender_ip="103.145.2.18"
    )

    # 3. Kịch bản 3: Email học tập / công việc hợp lệ (Ham)
    print("[3/6] Trích xuất Kịch bản 3: Email Học tập / Công việc Hợp lệ...")
    analyzer.analyze_email(
        sender="giangvien@hust.edu.vn",
        subject="Thông báo lịch thi kết thúc học phần môn Xử lý ảnh",
        body="Phòng Đào tạo gửi danh sách phòng thi và quy chế thi học kỳ. Sinh viên kiểm tra kỹ thông tin đính kèm.",
        attachments=["Lich_Thi_Hoc_Ky.pdf"],
        sender_ip="203.162.0.11"
    )

    # 4. Kịch bản 4: Tấn công dồn dập Flood / Sybil Attack (3 email dồn dập từ nhiều tài khoản)
    print("[4/6] Trích xuất Kịch bản 4: Tấn công dồn dập Flood / Sybil...")
    for i in range(1, 4):
        analyzer.analyze_email(
            sender=f"clone_bot_{i}@gmail.com",
            subject=f"Nhận 500 USDT miễn phí đợt {i}",
            body="Click ngay vào link https://claim-crypto.cc để nhận 500 USDT ngay lập tức!",
            sender_ip=f"45.122.25.{i+10}"
        )
        time.sleep(0.1)

    # 5. Kịch bản 5: Phát tán file mã độc đuôi kép (.pdf.exe)
    print("[5/6] Trích xuất Kịch bản 5: Email chứa mã độc đuôi kép...")
    analyzer.analyze_email(
        sender="fake_hr@company-secure.cc",
        subject="Cập nhật bảng lương và quyết định khen thưởng tháng 9",
        body="Phòng Nhân sự gửi bảng tính lương và phụ cấp điều chỉnh. Vui lòng mở tệp đính kèm.",
        attachments=["Bang_Luong_Dieu_Chinh.pdf.exe"],
        sender_ip="185.220.101.5"
    )

    # 6. Kịch bản 6: Email trao đổi đồ án Python của nhóm (Ham sạch 100%)
    print("[6/6] Trích xuất Kịch bản 6: Email trao đổi đồ án sạch...")
    analyzer.analyze_email(
        sender="nhomtruong@gmail.com",
        subject="Họp nhóm đồ án Python chiều nay",
        body="Chào bạn, chiều nay 14h nhóm mình họp online qua Google Meet để chốt slide báo cáo đồ án nhé.",
        attachments=["Slide_Bao_Cao_Python.pptx"],
        sender_ip="123.24.47.164"
    )

    print("\n" + "="*70)
    print("[+] ĐÃ TRÍCH XUẤT XONG! Tiến hành xuất Bảng Ma Trận Đặc Trưng ra Excel...")
    excel_path = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
    print(f"[+] File Excel Ma Trận Học Máy đã sẵn sàng tại: {excel_path}")
    print("="*70)

if __name__ == "__main__":
    run_full_suite()
