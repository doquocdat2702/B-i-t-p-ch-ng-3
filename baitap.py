import os
import shutil
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path="load_nguoidung.env")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SOURCE_DIR = "./"
BACKUP_DIR = "./backup/"

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'], msg['From'], msg['To'] = subject, SENDER_EMAIL, RECEIVER_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("[INFO] Email Đã Được Gửi Thành Công.")
    except Exception as e:
        print(f"[ERROR] Lỗi Khi Gửi Email: {e}")

def backup_database():
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        db_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith((".sql", ".sqlite3"))]
        if not db_files:
            send_email("Cảnh báo: Không tìm thấy file .sql hoặc .sqlite3.", "Không có file cơ sở dữ liệu để sao lưu.")
            return

        backup_files = []
        for file in db_files:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dst = os.path.join(BACKUP_DIR, f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}")
            shutil.copy2(os.path.join(SOURCE_DIR, file), dst)
            backup_files.append(os.path.basename(dst))

        send_email("Backup Thành Công", f"Sao lưu thành công:\n" + "\n".join(backup_files))
        print(f"[INFO] Backup successful: {backup_files}")
    except Exception as e:
        send_email("Backup Thất Bại", f"Lỗi khi sao lưu: {e}")
        print(f"[ERROR] Backup failed: {e}")

def main():
    print("[INFO] Đang thực hiện sao lưu ngay...")
   # backup_database()
    schedule.every().day.at("00:00").do(backup_database)
    print("[INFO] Hệ Thống Đang Khởi Động. Xin Vui Lòng Chờ Đợi")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
