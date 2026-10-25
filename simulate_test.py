import sys
import io
import time
from threat_analyzer import ThreatAnalyzer

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_simulation():
    print("="*60)
    print("[*] BAT DAU MO PHONG KIEM THU 5 TRUONG HOP TOAN DIEN")
    print("="*60)
    
    analyzer = ThreatAnalyzer()
    
    # 1. Kich ban 1: Phishing Crypto (Anh ban gui)
    print("\n[Case 1] Gui 1 email lua dao Crypto / Thua ke...")
    sender1 = "fake_friend_99@gmail.com"
    subject1 = "My precious legacy for you"
    body1 = (
        "Doctors told me cancer is incurable. I have decided to travel alone "
        "and bid farewell to this world in silence. I have no children. "
        "My only regret is not being able to spend this life with you. "
        "You were my first love and will live forever in my heart. "
        "I leave behind a precious legacy. I hope this friendship will bring "
        "us together again in the next life. Please keep this information safe. "
        "rcslj.com Username: MB2536 Password: dt1288 Balance: 2,684,742.17 USDT ($)"
    )
    res1 = analyzer.analyze_email(sender1, subject1, body1)
    print(f"-> Ket qua: {res1['verdict']} (Diem rui ro: {res1['spam_score']*100:.1f}%)")

    # 2. Kich ban 2: Spam quang cao thong thuong
    print("\n[Case 2] Gui 1 email spam quang cao co bac/khuyen mai...")
    res2 = analyzer.analyze_email(
        sender="promo@casino-win.cc",
        subject="Tang 100k trai nghiem nha cai uy tin",
        body="Dang ky ngay hom nay de nhan 100k vao tai khoan rut tien sieu nhanh click tai day!"
    )
    print(f"-> Ket qua: {res2['verdict']} (Diem rui ro: {res2['spam_score']*100:.1f}%)")

    # 3. Kich ban 3: Email hoc tap / cong viec hop le (Ham)
    print("\n[Case 3] Gui 1 email hoc tap kem file PDF binh thuong...")
    res3 = analyzer.analyze_email(
        sender="nhomtruong@gmail.com",
        subject="Hop do an tot nghiep luc 9h sang mai",
        body="Chao cac ban, sang mai chung ta hop nhom de phan chia nhiem vu viet bao cao va hoan thien code nhe.",
        attachments=["Slide_Thuyet_Trinh.pdf"]
    )
    print(f"-> Ket qua: {res3['verdict']} (Diem rui ro: {res3['spam_score']*100:.1f}%)")

    # 4. Kich ban 4: Tan cong dondap Flood / Sybil Attack
    print("\n[Case 4] Mo phong 6 tai khoan Gmail clone spam don dap trong 5 giay...")
    for i in range(1, 7):
        res4 = analyzer.analyze_email(
            sender=f"clone_bot_{i}@gmail.com",
            subject=f"Uu dai dac biet dot {i}",
            body="Bam vao day de nhan thuong 500 USDT ngay lap tuc!"
        )
        print(f"  [{i}/6] Mail tu clone_bot_{i} | Flood Alert: {res4['is_flood_attack']}")
        time.sleep(0.3)

    # 5. Kich ban 5: Phat tan ma doc qua file dinh kem (.pdf.exe)
    print("\n[Case 5] Gui email dinh kem file ma doc gia mao duoi kep (.pdf.exe)...")
    res5 = analyzer.analyze_email(
        sender="fake_hr@company-corp.cc",
        subject="Cap nhat bang tinh luong thang 9",
        body="Phong Nhan su gui bang dieu chinh luong. Vui long mo file dinh kem de kiem tra.",
        attachments=["Bang_Luong_Dieu_Chinh.pdf.exe"]
    )
    print(f"-> Ket qua: {res5['verdict']} (Diem rui ro: {res5['spam_score']*100:.1f}%)")
    print(f"-> Canh bao ma doc: {res5['indicators']['dangerous_files']}")

    print("\n" + "="*60)
    print("[+] DA HOAN TAT MO PHONG! Tien hanh cap nhat Bao Cao Excel...")
    
    from export_excel import export_logs_to_excel
    excel_file = export_logs_to_excel("Bao_Cao_Phat_Hien_Spam.xlsx")
    print(f"[+] File Excel da san sang: {excel_file}")
    print("-> Ban co the mo Dashboard bang lenh: streamlit run dashboard.py")
    print("="*60)

if __name__ == "__main__":
    run_simulation()
