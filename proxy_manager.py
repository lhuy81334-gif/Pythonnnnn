import os
import random
import socket
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import socks

BASE_DIR = Path(__file__).resolve().parent

def load_proxies(filepath: Path = None) -> List[Dict[str, Any]]:
    if filepath is None:
        filepath = BASE_DIR / "proxy.txt"
        
    proxies = []
    if not filepath.exists():
        return proxies
        
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Cho phép ghi chú quốc gia sau dấu # (ví dụ: host:port:user:pass # Châu Âu)
            country = "Châu Âu (EU)"
            if "#" in line:
                parts_comment = line.split("#", 1)
                line = parts_comment[0].strip()
                country = parts_comment[1].strip()
            
            parts = line.split(":")
            if len(parts) == 4:
                proxies.append({
                    "host": parts[0],
                    "port": int(parts[1]),
                    "username": parts[2],
                    "password": parts[3],
                    "country": country
                })
            elif len(parts) == 2:
                proxies.append({
                    "host": parts[0],
                    "port": int(parts[1]),
                    "username": None,
                    "password": None,
                    "country": country
                })
    return proxies

def load_senders(filepath: Path = None) -> List[Tuple[str, str]]:
    if filepath is None:
        filepath = BASE_DIR / "senders.txt"
        
    senders = []
    if not filepath.exists():
        return senders
        
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                email, pwd = line.split("|", 1)
                senders.append((email.strip(), pwd.strip()))
            elif ":" in line:
                email, pwd = line.split(":", 1)
                senders.append((email.strip(), pwd.strip()))
    return senders

def get_proxied_socket(proxy_info: Optional[Dict[str, Any]] = None, timeout: int = 10) -> socket.socket:
    """Tạo một socket đã được định tuyến qua Proxy."""
    if proxy_info:
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
        return s
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        return s
