import os
import sys
import time
import smtplib
import imaplib
import email
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

import config
from threat_analyzer import ThreatAnalyzer
from ip_extractor import extract_sender_ip
from mail_listener import extract_email_content, decode_mime_words
from export_excel import export_logs_to_excel

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

# 1. Khai báo 3 tài khoản THẬT 100%
RECEIVER_EMAIL = os.getenv("GMAIL_USER", "huymang196@gmail.com")
RECEIVER_PASS = os.getenv("GMAIL_APP_PASSWORD", "vrfa qiit bubg tpcc")

SENDER_1 = (os.getenv("SENDER_1_USER", "huy162131@gmail.com"), os.getenv("SENDER_1_PASS", "eptf oemi swrk pgvl"))
SENDER_2 = (os.getenv("SENDER_2_USER", "huyk60049@gmail.com"), os.getenv("SENDER_2_PASS", "rywj gatx kifw dciz"))

SENDERS = [SENDER_1, SENDER_2]

def send_real_email(sender_tuple, subject, body, attachment_name=None):
    sender_email, sender_pass = sender_tuple
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attachment_name:
        part = MIMEApplication(b"TEST DUMMY PAYLOAD", Name=attachment_name)
        part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=12)
        server.login(sender_email, sender_pass)
        server.send_message(msg)
        server.quit()
        print(f"  [+] GỬI THÀNH CÔNG từ [{sender_email}]: '{subject}'")
        return True
    except Exception as e:
        print(f"  [!] Lỗi gửi từ [{sender_email}]: {e}")
        return False

def generate_and_ingest_real_traffic():
    print("="*70)
    print("🚀 BẮT ĐẦU CHẠY THỰC CHIẾN BẰNG 3 TÀI KHOẢN GMAIL THẬT 100%")
    print(f"• Hòm thư Nhận Chính: {RECEIVER_EMAIL}")
    print(f"• Tài khoản Gửi 1   : {SENDER_1[0]}")
    print(f"• Tài khoản Gửi 2   : {SENDER_2[0]}")
    print("="*70)

    # 1. BƯỚC 1: HAI TÀI KHOẢN GỬI THAY PHIÊN NHAU BẮN CÁC KỊCH BẢN THẬT VÀO HÒM THƯ CHÍNH
    print("\n[BƯỚC 1] BẮT ĐẦU GỬI CÁC EMAIL THẬT QUA MÁY CHỦ GOOGLE:")
    
    # Kịch bản 1: SENDER 1 gửi thư lừa đảo Crypto / Thừa kế (ảnh bạn gửi)
    send_real_email(
        SENDER_1,
        subject="My precious legacy for you",
        body="Doctors told me cancer is incurable. I have decided to travel alone and bid farewell to this world in silence. I have no children. My only regret is not being able to spend this life with you. You were my first love and will live forever in my heart. I leave behind a precious legacy. I hope this friendship will bring us together again in the next life. Please keep this information safe. rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)"
    )
    time.sleep(1)

    # Kịch bản 2: SENDER 2 gửi thư spam quảng cáo nhà cái
    send_real_email(
        SENDER_2,
        subject="Tặng 100k trải nghiệm nhà cái uy tín hôm nay",
        body="Đăng ký tài khoản ngay hôm nay để nhận 100k vào tài khoản nạp rút siêu nhanh không cần điều kiện! Nhấp tại đây: http://nhacai88.vip"
    )
    time.sleep(1)

    # Kịch bản 3: SENDER 1 gửi email công việc/học tập sạch kèm file PDF
    send_real_email(
        SENDER_1,
        subject="Họp nhóm đồ án Python chiều nay",
        body="Chào bạn, chiều nay 14h nhóm mình họp online qua Google Meet để chốt slide báo cáo đồ án nhé.",
        attachment_name="Slide_Bao_Cao_Python.pdf"
    )
    time.sleep(1)

    # Kịch bản 4: TẤN CÔNG FLOOD / SYBIL: Cả SENDER 1 và SENDER 2 cùng bắn dồn dập 4 email nhận thưởng Crypto
    print("  [*] Hai tài khoản đang phối hợp bắn dồn dập (Flood / Sybil Attack)...")
    for i in range(1, 5):
        current_sender = SENDERS[i % 2]
        send_real_email(
            current_sender,
            subject=f"Ưu đãi đặc biệt nhận 500 USDT đợt {i}",
            body=f"Click ngay vào link https://claim-crypto.xyz để nhận 500 USDT miễn phí lần {i}!"
        )
        time.sleep(0.5)

    # Kịch bản 5: SENDER 2 gửi email chứa mã độc đuôi kép .pdf.exe
    send_real_email(
        SENDER_2,
        subject="Cập nhật bảng lương và quyết định khen thưởng tháng 9",
        body="Phòng Nhân sự gửi bảng tính lương và phụ cấp điều chỉnh. Vui lòng mở tệp đính kèm.",
        attachment_name="Bang_Luong_Dieu_Chinh.pdf.exe"
    )

    print("\n" + "="*70)
    print("[BƯỚC 2] CHỜ 3 GIÂY ĐỂ MÁY CHỦ GOOGLE ĐỒNG BỘ...")
    time.sleep(3)

    # 2. BƯỚC 2: HÒM THƯ CHÍNH (RECEIVER) KÉO TOÀN BỘ EMAIL THẬT VỀ & CHẠY RANDOM FOREST
    print("\n[BƯỚC 3] HÒM THƯ CHÍNH HUYMANG196@GMAIL.COM KÉO EMAIL VỀ & PHÂN TÍCH:")
    analyzer = ThreatAnalyzer()
    
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(RECEIVER_EMAIL, RECEIVER_PASS)
    mail.select("inbox")
    
    # Lấy các email mới nhất
    status, messages = mail.search(None, 'ALL')
    if status == "OK" and messages[0]:
        mail_ids = messages[0].split()
        # Lấy tối đa 10 email gần nhất
        recent_ids = mail_ids[-10:]
        
        for m_id in recent_ids:
            _, msg_data = mail.fetch(m_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = decode_mime_words(msg.get("From", "Unknown"))
                    subject = decode_mime_words(msg.get("Subject", "No Subject"))
                    sender_ip = extract_sender_ip(msg)
                    body, attachments = extract_email_content(msg)
                    
                    # Chỉ phân tích các email gửi từ 2 tài khoản thật hoặc liên quan
                    if any(s[0] in sender for s in SENDERS) or "vbee" not in sender.lower():
                        analysis = analyzer.analyze_email(
                            sender=sender,
                            subject=subject,
                            body=body,
                            attachments=attachments,
                            sender_ip=sender_ip
                        )
                        print(f"  • Đã phân tích: [{sender}] | IP: {sender_ip} | Tiêu đề: {subject[:30]}... -> Nhãn: {analysis['verdict']}")

    mail.close()
    mail.logout()

    # 3. BƯỚC 3: XUẤT RA FILE EXCEL
    print("\n" + "="*70)
    print("[BƯỚC 4] XUẤT BẢNG SỐ LIỆU THẬT 100% RA EXCEL:")
    excel_file = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
    print(f"✅ ĐÃ HOÀN THÀNH TOÀN BỘ! File Excel thực tế 100%: {excel_file}")
    print("="*70)

if __name__ == "__main__":
    generate_and_ingest_real_traffic()
