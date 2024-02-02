import win32serviceutil, win32service
import subprocess
import tkinter as tk
from tkinter import messagebox

WELCOME_MESSAGE = "설정하려는 서버를 선택하세요."


def update_status(status_label, message):
    status_label.config(text=message)
    status_label.update()


def set_timezone(status_label, timezone_name):
    update_status(status_label, f"시간대를 {timezone_name}로 설정 중...")
    subprocess.run(["tzutil", "/s", timezone_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)


def check_and_start_w32time(status_label):
    try:
        service_name = "w32time"
        if win32serviceutil.QueryServiceStatus(service_name)[1] == 4:  # 4는 서비스가 실행 중임을 나타냄
            update_status(status_label, "Windows Time 서비스가 이미 실행 중입니다.")
        else:
            update_status(status_label, "Windows Time 서비스를 시작합니다...")
            win32serviceutil.StartService(service_name)
            win32serviceutil.WaitForServiceStatus(service_name, win32service.SERVICE_RUNNING, 10)  # 10초 동안 서비스가 시작될 때까지 기다림
            update_status(status_label, "서비스 시작 완료.")
    except Exception as e:
        messagebox.showerror("오류", f"서비스 시작 중 오류 발생: {e}")
        update_status(status_label, "오류가 발생했습니다.")


def resync_time(status_label):
    # Windows API를 직접 호출하여 시간 동기화를 수행하는 것은 제한됩니다.
    # 이 함수 내에서 'w32tm /resync' 명령의 직접적인 대체는 제공하지 않습니다.
    # 대신, 'w32time' 서비스를 재시작하는 것으로 간접적인 시간 동기화를 시도할 수 있습니다.
    check_and_start_w32time(status_label)


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


def main():
    window = tk.Tk()
    window.title("PUBG 서버 설정 도우미")
    window.geometry("300x125")

    status_label = tk.Label(window, text=WELCOME_MESSAGE, wraplength=300)
    status_label.pack(pady=10)

    tk.Button(window, text="Kor/JP 서버", command=lambda: apply_settings(status_label, "Korea")).pack(fill=tk.X, padx=50, pady=5)
    tk.Button(window, text="Asia 서버", command=lambda: apply_settings(status_label, "China")).pack(fill=tk.X, padx=50, pady=5)

    window.mainloop()


if __name__ == "__main__":
    main()
