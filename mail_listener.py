import imaplib
import email
import email.message
from email.message import Message
from email.header import decode_header
from email.utils import parsedate_to_datetime
import time
import sys
import re
from typing import List, Tuple

import config
from threat_analyzer import ThreatAnalyzer
from ip_extractor import extract_sender_ip
from export_excel import export_logs_to_excel

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def decode_mime_words(header_value: str) -> str:
    """Giai ma tieu de MIME co dau / ky tu dac biet."""
    if not header_value:
        return ""
    decoded_fragments = decode_header(header_value)
    result = []
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            if encoding:
                result.append(fragment.decode(encoding, errors="ignore"))
            else:
                result.append(fragment.decode("utf-8", errors="ignore"))
        else:
            result.append(str(fragment))
    return "".join(result)

def clean_html(raw_html: str) -> str:
    """Loai bo the HTML de trich xuat van ban thuan."""
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return " ".join(cleantext.split())

def extract_email_content(msg: Message) -> Tuple[str, List[str]]:
    """Boc tach phan van ban va danh sach ten tep dinh kem tu email."""
    body = ""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            filename = part.get_filename()
            
            if filename:
                decoded_fname = decode_mime_words(filename)
                attachments.append(decoded_fname)
                
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body += payload.decode(charset, errors="ignore")
            elif content_type == "text/html" and not body and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body += clean_html(payload.decode(charset, errors="ignore"))
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            decoded_text = payload.decode(charset, errors="ignore")
            if content_type == "text/html":
                body = clean_html(decoded_text)
            else:
                body = decoded_text
            
    return body.strip(), attachments

def get_email_timestamp(msg: Message) -> float:
    """Lay chinh xac thoi gian gui tu Date Header cua Google."""
    date_header = msg.get("Date")
    if date_header:
        try:
            return parsedate_to_datetime(date_header).timestamp()
        except Exception:
            pass
    return time.time()

def run_mail_listener():
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        print("[!] LOI: Vui long cau hinh GMAIL_USER va GMAIL_APP_PASSWORD trong file .env truoc khi chay!")
        sys.exit(1)

    print(f"[*] KHOI DONG SERVICE LANG NGHE GMAIL 24/7 CHO: {config.GMAIL_USER}")
    print("[*] Dang theo doi ca HOP THU DEN (INBOX) va THU RAC ([Gmail]/Spam)...")
    analyzer = ThreatAnalyzer()

    # Theo doi ca INBOX va Spam Folder de khong bo sot bat ky email nao
    monitored_folders = ['INBOX', '"[Gmail]/Spam"']

    while True:
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)

            has_new_mail = False

            for folder in monitored_folders:
                status, _ = mail.select(folder)
                if status != "OK":
                    continue

                # Tim kiem cac email CHUA DOC (UNSEEN)
                status, messages = mail.search(None, 'UNSEEN')
                if status == "OK" and messages[0]:
                    mail_ids = messages[0].split()
                    print(f"\n[+] Phat hien {len(mail_ids)} email moi trong [{folder}]. Tien hanh phan tich...")

                    for mail_id in mail_ids:
                        _, msg_data = mail.fetch(mail_id, '(RFC822)')
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                sender = decode_mime_words(msg.get("From", "Unknown"))
                                subject = decode_mime_words(msg.get("Subject", "No Subject"))
                                sender_ip = extract_sender_ip(msg)
                                body, attachments = extract_email_content(msg)
                                exact_time = get_email_timestamp(msg)

                                print(f"\n" + "="*60)
                                print(f"[*] DA KEO EMAIL MOI:")
                                print(f"- Thu muc   : {folder}")
                                print(f"- Nguoi gui : {sender}")
                                print(f"- IP Nguon  : {sender_ip}")
                                print(f"- Tieu de   : {subject}")
                                print(f"- Do dai    : {len(body)} ky tu")
                                print(f"- Dinh kem  : {attachments if attachments else 'Khong co'}")

                                # Dua vao bo phan tich AI & Hanh vi & IP & File
                                analysis = analyzer.analyze_email(
                                    sender=sender,
                                    subject=subject,
                                    body=body,
                                    attachments=attachments,
                                    sender_ip=sender_ip,
                                    timestamp=exact_time
                                )

                                print(f"[*] KET QUA DANH GIA:")
                                print(f"- Diem Rui Ro: {analysis['spam_score']*100:.1f}% -> {'[!] CANH BAO SPAM/LUA DAO' if analysis['is_spam'] else '[OK] HOP LE'}")
                                if analysis['indicators'].get('has_credentials'):
                                    print("  * [!] Phat hien bay chiem tai khoan User/Password!")
                                if analysis['indicators'].get('has_crypto'):
                                    print("  * [!] Phat hien tu khoa lua dao Tien ao USDT!")
                                if analysis['is_flood_attack']:
                                    print("  * [!] Canh bao tan cong don dap Flood Attack!")
                                print("="*60)

                                has_new_mail = True

            mail.close()
            mail.logout()

            # Neu co email moi -> Tu dong cap nhat lai file Excel
            if has_new_mail:
                export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")

        except Exception as e:
            print(f"[!] Loi ket noi IMAP: {e}")

        time.sleep(config.POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_mail_listener()
