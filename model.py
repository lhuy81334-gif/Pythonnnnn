import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import config
from features import extract_handcrafted_features

# Tập dữ liệu mẫu cân bằng và đầy đủ các trường hợp thực tế
SEED_DATA = [
    # --- HAM (Thư công việc, học tập, giao dịch hợp lệ) ---
    ("Họp dự án đồ án tốt nghiệp lúc 9h sáng mai", "Chào bạn, sáng mai chúng ta họp nhóm để phân chia nhiệm vụ module tiếp theo nhé.", [], 0),
    ("Báo cáo tuần môn Học máy và Thị giác máy tính", "Gửi thầy báo cáo tiến độ tuần 4 của nhóm 3. Em đính kèm file slide trong mail ạ.", ["slide_bao_cao.pdf"], 0),
    ("Biên nhận thanh toán tiền điện tháng 9", "Kính gửi quý khách, hóa đơn điện tử số 123456 đã được thanh toán thành công qua ngân hàng.", ["hoa_don_dien_tu.pdf"], 0),
    ("Lời mời tham dự hội thảo công nghệ AI", "Trân trọng mời bạn tham dự buổi chia sẻ về Generative AI vào chiều thứ 7 tuần này.", [], 0),
    ("Xác nhận đặt lịch hẹn phỏng vấn thực tập sinh", "Cảm ơn bạn đã ứng tuyển vị trí Python Developer. Chúng tôi xin hẹn bạn phỏng vấn trực tuyến.", ["job_description.docx"], 0),
    ("Weekly team sprint update", "Here is the summary of tasks completed in sprint 12. Please review the PRs before Friday.", [], 0),
    ("Thông báo lịch thi kết thúc học phần học kỳ 1", "Phòng đào tạo thông báo danh sách phòng thi và thời gian thi chính thức cho sinh viên.", ["lich_thi.xlsx"], 0),
    ("Tài liệu bài giảng môn Xử lý ngôn ngữ tự nhiên", "Thầy gửi cả lớp tài liệu tham khảo và bài tập về nhà tuần này nhé.", ["bai_giang_nlp.pdf"], 0),
    ("Họp nhóm đồ án Python chiều nay", "Chào bạn, chiều nay 14h nhóm mình họp online qua Google Meet để chốt slide báo cáo đồ án nhé.", ["Slide_Thuyet_Trinh.pdf"], 0),
    ("Thông báo kết quả xét duyệt học bổng kỳ vừa qua", "Chúc mừng sinh viên đã đạt kết quả xuất sắc và nhận học bổng khuyến khích học tập.", [], 0),
    
    # --- SPAM / PHISHING (Lừa đảo & Rác thông thường) ---
    ("Tặng 100k trải nghiệm nhà cái uy tín", "Đăng ký ngay nhận 100k miễn phí vào tài khoản cá cược nạp rút siêu nhanh click tại đây.", [], 1),
    ("Khuyến mãi giảm giá 70% duy nhất hôm nay", "Cơ hội cuối cùng để săn deal cực sốc. Bấm vào liên kết mua ngay kẻo hết quà tặng!", [], 1),
    ("Cảnh báo bảo mật tài khoản ngân hàng", "Tài khoản của bạn đã bị khóa tạm thời. Vui lòng đăng nhập vào link https://fake-bank.cc để mở lại.", [], 1),
    ("My precious legacy for you", "Doctors told me cancer is incurable. I have decided to travel alone and bid farewell. rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)", [], 1),
    ("Urgent: Inheritance donation fund from London", "I have 5,000,000 USD funds from late husband. Need your wallet address to transfer crypto USDT urgently.", [], 1),
    ("Claim your 500 USDT Airdrop Reward!", "Congratulations! Your email won the lucky draw. Visit metamask-claim.xyz and enter your credentials now.", [], 1),
    ("Ưu đãi đặc biệt đợt nhận thưởng lớn", "Click ngay vào link https://bonus-crypto.xyz để nhận 1000 USDT miễn phí lần này!", [], 1),
    
    # --- MALWARE ATTACHMENT (Mã độc đính kèm) ---
    ("Hóa đơn thanh toán quá hạn - Cần kiểm tra gấp", "Kính gửi quý khách hàng, vui lòng xem chi tiết biên lai quá hạn trong file đính kèm.", ["Hoa_Don_Thang_9.pdf.exe"], 1),
    ("Cập nhật bảng lương và thưởng nhân viên", "Phòng nhân sự gửi bảng lương điều chỉnh. Mở tệp đính kèm để xem chi tiết.", ["Bang_Luong.scr"], 1),
    ("Tài liệu hướng dẫn cài đặt phần mềm crack", "Tải công cụ bẻ khóa bản quyền phần mềm kèm theo trong thư để kích hoạt.", ["Patch_Installer.bat"], 1),
    ("Urgent Invoice Overdue Notification", "Please find attached the official overdue invoice statement.", ["Invoice_Overdue.iso"], 1)
]

class SpamDetectionPipeline:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.clf = RandomForestClassifier(n_estimators=150, random_state=42)
        self.is_trained = False

    def _prepare_feature_vector(self, subjects, bodies, attachments_list=None, fit_vectorizer=False):
        if attachments_list is None:
            attachments_list = [[] for _ in subjects]
            
        full_texts = [f"{s} {b}" for s, b in zip(subjects, bodies)]
        
        if fit_vectorizer:
            tfidf_matrix = self.vectorizer.fit_transform(full_texts).toarray()
        else:
            tfidf_matrix = self.vectorizer.transform(full_texts).toarray()
            
        handcrafted_list = []
        for s, b, atts in zip(subjects, bodies, attachments_list):
            feats = extract_handcrafted_features(s, b, atts)
            handcrafted_list.append([
                feats["has_credentials"],
                feats["has_crypto"],
                feats["crypto_count"],
                feats["has_huge_money"],
                feats["bait_score"],
                feats["urgency_score"],
                feats["url_count"],
                feats["uppercase_ratio"],
                feats["exclamation_count"],
                feats["dollar_count"],
                feats["has_attachment"],
                feats["has_dangerous_file"],
                feats["has_double_extension"]
            ])
            
        handcrafted_matrix = np.array(handcrafted_list)
        combined_matrix = np.hstack([tfidf_matrix, handcrafted_matrix])
        return combined_matrix

    def train(self, data=None):
        if data is None:
            data = SEED_DATA
        
        subjects = [item[0] for item in data]
        bodies = [item[1] for item in data]
        attachments_list = [item[2] for item in data]
        labels = [item[3] for item in data]
        
        X = self._prepare_feature_vector(subjects, bodies, attachments_list, fit_vectorizer=True)
        y = np.array(labels)
        
        self.clf.fit(X, y)
        self.is_trained = True
        
        joblib.dump(self.clf, config.MODEL_PATH)
        joblib.dump(self.vectorizer, config.VECTORIZER_PATH)
        print("[+] Model Random Forest da duoc huan luyen va toi uu hoa!")

    def load(self):
        if config.MODEL_PATH.exists() and config.VECTORIZER_PATH.exists():
            self.clf = joblib.load(config.MODEL_PATH)
            self.vectorizer = joblib.load(config.VECTORIZER_PATH)
            self.is_trained = True
        else:
            self.train()

    def predict(self, subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
        if not self.is_trained:
            self.load()
            
        if attachments is None:
            attachments = []
            
        X = self._prepare_feature_vector([subject], [body], [attachments], fit_vectorizer=False)
        pred_label = int(self.clf.predict(X)[0])
        probabilities = self.clf.predict_proba(X)[0]
        spam_score = float(probabilities[1]) if len(probabilities) > 1 else float(pred_label)
        
        handcrafted = extract_handcrafted_features(subject, body, attachments)
        
        # Nếu phát hiện file độc hại (.exe, .scr, .pdf.exe) -> Gắn nhãn MALWARE ngay lập tức
        if handcrafted["has_dangerous_file"] or handcrafted["has_double_extension"]:
            pred_label = 1
            spam_score = max(spam_score, 0.99)
            verdict = "MALWARE ATTACHMENT"
        elif pred_label == 1:
            verdict = "SPAM / PHISHING"
        else:
            verdict = "LEGIT (HAM)"
            
        return {
            "is_spam": bool(pred_label == 1),
            "spam_score": round(spam_score, 4),
            "verdict": verdict,
            "indicators": handcrafted
        }

if __name__ == "__main__":
    detector = SpamDetectionPipeline()
    detector.train()
