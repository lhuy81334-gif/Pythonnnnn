import re
import json
import urllib.request
from typing import List, Optional, Dict

_GEO_CACHE: Dict[str, str] = {
    "127.0.0.1": "Mạng Nội Bộ (Localhost)",
    "localhost": "Mạng Nội Bộ (Localhost)",
}

def get_ip_location(ip_str: str) -> str:
    """
    Xác định Quốc gia / Vị trí địa lý từ địa chỉ IP người gửi (GeoIP Lookup).
    Có bộ đệm Cache và Fallback thông minh, không làm chậm hệ thống.
    """
    if not ip_str or "Không xác định" in ip_str:
        return "Máy chủ Google Relay (Hoa Kỳ)"

    ip_clean = ip_str.strip("[]() ")
    if ip_clean in _GEO_CACHE:
        return _GEO_CACHE[ip_clean]

    # Nhận diện nhanh các dải IP relay phổ biến của Google
    if ip_clean.startswith(("209.85.", "108.177.", "172.217.", "142.250.", "74.125.", "64.233.")):
        _GEO_CACHE[ip_clean] = "Hoa Kỳ (Google Relay)"
        return _GEO_CACHE[ip_clean]

    # Thử truy vấn GeoIP API online (timeout 1.0s)
    try:
        url = f"http://ip-api.com/json/{ip_clean}?fields=status,country,countryCode,city"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("status") == "success":
                country = data.get("country", "")
                city = data.get("city", "")
                loc_str = f"{country} ({city})" if city else country
                _GEO_CACHE[ip_clean] = loc_str
                return loc_str
    except Exception:
        pass

    # Fallback heuristic
    loc_fallback = "Châu Âu (Proxy EU)" if any(k in ip_clean for k in ["ydns", "eu", "185.", "194.", "45."]) else "Quốc tế (Proxy)"
    _GEO_CACHE[ip_clean] = loc_fallback
    return loc_fallback

def extract_sender_ip(msg) -> str:
    """
    Trích xuất chính xác địa chỉ IP của máy gửi từ các Header 'Received' của email.
    Chỉ lấy các IP hợp lệ nằm trong dấu ngoặc vuông [...] hoặc sau chữ 'from ... [IP]'
    """
    # 1. Kiểm tra header X-Originating-IP (nếu có)
    orig_ip = msg.get("X-Originating-IP", "")
    if orig_ip:
        ip_clean = orig_ip.strip("[]() ")
        return ip_clean

    # 2. Bóc tách từ các header Received
    received_headers = msg.get_all("Received", [])
    
    # Mẫu tìm kiếm IP nằm trong ngoặc vuông [x.x.x.x] chuẩn RFC
    bracket_ip_pattern = r'\[((?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))\]'
    
    candidate_ips = []
    for header in received_headers:
        matches = re.findall(bracket_ip_pattern, header)
        for ip in matches:
            # Loại trừ localhost
            if not ip.startswith("127."):
                candidate_ips.append(ip)

    if candidate_ips:
        # Lấy IP đầu tiên của người gửi gốc (hop đầu tiên)
        return candidate_ips[-1]
        
    return "Không xác định (Google Relay)"

