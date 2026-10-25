import time
import json
from collections import deque
from typing import Dict, Any, List
import config
from model import SpamDetectionPipeline

class ThreatAnalyzer:
    """
    Bộ phân tích mối đe dọa toàn diện:
    - Phân tích nội dung AI (Random Forest)
    - Quét tệp đính kèm mã độc / đuôi kép nguy hiểm (.exe, .scr, .pdf.exe)
    - Phát hiện tấn công dồn dập (Flood / DoS / Sybil spam) qua cửa sổ thời gian
    """
    def __init__(self):
        self.model = SpamDetectionPipeline()
        self.model.load()
        self.recent_emails = deque()

    def _clean_old_history(self, current_time: float):
        while self.recent_emails and (current_time - self.recent_emails[0]["timestamp"] > config.FLOOD_WINDOW_SECONDS):
            self.recent_emails.popleft()

    def analyze_email(self, sender: str, subject: str, body: str, attachments: List[str] = None, sender_ip: str = "Không xác định", timestamp: float = None) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = time.time()
            
        if attachments is None:
            attachments = []
            
        # 1. Phân tích nội dung & File đính kèm qua Random Forest
        content_analysis = self.model.predict(subject, body, attachments)
        
        # 2. Phân tích hành vi & Tần suất
        self._clean_old_history(timestamp)
        
        recent_count = len(self.recent_emails)
        unique_senders = set(e["sender"] for e in self.recent_emails)
        unique_senders.add(sender)
        
        similar_content_count = 0
        current_text = f"{subject} {body}".strip().lower()
        for past_email in self.recent_emails:
            past_text = f"{past_email['subject']} {past_email['body']}".strip().lower()
            if past_text in current_text or current_text in past_text:
                similar_content_count += 1
                
        is_flood_attack = False
        flood_reasons = []
        
        if recent_count + 1 >= config.FLOOD_EMAIL_THRESHOLD:
            is_flood_attack = True
            flood_reasons.append(f"Nhận {recent_count + 1} email trong {config.FLOOD_WINDOW_SECONDS}s gần nhất.")
            
        if similar_content_count >= 2 and len(unique_senders) >= 2:
            is_flood_attack = True
            flood_reasons.append(f"Phát hiện {len(unique_senders)} tài khoản khác nhau gửi nội dung tương tự nhau.")
            
        email_record = {
            "timestamp": timestamp,
            "sender": sender,
            "sender_ip": sender_ip,
            "subject": subject,
            "body": body,
            "attachments": attachments,
            "is_spam": content_analysis["is_spam"],
            "spam_score": content_analysis["spam_score"],
            "verdict": content_analysis["verdict"],
            "is_flood_attack": is_flood_attack,
            "flood_reasons": flood_reasons,
            "indicators": content_analysis["indicators"]
        }
        self.recent_emails.append(email_record)
        self._append_to_log(email_record)
        
        return email_record


    def _append_to_log(self, record: Dict[str, Any]):
        logs = []
        if config.DATABASE_LOG_PATH.exists():
            try:
                with open(config.DATABASE_LOG_PATH, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except Exception:
                logs = []
                
        logs.append(record)
        if len(logs) > 500:
            logs = logs[-500:]
            
        with open(config.DATABASE_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
