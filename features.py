import re
from typing import Dict, Any, List

# Danh mục từ khóa nhận diện các dạng Spam / Phishing phổ biến
CRYPTO_KEYWORDS = {"usdt", "btc", "bitcoin", "eth", "ethereum", "wallet", "crypto", "binance", "metamask", "balance"}
EMOTIONAL_BAIT_WORDS = {"cancer", "legacy", "farewell", "inheritance", "incurable", "charity", "dying", "first love"}
URGENCY_KEYWORDS = {"urgent", "immediate", "account suspended", "verify now", "action required", "winner", "prize"}

# Danh sách phần mở rộng tệp nguy hiểm thường dùng để phát tán mã độc (Malware / Ransomware)
DANGEROUS_EXTENSIONS = {
    ".exe", ".scr", ".bat", ".cmd", ".vbs", ".js", ".ps1", 
    ".msi", ".jar", ".pif", ".hta", ".iso", ".lnk", ".wsf"
}

def extract_urls(text: str) -> List[str]:
    """Trích xuất danh sách URL / Domain từ văn bản."""
    url_pattern = r'(?:https?://|www\.)[^\s/$.?#].[^\s]*|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
    candidates = re.findall(url_pattern, text, re.IGNORECASE)
    valid_urls = []
    for c in candidates:
        if '.' in c and not c.endswith('.'):
            valid_urls.append(c.strip('.,;()[]{}<>'))
    return valid_urls

def inspect_attachments(attachments: List[str]) -> Dict[str, Any]:
    """
    Quét danh sách tên file đính kèm để phát hiện tệp thực thi độc hại
    hoặc kỹ thuật ẩn đuôi kép (Double Extension, ví dụ: 'document.pdf.exe')
    """
    if not attachments:
        return {
            "has_attachment": 0,
            "attachment_count": 0,
            "has_dangerous_file": 0,
            "has_double_extension": 0,
            "dangerous_files": []
        }
        
    dangerous_found = []
    has_double_ext = 0
    
    for filename in attachments:
        fname_lower = filename.lower()
        # 1. Kiểm tra đuôi file nguy hiểm
        for ext in DANGEROUS_EXTENSIONS:
            if fname_lower.endswith(ext):
                dangerous_found.append(filename)
                break
                
        # 2. Kiểm tra kỹ thuật lừa đuôi kép (Double Extension: .pdf.exe, .docx.scr)
        parts = fname_lower.split('.')
        if len(parts) > 2:
            last_ext = f".{parts[-1]}"
            second_last = f".{parts[-2]}"
            if last_ext in DANGEROUS_EXTENSIONS and second_last in {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.png', '.jpg'}:
                has_double_ext = 1

    return {
        "has_attachment": 1,
        "attachment_count": len(attachments),
        "has_dangerous_file": int(len(dangerous_found) > 0),
        "has_double_extension": has_double_ext,
        "dangerous_files": dangerous_found
    }

def extract_handcrafted_features(subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
    """
    Trích xuất toàn diện các đặc trưng:
    - Nội dung văn bản
    - Dấu hiệu lừa đảo / Phishing
    - Phân tích file đính kèm độc hại (Malware Indicators)
    """
    if attachments is None:
        attachments = []
        
    full_text = f"{subject} {body}".strip()
    text_lower = full_text.lower()
    
    # 1. Bẫy thông tin tài khoản User / Password
    has_credentials = int(bool(re.search(
        r'(username|user|tk|account|login|id)\s*[:=]\s*\S+.*(password|pass|mk|pwd)\s*[:=]\s*\S+',
        full_text, re.IGNORECASE | re.DOTALL
    )))
    
    # 2. Từ khóa Crypto
    crypto_count = sum(1 for word in CRYPTO_KEYWORDS if word in text_lower)
    has_crypto = int(crypto_count > 0)
    
    # 3. Số tiền lớn
    has_huge_money = int(bool(re.search(
        r'\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*(?:usdt|\$|usd|vnd|eur|btc)', 
        full_text, re.IGNORECASE
    )))
    
    # 4. Thao túng tâm lý
    bait_score = sum(1 for word in EMOTIONAL_BAIT_WORDS if word in text_lower)
    
    # 5. Mức độ khẩn cấp
    urgency_score = sum(1 for word in URGENCY_KEYWORDS if word in text_lower)
    
    # 6. URL & Domain
    urls = extract_urls(full_text)
    url_count = len(urls)
    
    # 7. Thống kê ký tự
    char_count = len(full_text) if len(full_text) > 0 else 1
    uppercase_count = sum(1 for c in full_text if c.isupper())
    uppercase_ratio = uppercase_count / char_count
    exclamation_count = full_text.count('!')
    dollar_count = full_text.count('$')
    
    # 8. Phân tích file đính kèm
    attach_info = inspect_attachments(attachments)
    
    return {
        "has_credentials": has_credentials,
        "has_crypto": has_crypto,
        "crypto_count": crypto_count,
        "has_huge_money": has_huge_money,
        "bait_score": bait_score,
        "urgency_score": urgency_score,
        "url_count": url_count,
        "uppercase_ratio": round(uppercase_ratio, 4),
        "exclamation_count": exclamation_count,
        "dollar_count": dollar_count,
        "has_attachment": attach_info["has_attachment"],
        "attachment_count": attach_info["attachment_count"],
        "has_dangerous_file": attach_info["has_dangerous_file"],
        "has_double_extension": attach_info["has_double_extension"],
        "dangerous_files": attach_info["dangerous_files"],
        "extracted_urls": urls
    }
