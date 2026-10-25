import sys
import time
import socket
import ssl
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Tuple, Optional
import socks

import config
from proxy_manager import load_proxies, BASE_DIR

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_single_proxy(proxy: Dict[str, Any], timeout: float = 6.0) -> Tuple[bool, float, str, Dict[str, Any]]:
    """
    Kiểm tra 1 proxy bằng cách thử thiết lập socket SSL tới smtp.gmail.com:465.
    Trả về: (is_live, latency_ms, error_message, proxy_info)
    """
    host = proxy["host"]
    port = proxy["port"]
    user = proxy.get("username")
    pwd = proxy.get("password")
    country = proxy.get("country", "Châu Âu (EU)")

    start_time = time.time()
    try:
        s = socks.socksocket()
        s.set_proxy(
            proxy_type=socks.HTTP,
            addr=host,
            port=port,
            rdns=True,
            username=user,
            password=pwd
        )
        s.settimeout(timeout)
        s.connect(('smtp.gmail.com', 465))

        # Thử bọc SSL để xác nhận proxy truyền tải dữ liệu mã hóa chuẩn
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ssock = ctx.wrap_socket(s, server_hostname='smtp.gmail.com')
        ssock.close()

        latency = (time.time() - start_time) * 1000.0
        return True, latency, "OK", proxy
    except Exception as e:
        latency = (time.time() - start_time) * 1000.0
        err = str(e)
        if "timed out" in err.lower():
            err = "Timeout (>6s)"
        elif "connection refused" in err.lower():
            err = "Connection Refused"
        return False, latency, err, proxy

def check_all_proxies(
    input_file: Path = None,
    output_file: Path = None,
    max_workers: int = 50,
    timeout: float = 4.0
) -> list:
    """
    Kiểm tra toàn bộ proxy đa luồng (mặc định 50 workers) và lưu danh sách proxy sống vào working_proxies.txt
    """
    if input_file is None:
        input_file = BASE_DIR / "proxy.txt"
    if output_file is None:
        output_file = BASE_DIR / "working_proxies.txt"

    proxies = load_proxies(input_file)
    if not proxies:
        print(f"[!] Không tìm thấy proxy trong file: {input_file}")
        return []

    # Giới hạn số luồng tối đa không vượt quá số proxy nếu ít hơn
    actual_workers = min(max_workers, max(len(proxies), 1))

    print(f"============================================================")
    print(f"[*] BẮT ĐẦU KIỂM TRA {len(proxies)} PROXY VỚI BỘ LỌC TỐC ĐỘ CAO ({actual_workers} THREADS)")
    print(f"[*] Đích kiểm tra: Google SMTP SSL (smtp.gmail.com:465) | Timeout: {timeout}s")
    print(f"============================================================\n")

    working_list = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {
            executor.submit(test_single_proxy, p, timeout): p for p in proxies
        }

        for future in as_completed(future_to_proxy):
            is_live, latency, err, proxy = future.result()
            host_port = f"{proxy['host']}:{proxy['port']}"
            country = proxy.get('country', 'Châu Âu (EU)')

            if is_live:
                print(f"  [+] LIVE ({latency:.0f}ms) -> {host_port:<28} | {country}")
                working_list.append((proxy, latency))
            else:
                print(f"  [-] DEAD ({latency:.0f}ms) -> {host_port:<28} | Lỗi: {err}")

    # Sắp xếp proxy sống theo độ trễ tăng dần (ưu tiên proxy nhanh nhất)
    working_list.sort(key=lambda x: x[1])

    # Ghi vào file output
    lines_to_write = [
        "# Danh sách Proxy LIVE đã qua kiểm tra 10 luồng tự động (Sắp xếp theo tốc độ)",
        f"# Cập nhật lúc: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    for p, lat in working_list:
        if p.get("username") and p.get("password"):
            line = f"{p['host']}:{p['port']}:{p['username']}:{p['password']} # {p.get('country', 'Châu Âu (EU)')} - {lat:.0f}ms"
        else:
            line = f"{p['host']}:{p['port']} # {p.get('country', 'Châu Âu (EU)')} - {lat:.0f}ms"
        lines_to_write.append(line)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_to_write) + "\n")

    print(f"\n============================================================")
    print(f"[*] HOÀN TẤT: {len(working_list)}/{len(proxies)} PROXY ĐANG HOẠT ĐỘNG TỐT!")
    print(f"[*] Đã lưu danh sách proxy sống vào: {output_file.name}")
    print(f"============================================================")

    return [p for p, _ in working_list]

if __name__ == "__main__":
    check_all_proxies(max_workers=50, timeout=4.0)
