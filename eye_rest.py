import tkinter as tk
import tkinter.messagebox as messagebox
import json
import os
import sys
import socket
import time
import datetime
import math
import ctypes

TEST_MODE = "--test" in sys.argv
INTERVAL_MIN = 20
BREAK_SEC = 20
PORT = 28940
CHECK_MS = 10000
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eye_rest_config.json")
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eye_rest_state.json")

DEFAULT_TEXT = "该休息眼睛了！\n\n看看远处 20 英尺（约 6 米）以外的物体\n至少 20 秒，让睫状肌放松\n\n（20-20-20 法则）"


def load_config():
    cfg = {"interval_min": INTERVAL_MIN, "break_sec": BREAK_SEC, "text": DEFAULT_TEXT}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:
        pass
    return cfg


def write_state(ts):
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump({"next_reminder": fmt_time(ts)}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def read_state():
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def boot_time():
    ms = ctypes.windll.kernel32.GetTickCount64()
    return time.time() - ms / 1000.0


def fmt_time(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%H:%M")


cfg = load_config()
interval_s = int(cfg["interval_min"] * 60)
break_sec = int(cfg["break_sec"])
reminder_text = cfg.get("text", DEFAULT_TEXT)

BOOT_TS = boot_time()


def next_reminder_ts(now=None):
    if now is None:
        now = time.time()
    n = math.ceil((now - BOOT_TS) / interval_s)
    if n < 1:
        n = 1
    return BOOT_TS + n * interval_s


next_ts = next_reminder_ts()

root = tk.Tk()
root.title("护眼提醒")
root.withdraw()


def check_loop():
    global next_ts
    now = time.time()
    if now >= next_ts:
        next_ts = next_reminder_ts(now)
        write_state(next_ts)
        show_reminder()
    root.after(CHECK_MS, check_loop)


def show_reminder():
    win = tk.Toplevel(root)
    win.title("休息一下")
    win.attributes("-topmost", True)
    win.geometry("480x360")
    win.configure(bg="#f0f8ff")

    tk.Label(win, text=f"已经连续工作 {cfg['interval_min']} 分钟", font=("Microsoft YaHei", 16, "bold"),
             bg="#f0f8ff", fg="#1e5aa8").pack(pady=(24, 8))

    tk.Label(win, text=reminder_text, font=("Microsoft YaHei", 13),
             bg="#f0f8ff", fg="#333333", justify="left").pack(pady=8, padx=30)

    countdown_var = tk.StringVar(value=f"休息 {break_sec} 秒后可继续工作")
    tk.Label(win, textvariable=countdown_var, font=("Microsoft YaHei", 11),
             bg="#f0f8ff", fg="#666666").pack(pady=4)

    close_btn = tk.Button(win, text="我已休息好，继续工作", font=("Microsoft YaHei", 12),
                          command=lambda: close_window(win), bg="#4caf50", fg="white",
                          activebackground="#388e3c", activeforeground="white",
                          relief="flat", padx=20, pady=6)
    close_btn.pack(pady=14)

    snooze_btn = tk.Button(win, text="5 分钟后提醒", font=("Microsoft YaHei", 10),
                           command=lambda: snooze(win), bg="#ff9800", fg="white",
                           activebackground="#f57c00", activeforeground="white",
                           relief="flat", padx=14, pady=4)
    snooze_btn.pack()

    remaining = break_sec
    win._countdown = [remaining]

    def tick():
        if win.winfo_exists():
            win._countdown[0] -= 1
            if win._countdown[0] > 0:
                countdown_var.set(f"休息 {win._countdown[0]} 秒后可继续工作")
                win.after(1000, tick)
            else:
                countdown_var.set("可以继续工作了")
                close_btn.config(state="normal")

    tick()


def close_window(win):
    win.destroy()
    if TEST_MODE:
        root.destroy()


def snooze(win):
    global next_ts
    win.destroy()
    if not TEST_MODE:
        next_ts = time.time() + 300
        write_state(next_ts)


def already_running():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv.bind(("127.0.0.1", PORT))
        srv.listen(1)
        return None, srv
    except OSError:
        return True, None


if __name__ == "__main__":
    running, srv = already_running()
    if running and not TEST_MODE:
        notify = tk.Tk()
        notify.withdraw()
        state = read_state()
        next_str = state.get("next_reminder", "未知")
        now_str = datetime.datetime.now().strftime("%H:%M")
        messagebox.showinfo(
            "护眼提醒",
            f"护眼提醒已在后台运行。\n\n当前时间：{now_str}\n下次提醒：{next_str}\n\n（计时以开机时间为准，不受本次点击影响）",
            parent=notify,
        )
        notify.destroy()
        sys.exit(0)
    if TEST_MODE:
        root.after(1000, show_reminder)
    else:
        write_state(next_ts)
        check_loop()
    root.mainloop()
