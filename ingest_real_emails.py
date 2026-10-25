import os
import sys
import time
import imaplib
import email
from email.utils import parsedate_to_datetime
import datetime
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

RECEIVER_EMAIL = os.getenv("GMAIL_USER", "huymang196@gmail.com")
RECEIVER_PASS = os.getenv("GMAIL_APP_PASSWORD", "vrfa qiit bubg tpcc")

SENDER_1 = (os.getenv("SENDER_1_USER", "huy162131@gmail.com"), os.getenv("SENDER_1_PASS", "eptf oemi swrk pgvl"))
SENDER_2 = (os.getenv("SENDER_2_USER", "huyk60049@gmail.com"), os.getenv("SENDER_2_PASS", "rywj gatx kifw dciz"))
SENDERS = [SENDER_1, SENDER_2]

def get_email_datetime(msg) -> float:
    date_header = msg.get("Date")
    if date_header:
        try:
            dt = parsedate_to_datetime(date_header)
            return dt.timestamp()
        except Exception:
            pass
    return time.time()

def ingest_all_real_folders():
    print("="*70)
    print("🔍 ĐANG ĐỒNG BỘ CHÍNH XÁC TOÀN BỘ EMAIL TỪ GMAIL THẬT...")
    print("="*70)

    import json
    with open(config.DATABASE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

    analyzer = ThreatAnalyzer()
    
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(RECEIVER_EMAIL, RECEIVER_PASS)

    # Đọc cả INBOX và Spam folder với định dạng chuẩn IMAP
    folders = ['INBOX', '"[Gmail]/Spam"']
    processed_count = 0

    for folder in folders:
        try:
            status, _ = mail.select(folder)
            if status != "OK":
                continue

            status, messages = mail.search(None, 'ALL')
            if status == "OK" and messages[0]:
                mail_ids = messages[0].split()
                for m_id in mail_ids:
                    _, msg_data = mail.fetch(m_id, '(RFC822)')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            sender = decode_mime_words(msg.get("From", "Unknown"))
                            subject = decode_mime_words(msg.get("Subject", "No Subject"))
                            sender_ip = extract_sender_ip(msg)
                            body, attachments = extract_email_content(msg)
                            exact_timestamp = get_email_datetime(msg)

                            # Chỉ lấy các email do 2 tài khoản thật của bạn gửi
                            if any(s[0] in sender for s in SENDERS):
                                analysis = analyzer.analyze_email(
                                    sender=sender,
                                    subject=subject,
                                    body=body,
                                    attachments=attachments,
                                    sender_ip=sender_ip,
                                    timestamp=exact_timestamp
                                )
                                dt_display = datetime.datetime.fromtimestamp(exact_timestamp).strftime("%H:%M:%S %d/%m/%Y")
                                print(f"  [+] [{dt_display}] {sender[:18]} | '{subject[:30]}' -> Nhãn: {analysis['verdict']}")
                                processed_count += 1
        except Exception as e:
            print(f"[!] Lỗi đọc folder {folder}: {e}")

    mail.close()
    mail.logout()

    print("\n" + "="*70)
    print(f"[*] Đã quét và xử lý thành công {processed_count} email thật từ 2 tài khoản gửi của bạn!")
    excel_file = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
    print(f"✅ ĐÃ ĐỒNG BỘ XONG! File Excel thực tế 100%: {excel_file}")
    print("="*70)

if __name__ == "__main__":
    ingest_all_real_folders()
