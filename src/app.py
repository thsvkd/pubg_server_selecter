import tkinter as tk
from tkinter import messagebox, Frame
import webbrowser
from PIL import Image, ImageTk
import subprocess
import win32serviceutil, win32service
import os, sys


class MainApplication(tk.Tk):
    WELCOME_MESSAGE = '설정하려는 서버를 선택하세요.'
    APP_NAME = 'pubg_server_selector'
    VERSION = 'v0.1.1'
    GITHUB_URL = 'https://github.com/thsvkd/pubg_server_selecter'

    def __init__(self):
        super().__init__()
        self.title(self.APP_NAME)
        self.geometry("350x160")  # 약간의 여유 공간 추가
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text=self.WELCOME_MESSAGE, wraplength=300)
        self.status_label.pack(pady=10)

        tk.Button(self, text="Kor/JP 서버", command=lambda: self.apply_settings('Korea Standard Time')).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Asia 서버", command=lambda: self.apply_settings('China Standard Time')).pack(fill=tk.X, padx=50, pady=5)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        version_label = tk.Label(bottom_frame, text=f"{self.APP_NAME}: {self.VERSION}", fg="grey", anchor="w")
        version_label.pack(side=tk.LEFT)

        image_path = os.path.join(sys._MEIPASS, 'res', 'github.png')
        original_image = Image.open(image_path)
        resized_image = original_image.resize((24, 24))
        self.github_img = ImageTk.PhotoImage(resized_image)

        github_button = tk.Button(bottom_frame, image=self.github_img, command=self.open_github, borderwidth=0)
        github_button.pack(side=tk.RIGHT, padx=10)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.status_label.update()

    def set_timezone(self, timezone_name):
        self.update_status(f'시간대를 {timezone_name}로 설정 중...')
        subprocess.run(['tzutil', '/s', timezone_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    def check_and_start_w32time(self):
        try:
            service_name = 'w32time'
            if win32serviceutil.QueryServiceStatus(service_name)[1] == 4:
                self.update_status('Windows Time 서비스가 이미 실행 중입니다.')
            else:
                self.update_status('Windows Time 서비스를 시작합니다...')
                win32serviceutil.StartService(service_name)
                win32serviceutil.WaitForServiceStatus(service_name, win32service.SERVICE_RUNNING, 10)
                self.update_status('서비스 시작 완료.')
        except Exception as e:
            messagebox.showerror('오류', f'서비스 시작 중 오류 발생: {e}')
            self.update_status('오류가 발생했습니다.')

    def resync_time(self):
        self.check_and_start_w32time()

    def apply_settings(self, timezone):
        try:
            self.set_timezone(timezone)
            self.resync_time()
            self.update_status('서버 설정이 완료되었습니다.')
            messagebox.showinfo('완료', '서버 설정이 완료되었습니다.')
            self.update_status(self.WELCOME_MESSAGE)
        except subprocess.CalledProcessError as e:
            self.update_status('오류가 발생했습니다.')
            messagebox.showerror('오류', f'오류 발생: {e}')
            self.update_status('오류가 발생했습니다.')

    def open_github(self):
        webbrowser.open(self.GITHUB_URL)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
