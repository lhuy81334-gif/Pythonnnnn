import sys
import socks
import socket
from pathlib import Path
from proxy_manager import load_proxies

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_single_proxy(proxy_info, timeout=5):
    """Kiem tra xem Proxy co ho tro ket noi den cong SMTP Gmail (465) khong."""
    try:
        s = socks.socksocket()
        s.set_proxy(
            proxy_type=socks.HTTP,
            addr=proxy_info["host"],
            port=proxy_info["port"],
            rdns=True,
            username=proxy_info["username"],
            password=proxy_info["password"]
        )
        s.settimeout(timeout)
        s.connect(('smtp.gmail.com', 465))
        s.close()
        return True, "HO TRO SMTP"
    except Exception as e:
        return False, str(e)

def scan_all_proxies():
    print("="*60)
    print("🔍 DANG QUET TOAN BO DANH SACH PROXY TRONG proxy.txt...")
    print("="*60)
    
    proxies = load_proxies()
    if not proxies:
        print("[!] File proxy.txt rong hoac khong tim thay.")
        return

    working_proxies = []
    
    for idx, p in enumerate(proxies, 1):
        proxy_str = f"{p['host']}:{p['port']}"
        print(f"[{idx}/{len(proxies)}] Dang kiem tra: {proxy_str} ... ", end="", flush=True)
        
        ok, msg = test_single_proxy(p, timeout=4)
        if ok:
            print("[OK] HO TRO TOT")
            working_proxies.append(p)
        else:
            print(f"[FAIL] {msg[:35]}")

    print("="*60)
    print(f"📊 KET QUA: Tim thay {len(working_proxies)} / {len(proxies)} proxy ho tro SMTP Gmail.")
    
    # Luu lai danh sach proxy song vao file working_proxies.txt
    if working_proxies:
        out_file = Path("working_proxies.txt")
        with open(out_file, "w", encoding="utf-8") as f:
            for p in working_proxies:
                f.write(f"{p['host']}:{p['port']}:{p['username']}:{p['password']}\n")
        print(f"[+] Da luu danh sach proxy hoat dong vao: {out_file.resolve()}")
    print("="*60)

if __name__ == "__main__":
    scan_all_proxies()
