import os
import sys
import smtplib
import ssl
import time
import random
from typing import Optional, Dict, Any, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

import config
from proxy_manager import load_proxies, load_senders, get_proxied_socket

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

RECEIVER_USER = os.getenv("GMAIL_USER", "huymang196@gmail.com")
PROXIES = load_proxies(config.BASE_DIR / "working_proxies.txt") or load_proxies()
SENDERS = load_senders()

if not SENDERS:
    fallback_user = os.getenv("SENDER_GMAIL_USER", "huy162131@gmail.com")
    fallback_pass = os.getenv("SENDER_GMAIL_APP_PASSWORD", "eptf oemi swrk pgvl")
    SENDERS.append((fallback_user, fallback_pass))

def send_email_via_proxy(
    sender_tuple: Tuple[str, str],
    subject: str,
    body: str,
    attachment_filename: Optional[str] = None,
    proxy_info: Optional[Dict[str, Any]] = None,
    fake_content: bytes = b"DUMMY TEST ATTACHMENT DATA"
) -> bool:
    """
    Gửi email từ 1 tài khoản cụ thể QUA PROXY ĐÍCH THỰC (SSL Port 465) đến tài khoản nhận
    """
    sender_email, sender_password = sender_tuple
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = RECEIVER_USER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attachment_filename:
        part = MIMEApplication(fake_content, Name=attachment_filename)
        part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
        msg.attach(part)

    country_info = proxy_info.get('country', 'Châu Âu (EU)') if proxy_info else 'Trực tiếp (Việt Nam)'
    proxy_desc = f"{proxy_info['host']}:{proxy_info['port']} ({country_info})" if proxy_info else "Direct (Việt Nam)"
    print(f"[*] Đang gửi từ [{sender_email}] qua Proxy [{proxy_desc}]...")

    # 1. Gửi qua Proxy SSL chuẩn
    if proxy_info:
        try:
            # Tạo socket định tuyến qua Proxy
            sock = get_proxied_socket(proxy_info, timeout=15)
            sock.connect(('smtp.gmail.com', 465))
            
            # Bọc SSL trên đường truyền Proxy
            ssl_context = ssl.create_default_context()
            secure_sock = ssl_context.wrap_socket(sock, server_hostname='smtp.gmail.com')
            
            server = smtplib.SMTP_SSL()
            server.sock = secure_sock
            server.file = secure_sock.makefile('rb')
            
            # Đọc banner chào mừng từ Google SMTP và thực hiện ESMTP handshake
            server.getreply()
            server.ehlo()
            
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"[+] [SUCCESS VIA PROXY] ĐÃ GỬI QUA PROXY THÀNH CÔNG: '{subject}' -> {RECEIVER_USER}")
            return True
        except Exception as e:
            print(f"[-] Gửi qua Proxy {proxy_desc} gặp lỗi: {e}")
            print("[*] Chuyển sang đường truyền trực tiếp...")

    # 2. Gửi trực tiếp nếu không dùng proxy hoặc proxy lỗi
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=12)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"[+] [DIRECT SUCCESS] ĐÃ GỬI THÀNH CÔNG: '{subject}' -> {RECEIVER_USER}")
        return True
    except Exception as e2:
        print(f"[!] Lỗi gửi: {e2}")
        return False

def get_random_sender_and_proxy():
    sender = random.choice(SENDERS)
    proxy = random.choice(PROXIES) if PROXIES else None
    return sender, proxy

def menu():
    print("="*60)
    print("🚀 TOOL TẤN CÔNG & KIỂM THỬ ĐỒ ÁN (MULTI-ACCOUNT & PROXY ROTATION)")
    print(f"• Hòm thư Nhận (Victim): {RECEIVER_USER}")
    print(f"• Số lượng tài khoản gửi (Senders): {len(SENDERS)} tài khoản ({', '.join([s[0] for s in SENDERS])})")
    print(f"• Số lượng Proxy nạp được: {len(PROXIES)} proxies từ working_proxies.txt")
    print("="*60)
    print("1. [Case 1] Gửi Email Lừa Đảo Crypto / Thừa kế (Ảnh bạn gửi)")
    print("2. [Case 2] Gửi Email Spam Quảng Cáo (Nhà cái, Khuyến mãi)")
    print("3. [Case 3] Gửi Email Học tập / Công việc Hợp lệ (Ham)")
    print("4. [Case 4] TẤN CÔNG SYBIL / FLOOD (Xoay tua nhiều tài khoản + Proxy bắn dồn dập)")
    print("5. [Case 5] Gửi Email Chứa File Độc Hại (.pdf.exe / .scr)")
    print("6. Tự nhập nội dung tùy biến")
    print("="*60)

    choice = input("Nhập lựa chọn của bạn (1-6): ").strip()

    if choice == "1":
        sender, proxy = get_random_sender_and_proxy()
        subject = "My precious legacy for you"
        body = (
            "Doctors told me cancer is incurable. I have decided to travel alone "
            "and bid farewell to this world in silence. I have no children. "
            "My only regret is not being able to spend this life with you. "
            "You were my first love and will live forever in my heart. "
            "I leave behind a precious legacy. I hope this friendship will bring "
            "us together again in the next life. Please keep this information safe. "
            "rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)"
        )
        send_email_via_proxy(sender, subject, body, proxy_info=proxy)

    elif choice == "2":
        sender, proxy = get_random_sender_and_proxy()
        subject = "Tặng 100k trải nghiệm nhà cái uy tín hôm nay"
        body = "Đăng ký tài khoản ngay hôm nay để nhận 100k vào tài khoản nạp rút siêu nhanh không cần điều kiện!"
        send_email_via_proxy(sender, subject, body, proxy_info=proxy)

    elif choice == "3":
        sender, proxy = get_random_sender_and_proxy()
        subject = "Họp nhóm đồ án Python chiều nay"
        body = "Chào bạn, chiều nay 14h nhóm mình họp online qua Google Meet để chốt slide báo cáo đồ án nhé."
        send_email_via_proxy(sender, subject, body, attachment_filename="Slide_Bao_Cao.pdf", proxy_info=proxy)

    elif choice == "4":
        print("[*] Đang kích hoạt chế độ TẤN CÔNG SYBIL / FLOOD ATTACK (Xoay tua tài khoản & Proxy)...")
        num_emails = 6
        for i in range(1, num_emails + 1):
            sender = SENDERS[(i - 1) % len(SENDERS)]
            proxy = PROXIES[(i - 1) % len(PROXIES)] if PROXIES else None
            
            subject = f"Ưu đãi nhận 500 USDT đợt {i}"
            body = f"Click ngay vào link https://bonus-crypto.xyz để nhận 500 USDT miễn phí lần {i}!"
            send_email_via_proxy(sender, subject, body, proxy_info=proxy)
            time.sleep(1)

    elif choice == "5":
        sender, proxy = get_random_sender_and_proxy()
        subject = "Cập nhật bảng lương và quyết định khen thưởng tháng 9"
        body = "Phòng Nhân sự gửi bảng tính lương và điều chỉnh phụ cấp. Kính mời các bạn tải file đính kèm để kiểm tra."
        send_email_via_proxy(sender, subject, body, attachment_filename="Bang_Luong_Dieu_Chinh.pdf.exe", proxy_info=proxy)

    elif choice == "6":
        sender, proxy = get_random_sender_and_proxy()
        subject = input("Nhập Tiêu đề: ")
        body = input("Nhập Nội dung: ")
        att = input("Nhập tên file đính kèm (bỏ trống nếu không): ").strip()
        send_email_via_proxy(sender, subject, body, attachment_filename=att if att else None, proxy_info=proxy)
    else:
        print("[!] Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    menu()
