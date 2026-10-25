import sys
import pandas as pd
from pathlib import Path
from threat_analyzer import ThreatAnalyzer
from export_excel import export_logs_to_excel
import config

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_csv_pipeline(input_csv_path: str = "dataset_input.csv", output_csv_path: str = "dataset_output.csv"):
    """
    Đọc dữ liệu ĐẦU VÀO từ file CSV -> Đưa qua mô hình AI & Phân tích -> Xuất kết quả ĐẦU RA.
    """
    csv_file = Path(input_csv_path)
    if not csv_file.exists():
        print(f"[!] Không tìm thấy file đầu vào: {input_csv_path}")
        return

    print(f"[*] ĐANG NẠP DỮ LIỆU ĐẦU VÀO TỪ: {input_csv_path}...")
    df_input = pd.read_csv(csv_file, encoding="utf-8")

    analyzer = ThreatAnalyzer()
    output_rows = []

    for _, row in df_input.iterrows():
        stt = row.get("STT")
        sender = str(row.get("Nguoi_Gui", ""))
        sender_ip = str(row.get("IP_Nguon", "Không xác định"))
        subject = str(row.get("Tieu_De", ""))
        body = str(row.get("Noi_Dung", ""))
        att_str = str(row.get("File_Dinh_Kem", ""))
        attachments = [att_str] if att_str and att_str != "nan" else []
        scenario = str(row.get("Kich_Ban", ""))

        # Đưa vào pipeline phân tích
        res = analyzer.analyze_email(
            sender=sender,
            subject=subject,
            body=body,
            attachments=attachments,
            sender_ip=sender_ip
        )

        indicators = res.get("indicators", {})
        spam_score = res.get("spam_score", 0.0)
        is_spam = res.get("is_spam", False)
        is_flood = res.get("is_flood_attack", False)

        output_rows.append({
            "STT": stt,
            "Nguoi_Gui": sender,
            "IP_Nguon": sender_ip,
            "Quoc_Gia": row.get("Quoc_Gia", ""),
            "Tieu_De": subject,
            "So_Luong_Link_URL": indicators.get("url_count", 0),
            "Bay_Mat_Khau_UserPass": indicators.get("has_credentials", 0),
            "Tien_Ao_Crypto_USDT": int(bool(indicators.get("has_crypto", 0) or indicators.get("has_huge_money", 0))),
            "File_Doc_Hai": int(bool(indicators.get("has_dangerous_file", 0) or indicators.get("has_double_extension", 0))),
            "Tan_Cong_Flood": int(is_flood),
            "Diem_Rui_Ro_AI": f"{spam_score*100:.1f}%",
            "Nhan_Ket_Qua": 1 if is_spam else 0,
            "Ket_Luan": "🚨 SPAM / LỪA ĐẢO / MÃ ĐỘC" if is_spam else "✅ HỢP LỆ (SẠCH)",
            "Kich_Ban_Goc": scenario
        })

    # Xuất ra CSV kết quả
    df_output = pd.DataFrame(output_rows)
    df_output.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"[+] ĐÃ XUẤT KẾT QUẢ ĐẦU RA THÀNH CÔNG RA: {output_csv_path}")

    # Đồng bộ sang Excel 4 sheet
    excel_path = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
    print(f"[+] ĐÃ ĐỒNG BỘ BÁO CÁO EXCEL TẠI: {excel_path}")

if __name__ == "__main__":
    run_csv_pipeline()
