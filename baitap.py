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

SOURCE_FILE = "C:/Users/Admin/Downloads/ASP.NET-MVC-master/ASP.NET-MVC-master/Database/BanDongHo.sql"
BACKUP_DIR = "E:/bai tap/backup"

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("[INFO] Email đã được gửi thành công.")
    except Exception as e:
        print(f"[ERROR] Lỗi khi gửi email: {e}")

def backup_database():
    try:
        if not os.path.isfile(SOURCE_FILE):
            raise FileNotFoundError(f"Không tìm thấy file: {SOURCE_FILE}")

        os.makedirs(BACKUP_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.basename(SOURCE_FILE)
        name, ext = os.path.splitext(file_name)

        backup_file_name = f"{name}_{timestamp}{ext}"
        backup_path = os.path.join(BACKUP_DIR, backup_file_name)

        shutil.copy2(SOURCE_FILE, backup_path)

        send_email("Backup thành công", f"Đã sao lưu tập tin thành công:\n{backup_file_name}")
        print(f"[INFO] Backup thành công: {backup_file_name}")

    except Exception as e:
        send_email("Backup thất bại", f"Lỗi khi sao lưu: {e}")
        print(f"[ERROR] Backup thất bại: {e}")

def main():
    print("[INFO] Đang thực hiện sao lưu ngay...")
    #backup_database()

    print("[INFO] Thiết lập lịch sao lưu tự động mỗi ngày lúc 00:00.")
    schedule.every().day.at("00:00").do(backup_database)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
