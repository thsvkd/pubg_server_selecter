import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

WELCOME_MESSAGE = "설정하려는 서버를 선택하세요."


def update_status(status_label, message):
    status_label.config(text=message)
    status_label.update()


def set_timezone(status_label, timezone_name):
    update_status(status_label, f"시간대를 {timezone_name}로 설정 중...")
    subprocess.run(["tzutil", "/s", timezone_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)


def check_and_start_w32time(status_label):
    service_status = subprocess.run(["sc", "query", "w32time"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    if "RUNNING" in service_status.stdout:
        update_status(status_label, "Windows Time 서비스가 이미 실행 중입니다.")
    else:
        update_status(status_label, "Windows Time 서비스를 시작합니다...")
        subprocess.run(["net", "start", "w32time"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        update_status(status_label, "서비스 시작 완료.")


def resync_time(status_label):
    update_status(status_label, "시간 동기화 중...")
    subprocess.run(["w32tm", "/resync"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    update_status(status_label, "시간 동기화 완료.")


def apply_settings(status_label, timezone):
    try:
        if timezone == "Korea":
            set_timezone(status_label, "Korea Standard Time")
        elif timezone == "China":
            set_timezone(status_label, "China Standard Time")
        check_and_start_w32time(status_label)
        resync_time(status_label)
        messagebox.showinfo("완료", "모든 설정이 완료되었습니다.")
        update_status(status_label, WELCOME_MESSAGE)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"오류 발생: {e}")
        update_status(status_label, "오류가 발생했습니다.")


def setup_gui():
    window = tk.Tk()
    window.title("PUBG 서버 설정 도우미")
    window.geometry("300x125")

    status_label = tk.Label(window, text=WELCOME_MESSAGE, wraplength=300)
    status_label.pack(pady=10)

    tk.Button(window, text="Kor/JP 서버", command=lambda: apply_settings(status_label, "Korea")).pack(fill=tk.X, padx=50, pady=5)
    tk.Button(window, text="Asia 서버", command=lambda: apply_settings(status_label, "China")).pack(fill=tk.X, padx=50, pady=5)

    window.mainloop()


if __name__ == "__main__":
    setup_gui()
