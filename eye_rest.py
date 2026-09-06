#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eye Rest Reminder - Apple Glassmorphism UI
"""

import webview, json, os, sys, socket, time, datetime, math, ctypes, ctypes.wintypes, threading, tempfile, re, shutil

HTML = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>护眼提醒</title>\n<style>\n@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\');\n*{margin:0;padding:0;box-sizing:border-box}\nhtml,body{height:100%}\nbody{\n  font-family:\'Inter\',-apple-system,\'Microsoft YaHei\',sans-serif;\n  height:100vh;overflow-y:auto;overflow-x:hidden;\n  display:flex;align-items:flex-start;justify-content:center;\n  user-select:none;\n  background:linear-gradient(160deg,rgba(15,12,41,0.85) 0%,rgba(26,26,62,0.7) 35%,rgba(36,36,62,0.65) 65%,rgba(13,13,26,0.85) 100%),url("WALLPAPER_PLACEHOLDER") center/cover no-repeat fixed;\n}\n.orb{position:fixed;border-radius:50%;filter:blur(100px);opacity:0.3;pointer-events:none}\n.orb-1{width:500px;height:500px;background:radial-gradient(circle,rgba(108,140,255,0.4),transparent 70%);top:-200px;right:-120px}\n.orb-2{width:450px;height:450px;background:radial-gradient(circle,rgba(167,139,250,0.3),transparent 70%);bottom:-180px;left:-100px}\n.orb-3{width:250px;height:250px;background:radial-gradient(circle,rgba(244,114,182,0.2),transparent 70%);top:30%;right:5%}\n.glass{\n  margin:auto;\n  width:400px;padding:36px 32px 32px;\n  background:rgba(255,255,255,0.04);\n  backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);\n  z-index:1;animation:fadeIn 0.7s cubic-bezier(0.16,1,0.3,1);\n  border:none;\n  border-radius:0 !important;\n}\n@keyframes fadeIn{from{opacity:0;transform:scale(0.9) translateY(24px)}to{opacity:1;transform:scale(1) translateY(0)}}\n.header{text-align:center;margin-bottom:24px}\n.icon-wrap{width:72px;height:72px;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;font-size:38px;background:rgba(255,255,255,0.06);animation:float 3s ease-in-out infinite;border:none}\n@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}\n.header h1{font-size:24px;font-weight:700;color:rgba(255,255,255,0.92);letter-spacing:-0.3px;margin-bottom:4px}\n.header .sub{font-size:13px;font-weight:400;color:rgba(255,255,255,0.4)}\n.ring-wrap{display:flex;justify-content:center;margin-bottom:24px}\n.ring-svg{position:relative;width:150px;height:150px;flex-shrink:0}\n.ring-svg svg{width:100%;height:100%;transform:rotate(-90deg)}\n.bg-ring{fill:none;stroke:rgba(255,255,255,0.05);stroke-width:6}\n.progress-ring{fill:none;stroke:url(#grad);stroke-width:6;stroke-linecap:round;stroke-dasharray:424;stroke-dashoffset:0;transition:stroke-dashoffset 0.5s cubic-bezier(0.4,0,0.2,1);filter:drop-shadow(0 0 8px rgba(108,140,255,0.3))}\n.ring-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}\n.ring-num{display:block;font-size:36px;font-weight:700;color:rgba(255,255,255,0.93);letter-spacing:-1px;line-height:1;font-variant-numeric:tabular-nums}\n.ring-unit{display:block;font-size:12px;font-weight:400;color:rgba(255,255,255,0.35);margin-top:2px;letter-spacing:2px;text-transform:uppercase}\n.info-box{background:rgba(255,255,255,0.03);padding:12px 16px;margin-bottom:24px;text-align:center}\n.info-box p{font-size:13px;line-height:1.6;color:rgba(255,255,255,0.65)}\n.info-box .hl{color:rgba(108,140,255,0.9);font-weight:600}\n.actions{display:flex;flex-direction:column;gap:10px}\n.btn{display:block;width:100%;padding:12px 0;overflow:hidden;font-family:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:all 0.2s;outline:none;position:relative;border:none;-webkit-appearance:none;background:linear-gradient(135deg,rgba(108,140,255,0.28) 0%,rgba(108,140,255,0.12) 40%,rgba(167,139,250,0.08) 100%);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);color:rgba(255,255,255,0.95);box-shadow:0 4px 20px rgba(108,140,255,0.15),inset 0 1px 0 rgba(255,255,255,0.25),inset 0 -1px 0 rgba(0,0,0,0.08)}\n.btn:hover{background:linear-gradient(135deg,rgba(108,140,255,0.38) 0%,rgba(108,140,255,0.18) 40%,rgba(167,139,250,0.12) 100%);box-shadow:0 8px 30px rgba(108,140,255,0.25),inset 0 1px 0 rgba(255,255,255,0.3);transform:translateY(-1px)}\n.btn:active{transform:scale(0.97)}\n.btn2{background:linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.02) 100%);color:rgba(255,255,255,0.5);font-size:13px;padding:10px 0;box-shadow:inset 0 1px 0 rgba(255,255,255,0.08)}\n.btn2:hover{background:linear-gradient(180deg,rgba(255,255,255,0.08) 0%,rgba(255,255,255,0.03) 100%);color:rgba(255,255,255,0.75)}\n.ripple{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.55) 0%,rgba(255,255,255,0.2) 55%,rgba(255,255,255,0) 72%);transform:scale(0);opacity:1;pointer-events:none;animation:ripple .62s cubic-bezier(.22,.61,.36,1) forwards}\n@keyframes ripple{to{transform:scale(2.6);opacity:0}}\nbody::-webkit-scrollbar{width:0;height:0}\n</style>\n</head>\n<body>\n<div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div>\n<svg width="0" height="0" style="position:absolute">\n  <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6c8cff"/><stop offset="100%" stop-color="#a78bfa"/></linearGradient></defs>\n</svg>\n<div class="glass">\n  <div class="header">\n    <div class="icon-wrap" id="iconMain">&#x23F0;</div>\n    <h1 id="titleMain">护眼倒计时</h1>\n    <p class="sub" id="subtitle">距下次休息还有</p>\n  </div>\n  <div class="ring-wrap">\n    <div class="ring-svg">\n      <svg viewBox="0 0 140 140">\n        <circle class="bg-ring" cx="70" cy="70" r="67.5"/>\n        <circle class="progress-ring" id="progress" cx="70" cy="70" r="67.5" stroke-dasharray="424" stroke-dashoffset="0"/>\n      </svg>\n      <div class="ring-text">\n        <span class="ring-num" id="timerNum">20:00</span>\n        <span class="ring-unit" id="timerUnit">分钟</span>\n      </div>\n    </div>\n  </div>\n  <div class="info-box" id="statusBox">\n    <p>下次休息时间：<span class="hl" id="nextTimeLabel">--:--</span></p>\n  </div>\n  <div class="info-box" id="readyBox" style="display:none">\n    <p>时间到了，点击下方按钮开始休息</p>\n  </div>\n  <div class="info-box" id="breakBox" style="display:none">\n    <p id="breakText">该休息眼睛了！</p>\n  </div>\n  <div class="actions">\n    <button class="btn" id="btnStart" style="display:none">开始休息</button>\n    <button class="btn" id="btnDismiss" style="display:none">我已经休息好了</button>\n    <button class="btn btn2" id="btnSnooze" style="display:none">5 分钟后提醒</button>\n  </div>\n</div>\n<script>\nfunction setTimerCount(s,p,t){var m=Math.floor(s/60),se=s%60;document.getElementById(\'timerNum\').textContent=(m<10?\'0\':\'\')+m+\':\'+(se<10?\'0\':\'\')+se;if(t){document.getElementById(\'nextTimeLabel\').textContent=t;}document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));}\nfunction setBreakCount(s,p){document.getElementById(\'timerNum\').textContent=String(s);document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));}\nvar C=424;\nfunction api(m,n){n=n||0;var f=null;try{f=(window.pywebview&&pywebview.api)?pywebview.api[m]:null;}catch(e){f=null}if(typeof f===\'function\'){try{var r=f();if(r&&typeof r.catch===\'function\'){r.catch(function(){});}return;}catch(e){}}if(n<40){setTimeout(function(){api(m,n+1);},120);}}\nfunction ripple(e,el){try{var r=el.getBoundingClientRect();var d=Math.max(r.width,r.height)*1.1;var x=(e&&typeof e.clientX===\'number\')?e.clientX:r.left+r.width/2;var y=(e&&typeof e.clientY===\'number\')?e.clientY:r.top+r.height/2;var s=document.createElement(\'span\');s.className=\'ripple\';s.style.width=s.style.height=d+\'px\';s.style.left=(x-r.left-d/2)+\'px\';s.style.top=(y-r.top-d/2)+\'px\';el.appendChild(s);setTimeout(function(){if(s.parentNode){s.parentNode.removeChild(s);}},640);}catch(err){}}\nfunction modeTimer(s,p,t){\n  document.getElementById(\'iconMain\').textContent=\'\\u23F0\';document.getElementById(\'titleMain\').textContent=\'护眼倒计时\';document.getElementById(\'subtitle\').textContent=\'距下次休息还有\';document.getElementById(\'statusBox\').style.display=\'block\';document.getElementById(\'readyBox\').style.display=\'none\';document.getElementById(\'breakBox\').style.display=\'none\';document.getElementById(\'btnStart\').style.display=\'none\';document.getElementById(\'btnDismiss\').style.display=\'none\';document.getElementById(\'btnSnooze\').style.display=\'none\';document.getElementById(\'nextTimeLabel\').textContent=t||\'--:--\';var m=Math.floor(s/60),se=s%60;document.getElementById(\'timerNum\').textContent=(m<10?\'0\':\'\')+m+\':\'+(se<10?\'0\':\'\')+se;document.getElementById(\'timerUnit\').textContent=\'\\u5206\\u949F\';document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));\n}\nfunction modeReady(){\n  document.getElementById(\'iconMain\').textContent=\'\\u{1F440}\';document.getElementById(\'titleMain\').textContent=\'\\u4F11\\u606F\\u65F6\\u95F4\\u5230\';document.getElementById(\'subtitle\').textContent=\'\\u8BE5\\u8BA9\\u773C\\u775B\\u4F11\\u606F\\u4E00\\u4E0B\\u4E86\';document.getElementById(\'statusBox\').style.display=\'none\';document.getElementById(\'readyBox\').style.display=\'block\';document.getElementById(\'breakBox\').style.display=\'none\';document.getElementById(\'btnStart\').style.display=\'block\';document.getElementById(\'btnDismiss\').style.display=\'none\';document.getElementById(\'btnSnooze\').style.display=\'block\';document.getElementById(\'timerNum\').textContent=\'0\';document.getElementById(\'timerUnit\').textContent=\'\\u79D2\';document.getElementById(\'progress\').style.strokeDashoffset=C;\n}\nfunction modeBreak(s,p,t){\n  document.getElementById(\'iconMain\').textContent=\'\\u{1F440}\';document.getElementById(\'titleMain\').textContent=\'\\u4F11\\u606F\\u4E00\\u4E0B\';document.getElementById(\'subtitle\').textContent=\'\\u8BA9\\u773C\\u775B\\u653E\\u677E\\u4E00\\u4E0B\\u5427\';document.getElementById(\'statusBox\').style.display=\'none\';document.getElementById(\'readyBox\').style.display=\'none\';document.getElementById(\'breakBox\').style.display=\'block\';document.getElementById(\'btnStart\').style.display=\'none\';document.getElementById(\'btnDismiss\').style.display=\'block\';document.getElementById(\'btnSnooze\').style.display=\'none\';document.getElementById(\'breakText\').innerHTML=t.replace(/\\n/g,\'<br>\');document.getElementById(\'timerNum\').textContent=String(s);document.getElementById(\'timerUnit\').textContent=\'\\u79D2\';document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));\n}\ndocument.getElementById(\'btnStart\').addEventListener(\'click\',function(e){ripple(e,this);api(\'startBreak\');});\ndocument.getElementById(\'btnDismiss\').addEventListener(\'click\',function(e){ripple(e,this);api(\'dismiss\');});\ndocument.getElementById(\'btnSnooze\').addEventListener(\'click\',function(e){ripple(e,this);api(\'snooze\');});\n</script>\n</body>\n</html>'


TEST_MODE = '--test' in sys.argv
INTERVAL_MIN = 20
BREAK_SEC = 20
PORT = 28940
MIN_INTERVAL_MIN = 1
MAX_INTERVAL_MIN = 1440
MIN_BREAK_SEC = 1
MAX_BREAK_SEC = 600
MAX_TEXT_LEN = 600
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eye_rest_config.json')
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eye_rest_state.json')
DEFAULT_TEXT = '该休息眼睛了！\n\n看看远处 20 英尺（约 6 米）以外的物体\n至少 20 秒，让睫状肌放松\n\n（20-20-20 法则）'


def _coerce_int(value, default, lo, hi):
    try:
        n = float(value)
    except (TypeError, ValueError):
        return default
    if n != n or n in (float('inf'), float('-inf')):
        return default
    return max(lo, min(hi, int(n)))

def load_config():
    cfg = {'interval_min': INTERVAL_MIN, 'break_sec': BREAK_SEC, 'text': DEFAULT_TEXT}
    try:
        # utf-8-sig: a config saved by Notepad or PowerShell carries a BOM,
        # which would otherwise make json.load() fail and silently drop it.
        with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        if isinstance(data, dict): cfg.update(data)
    except Exception: pass
    # The config is hand-editable, so never trust it: a zero interval divides by
    # zero and a negative one keeps the reminder permanently overdue, which would
    # spin the timer loop and freeze the countdown.
    cfg['interval_min'] = _coerce_int(cfg.get('interval_min'), INTERVAL_MIN, MIN_INTERVAL_MIN, MAX_INTERVAL_MIN)
    cfg['break_sec'] = _coerce_int(cfg.get('break_sec'), BREAK_SEC, MIN_BREAK_SEC, MAX_BREAK_SEC)
    text = cfg.get('text', DEFAULT_TEXT)
    if not isinstance(text, str) or not text.strip():
        text = DEFAULT_TEXT
    # An arbitrarily long message makes the card taller than the screen.
    cfg['text'] = text[:MAX_TEXT_LEN]
    return cfg

def write_state(ts):
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump({'next_reminder': fmt_time(ts)}, f, ensure_ascii=False, indent=2)
    except: pass

def boot_time():
    return time.time() - ctypes.windll.kernel32.GetTickCount64() / 1000.0

def fmt_time(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M')

def get_wallpaper_url():
    try:
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.user32.SystemParametersInfoW(0x0073, 260, buf, 0)
        path = buf.value
        if path and os.path.exists(path):
            ext = os.path.splitext(path)[1].lower()
            dest = os.path.join(tempfile.gettempdir(), 'eye_rest_wallpaper' + ext)
            shutil.copy2(path, dest)
            return 'file:///' + dest.replace('\\', '/')
    except: pass
    return ''

cfg = load_config()
interval_s = int(cfg['interval_min'] * 60)
break_sec = int(cfg['break_sec'])
reminder_text = cfg.get('text', DEFAULT_TEXT)
BOOT_TS = boot_time()
WALLPAPER_URL = get_wallpaper_url()

def next_reminder_ts(now=None):
    if now is None: now = time.time()
    n = math.ceil((now - BOOT_TS) / interval_s)
    if n < 1: n = 1
    return BOOT_TS + n * interval_s

def inject_wallpaper(html_str):
    if WALLPAPER_URL:
        return html_str.replace('WALLPAPER_PLACEHOLDER', WALLPAPER_URL)
    return re.sub(r',\s*url\("WALLPAPER_PLACEHOLDER"\)', '', html_str)

HTML = inject_wallpaper(HTML)

_TEMP_DIR = os.path.join(tempfile.gettempdir(), 'eye_rest_reminder_html')
os.makedirs(_TEMP_DIR, exist_ok=True)
with open(os.path.join(_TEMP_DIR, 'main.html'), 'w', encoding='utf-8') as f: f.write(HTML)

class ReminderApi:
    def __init__(self):
        self._on_start = None
        self._on_dismiss = None
        self._on_snooze = None
        self._data = json.dumps({'interval_min': cfg['interval_min'], 'break_sec': break_sec, 'text': reminder_text})
    def set_callbacks(self, s, d, z):
        self._on_start = s
        self._on_dismiss = d
        self._on_snooze = z
    def get_initial(self):
        return self._data
    def startBreak(self):
        try:
            if self._on_start: self._on_start()
        except: pass
    def dismiss(self):
        try:
            if self._on_dismiss: self._on_dismiss()
        except: pass
    def snooze(self):
        try:
            if self._on_snooze: self._on_snooze()
        except: pass

next_ts = next_reminder_ts()
_reminder_api = ReminderApi()
_done = threading.Event()
_break_end = threading.Event()
_break_started = threading.Event()
_state = {'next_ts': next_ts, 'alive': True}

SHOW_CMD = b'SHOW'

def acquire_port(retries=12, delay=0.25):
    # Right after a previous instance exits the socket can still be unavailable,
    # so retry instead of concluding that another instance owns the port.
    for _ in range(retries):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            srv.bind(('127.0.0.1', PORT))
            srv.listen(4)
            return srv
        except OSError:
            try:
                srv.close()
            except OSError:
                pass
            time.sleep(delay)
    return None

def notify_running_instance():
    # Ask the instance that owns the port to bring its timer window to the front.
    try:
        conn = socket.create_connection(('127.0.0.1', PORT), timeout=3)
    except OSError:
        return False
    try:
        conn.sendall(SHOW_CMD)
        return True
    except OSError:
        return False
    finally:
        try:
            conn.close()
        except OSError:
            pass

WINDOW_TITLE = '\u62a4\u773c\u63d0\u9192'

def find_hwnd():
    # Locate our own top-level window by owning process id, which works even
    # while the window is hidden or minimised.
    try:
        u32 = ctypes.windll.user32
        pid = os.getpid()
        found = []
        u32.GetWindow.restype = ctypes.wintypes.HWND
        def cb(hwnd, _):
            out_pid = ctypes.wintypes.DWORD()
            u32.GetWindowThreadProcessId(hwnd, ctypes.byref(out_pid))
            # keep top-level windows owned by this process (GW_OWNER == 4)
            if out_pid.value == pid and not u32.GetWindow(hwnd, 4):
                found.append(hwnd)
            return True
        proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)(cb)
        u32.EnumWindows(proc, 0)
        if not found:
            return None
        # Prefer the window carrying our title if more than one candidate exists.
        u32.GetWindowTextLengthW.restype = ctypes.c_int
        for hwnd in found:
            try:
                n = u32.GetWindowTextLengthW(hwnd)
                if n:
                    buf = ctypes.create_unicode_buffer(n + 1)
                    u32.GetWindowTextW(hwnd, buf, n + 1)
                    if buf.value == WINDOW_TITLE:
                        return hwnd
            except Exception:
                continue
        return found[0]
    except Exception:
        return None

SW_RESTORE = 9

def _show_window(hwnd, flags):
    try:
        u32 = ctypes.windll.user32
        u32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
        u32.ShowWindow.restype = ctypes.wintypes.BOOL
        u32.ShowWindow(hwnd, flags)
    except Exception:
        pass

def window_needs_restore(hwnd):
    if not hwnd:
        return True
    try:
        u32 = ctypes.windll.user32
        u32.IsWindowVisible.restype = ctypes.wintypes.BOOL
        u32.IsIconic.restype = ctypes.wintypes.BOOL
        return (not u32.IsWindowVisible(hwnd)) or bool(u32.IsIconic(hwnd))
    except Exception:
        return True

def bring_to_front(win, focus=True):
    # Only touch the window when it is actually hidden or minimised. Resizing or
    # re-activating an already visible window would move it under the cursor and
    # can turn a stray mouse event into an unintended button click.
    if not _state['alive'] or not win:
        return
    global _current_mode
    hwnd = find_hwnd()
    if window_needs_restore(hwnd):
        try:
            win.restore()
        except Exception:
            pass
        try:
            win.show()
        except Exception:
            pass
        if hwnd:
            _show_window(hwnd, SW_RESTORE)
        # Form.Show() drops the window back to its default 440x500 size, which
        # would clip the card again. Re-apply the size fitted for this mode.
        try:
            mode = _current_mode or 'timer'
            _current_mode = None
            resize_for_mode(win, mode)
        except Exception:
            pass
    if hwnd and focus:
        try:
            u32 = ctypes.windll.user32
            u32.SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
            u32.SetForegroundWindow(hwnd)
        except Exception:
            pass

def on_closing():
    # Closing the window only hides it; the reminder keeps running in the
    # background and the desktop shortcut brings it back.
    try:
        if not _state['alive'] or _done.is_set():
            return True
        if webview.windows:
            webview.windows[0].hide()
        return False
    except Exception:
        return False

def serve_show_requests(srv, win):
    srv.settimeout(1.0)
    while not _done.is_set() and _state['alive']:
        try:
            conn, _ = srv.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        try:
            conn.settimeout(2.0)
            if conn.recv(16).strip() == SHOW_CMD:
                bring_to_front(win)
        except OSError:
            pass
        finally:
            try:
                conn.close()
            except OSError:
                pass

def eval_js(win, js):
    if not _state['alive']:
        return
    try:
        if win: win.evaluate_js(js)
    except: pass

WINDOW_WIDTH = 440
MODE_HEIGHTS = {'timer': 500, 'ready': 550, 'break': 680}
FIT_MARGIN = 8
_current_mode = 'timer'

def screen_height():
    try:
        return int(ctypes.windll.user32.GetSystemMetrics(1))
    except Exception:
        return 1080

def measure_card(win):
    js = ("(function(){var g=document.querySelector('.glass');"
          "if(!g){return ''}return Math.ceil(g.offsetHeight)+'|'+window.innerHeight;})()")
    try:
        v = win.evaluate_js(js)
        v = str(v) if v is not None else ''
        if '|' not in v:
            return None, None
        a, b = v.split('|')[:2]
        return int(a), int(b)
    except Exception:
        return None, None

def fit_window(win, requested):
    # requested covers the whole window (title bar included) while the page only
    # sees the client area, so the card gets clipped and its bottom buttons stop
    # being clickable. Measure the real content height and grow the window to fit.
    content_h, inner_h = measure_card(win)
    if not content_h or inner_h is None:
        return
    chrome = max(0, requested - inner_h)
    want = content_h + chrome + FIT_MARGIN
    if want <= requested:
        return
    want = min(want, max(320, screen_height() - chrome - 16))
    try:
        win.resize(WINDOW_WIDTH, want)
    except Exception:
        pass

def resize_for_mode(win, mode):
    if not _state['alive'] or not win:
        return
    global _current_mode
    if mode == _current_mode:
        return
    h = MODE_HEIGHTS.get(mode, 500)
    try:
        win.resize(WINDOW_WIDTH, h)
        _current_mode = mode
    except Exception:
        return
    fit_window(win, h)

def break_phase(win):
    try:
        _break_end.clear()
        _break_started.clear()

        # Phase 1: Ready interface - [开始休息] [5分钟后提醒]
        bring_to_front(win, focus=False)
        eval_js(win, 'modeReady()')
        resize_for_mode(win, 'ready')
        t0 = time.time() + 1800
        while not _break_started.is_set() and not _break_end.is_set() and not _done.is_set() and _state['alive']:
            if time.time() > t0:
                break
            time.sleep(0.1)
        if _done.is_set() or not _state['alive']:
            return
        if _break_end.is_set():
            # User clicked "5分钟后提醒"
            snooze_s = 5 if TEST_MODE else 300
            _state['next_ts'] = time.time() + snooze_s
            write_state(_state['next_ts'])
            r = int(_state['next_ts'] - time.time())
            p = 1 - (r / interval_s) if interval_s > 0 else 0
            eval_js(win, 'modeTimer(' + str(r) + ',' + str(p) + ',' + json.dumps(fmt_time(_state['next_ts'])) + ')')
            resize_for_mode(win, 'timer')
            fit_window(win, MODE_HEIGHTS['timer'])
            return

        # Phase 2: Break countdown - [我已经休息好了]
        b0 = time.time()
        eval_js(win, 'modeBreak(' + str(break_sec) + ',0,' + json.dumps(reminder_text) + ')')
        resize_for_mode(win, 'break')
        last_shown = None
        while not _break_end.is_set() and not _done.is_set() and _state['alive']:
            e = time.time() - b0
            r = max(0, break_sec - e)
            ri = int(math.ceil(r)) if r > 0 else 0
            p = 1 - (r / break_sec) if break_sec > 0 else 1
            if ri != last_shown:
                last_shown = ri
                eval_js(win, 'setBreakCount(' + str(ri) + ',' + str(p) + ')')
            if r <= 0:
                time.sleep(0.3)
                break
            time.sleep(0.1)
        if TEST_MODE:
            _done.set()
            return
        if _state['alive']:
            _state['next_ts'] = next_reminder_ts(time.time())
            write_state(_state['next_ts'])
            r = int(_state['next_ts'] - time.time())
            p = 1 - (r / interval_s) if interval_s > 0 else 0
            eval_js(win, 'modeTimer(' + str(r) + ',' + str(p) + ',' + json.dumps(fmt_time(_state['next_ts'])) + ')')
        resize_for_mode(win, 'timer')
        fit_window(win, MODE_HEIGHTS['timer'])
    except Exception:
        # Even if the break phase fails it must reschedule, otherwise timer_loop
        # would spin on an overdue timestamp and freeze the countdown.
        try:
            if _state['alive'] and _state['next_ts'] <= time.time():
                _state['next_ts'] = next_reminder_ts(time.time())
                write_state(_state['next_ts'])
        except Exception:
            pass

def timer_loop(win):
    try:
        time.sleep(0.5)
        if TEST_MODE:
            _state['next_ts'] = time.time() + 3
        resize_for_mode(win, 'timer')
        r = int(_state['next_ts'] - time.time())
        p = 1 - (r / interval_s) if interval_s > 0 else 0
        eval_js(win, 'modeTimer(' + str(r) + ',' + str(p) + ',' + json.dumps(fmt_time(_state['next_ts'])) + ')')
        fit_window(win, MODE_HEIGHTS['timer'])
        while not _done.is_set() and _state['alive']:
            now = time.time()
            if now >= _state['next_ts']:
                break_phase(win)
                # guarantee forward progress if break_phase returned early
                if _state['alive'] and _state['next_ts'] <= time.time():
                    _state['next_ts'] = next_reminder_ts(time.time())
                    write_state(_state['next_ts'])
                time.sleep(0.2)
            else:
                r = int(_state['next_ts'] - now)
                p = 1 - (r / interval_s) if interval_s > 0 else 0
                eval_js(win, 'setTimerCount(' + str(r) + ',' + str(p) + ',' + json.dumps(fmt_time(_state['next_ts'])) + ')')
                time.sleep(1.0)
    except Exception:
        _state['alive'] = False

if __name__ == '__main__':
    srv = None if TEST_MODE else acquire_port()
    if srv is None and not TEST_MODE:
        # Another live instance owns the port: hand over to it instead of
        # opening a second window.
        if notify_running_instance():
            sys.exit(0)
        # Stale or foreign holder - start normally so the app is never lost.
        srv = acquire_port(retries=1, delay=0)

    def od():
        try:
            _break_end.set()
            if TEST_MODE: _done.set()
        except: pass

    def oz():
        try:
            _break_end.set()
            if TEST_MODE: _done.set()
        except: pass

    _reminder_api.set_callbacks(lambda: _break_started.set(), od, oz)
    try:
        win = webview.create_window(WINDOW_TITLE, url=os.path.join(_TEMP_DIR, 'main.html'), js_api=_reminder_api, width=440, height=500, resizable=False, on_top=True, easy_drag=False, text_select=False, confirm_close=False)
        win.events.closing += on_closing
        if srv is not None:
            threading.Thread(target=serve_show_requests, args=(srv, win), name='ipc', daemon=True).start()
        webview.start(func=lambda: timer_loop(win), debug=False, http_server=False)
    except Exception:
        _state['alive'] = False
