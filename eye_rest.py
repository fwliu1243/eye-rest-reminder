#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eye Rest Reminder - Apple Glassmorphism UI
"""

import webview, json, os, sys, socket, time, datetime, math, ctypes, ctypes.wintypes, threading, tempfile, re, shutil

HTML = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>护眼提醒</title>\n<style>\n@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\');\n*{margin:0;padding:0;box-sizing:border-box}\nhtml,body{height:100%}\nbody{\n  font-family:\'Inter\',-apple-system,\'Microsoft YaHei\',sans-serif;\n  height:100vh;overflow-y:auto;overflow-x:hidden;\n  display:flex;align-items:flex-start;justify-content:center;\n  user-select:none;\n  background:linear-gradient(160deg,rgba(15,12,41,0.85) 0%,rgba(26,26,62,0.7) 35%,rgba(36,36,62,0.65) 65%,rgba(13,13,26,0.85) 100%),url("WALLPAPER_PLACEHOLDER") center/cover no-repeat fixed;\n}\n.orb{position:fixed;border-radius:50%;filter:blur(100px);opacity:0.3;pointer-events:none}\n.orb-1{width:500px;height:500px;background:radial-gradient(circle,rgba(108,140,255,0.4),transparent 70%);top:-200px;right:-120px}\n.orb-2{width:450px;height:450px;background:radial-gradient(circle,rgba(167,139,250,0.3),transparent 70%);bottom:-180px;left:-100px}\n.orb-3{width:250px;height:250px;background:radial-gradient(circle,rgba(244,114,182,0.2),transparent 70%);top:30%;right:5%}\n.glass{\n  margin:auto;\n  width:400px;padding:36px 32px 32px;\n  background:rgba(255,255,255,0.04);\n  backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);\n  z-index:1;animation:fadeIn 0.7s cubic-bezier(0.16,1,0.3,1);\n  border:none;\n  border-radius:0 !important;\n}\n@keyframes fadeIn{from{opacity:0;transform:scale(0.9) translateY(24px)}to{opacity:1;transform:scale(1) translateY(0)}}\n.header{text-align:center;margin-bottom:24px}\n.icon-wrap{width:72px;height:72px;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;font-size:38px;background:rgba(255,255,255,0.06);animation:float 3s ease-in-out infinite;border:none}\n@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}\n.header h1{font-size:24px;font-weight:700;color:rgba(255,255,255,0.92);letter-spacing:-0.3px;margin-bottom:4px}\n.header .sub{font-size:13px;font-weight:400;color:rgba(255,255,255,0.4)}\n.ring-wrap{display:flex;justify-content:center;margin-bottom:24px}\n.ring-svg{position:relative;width:150px;height:150px;flex-shrink:0}\n.ring-svg svg{width:100%;height:100%;transform:rotate(-90deg)}\n.bg-ring{fill:none;stroke:rgba(255,255,255,0.05);stroke-width:6}\n.progress-ring{fill:none;stroke:url(#grad);stroke-width:6;stroke-linecap:round;stroke-dasharray:424;stroke-dashoffset:0;transition:stroke-dashoffset 0.5s cubic-bezier(0.4,0,0.2,1);filter:drop-shadow(0 0 8px rgba(108,140,255,0.3))}\n.ring-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}\n.ring-num{display:block;font-size:36px;font-weight:700;color:rgba(255,255,255,0.93);letter-spacing:-1px;line-height:1;font-variant-numeric:tabular-nums}\n.ring-unit{display:block;font-size:12px;font-weight:400;color:rgba(255,255,255,0.35);margin-top:2px;letter-spacing:2px;text-transform:uppercase}\n.info-box{background:rgba(255,255,255,0.03);padding:12px 16px;margin-bottom:24px;text-align:center}\n.info-box p{font-size:13px;line-height:1.6;color:rgba(255,255,255,0.65)}\n.info-box .hl{color:rgba(108,140,255,0.9);font-weight:600}\n.actions{display:flex;flex-direction:column;gap:10px}\n.btn{display:block;width:100%;padding:12px 0;overflow:hidden;font-family:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:all 0.2s;outline:none;position:relative;border:none;-webkit-appearance:none;background:linear-gradient(135deg,rgba(108,140,255,0.28) 0%,rgba(108,140,255,0.12) 40%,rgba(167,139,250,0.08) 100%);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);color:rgba(255,255,255,0.95);box-shadow:0 4px 20px rgba(108,140,255,0.15),inset 0 1px 0 rgba(255,255,255,0.25),inset 0 -1px 0 rgba(0,0,0,0.08)}\n.btn:hover{background:linear-gradient(135deg,rgba(108,140,255,0.38) 0%,rgba(108,140,255,0.18) 40%,rgba(167,139,250,0.12) 100%);box-shadow:0 8px 30px rgba(108,140,255,0.25),inset 0 1px 0 rgba(255,255,255,0.3);transform:translateY(-1px)}\n.btn:active{transform:scale(0.97)}\n.btn2{background:linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.02) 100%);color:rgba(255,255,255,0.5);font-size:13px;padding:10px 0;box-shadow:inset 0 1px 0 rgba(255,255,255,0.08)}\n.btn2:hover{background:linear-gradient(180deg,rgba(255,255,255,0.08) 0%,rgba(255,255,255,0.03) 100%);color:rgba(255,255,255,0.75)}\n.ripple{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.55) 0%,rgba(255,255,255,0.2) 55%,rgba(255,255,255,0) 72%);transform:scale(0);opacity:1;pointer-events:none;animation:ripple .62s cubic-bezier(.22,.61,.36,1) forwards}\n@keyframes ripple{to{transform:scale(2.6);opacity:0}}\nbody::-webkit-scrollbar{width:0;height:0}\n</style>\n</head>\n<body>\n<div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div>\n<svg width="0" height="0" style="position:absolute">\n  <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6c8cff"/><stop offset="100%" stop-color="#a78bfa"/></linearGradient></defs>\n</svg>\n<div class="glass">\n  <div class="header">\n    <div class="icon-wrap" id="iconMain">&#x23F0;</div>\n    <h1 id="titleMain">护眼倒计时</h1>\n    <p class="sub" id="subtitle">距下次休息还有</p>\n  </div>\n  <div class="ring-wrap">\n    <div class="ring-svg">\n      <svg viewBox="0 0 140 140">\n        <circle class="bg-ring" cx="70" cy="70" r="67.5"/>\n        <circle class="progress-ring" id="progress" cx="70" cy="70" r="67.5" stroke-dasharray="424" stroke-dashoffset="0"/>\n      </svg>\n      <div class="ring-text">\n        <span class="ring-num" id="timerNum">20:00</span>\n        <span class="ring-unit" id="timerUnit">分钟</span>\n      </div>\n    </div>\n  </div>\n  <div class="info-box" id="statusBox">\n    <p>下次休息时间：<span class="hl" id="nextTimeLabel">--:--</span></p>\n  </div>\n  <div class="info-box" id="readyBox" style="display:none">\n    <p>时间到了，点击下方按钮开始休息</p>\n  </div>\n  <div class="info-box" id="breakBox" style="display:none">\n    <p id="breakText">该休息眼睛了！</p>\n  </div>\n  <div class="actions">\n    <button class="btn" id="btnStart" style="display:none">开始休息</button>\n    <button class="btn" id="btnDismiss" style="display:none">我已经休息好了</button>\n    <button class="btn btn2" id="btnSnooze" style="display:none">5 分钟后提醒</button>\n  </div>\n</div>\n<script>\nfunction setTimerCount(s,p,t){var m=Math.floor(s/60),se=s%60;document.getElementById(\'timerNum\').textContent=(m<10?\'0\':\'\')+m+\':\'+(se<10?\'0\':\'\')+se;if(t){document.getElementById(\'nextTimeLabel\').textContent=t;}document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));}\nfunction setBreakCount(s,p){document.getElementById(\'timerNum\').textContent=String(s);document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));}\nvar C=424;\nfunction api(m,n){n=n||0;var f=null;try{f=(window.pywebview&&pywebview.api)?pywebview.api[m]:null;}catch(e){f=null}if(typeof f===\'function\'){try{var r=f();if(r&&typeof r.catch===\'function\'){r.catch(function(){});}return;}catch(e){}}if(n<40){setTimeout(function(){api(m,n+1);},120);}}\nfunction ripple(e,el){try{var r=el.getBoundingClientRect();var d=Math.max(r.width,r.height)*1.1;var x=(e&&typeof e.clientX===\'number\')?e.clientX:r.left+r.width/2;var y=(e&&typeof e.clientY===\'number\')?e.clientY:r.top+r.height/2;var s=document.createElement(\'span\');s.className=\'ripple\';s.style.width=s.style.height=d+\'px\';s.style.left=(x-r.left-d/2)+\'px\';s.style.top=(y-r.top-d/2)+\'px\';el.appendChild(s);setTimeout(function(){if(s.parentNode){s.parentNode.removeChild(s);}},640);}catch(err){}}\nfunction modeTimer(s,p,t){\n  document.getElementById(\'iconMain\').textContent=\'\\u23F0\';document.getElementById(\'titleMain\').textContent=\'护眼倒计时\';document.getElementById(\'subtitle\').textContent=\'距下次休息还有\';document.getElementById(\'statusBox\').style.display=\'block\';document.getElementById(\'readyBox\').style.display=\'none\';document.getElementById(\'breakBox\').style.display=\'none\';document.getElementById(\'btnStart\').style.display=\'none\';document.getElementById(\'btnDismiss\').style.display=\'none\';document.getElementById(\'btnSnooze\').style.display=\'none\';document.getElementById(\'nextTimeLabel\').textContent=t||\'--:--\';var m=Math.floor(s/60),se=s%60;document.getElementById(\'timerNum\').textContent=(m<10?\'0\':\'\')+m+\':\'+(se<10?\'0\':\'\')+se;document.getElementById(\'timerUnit\').textContent=\'\\u5206\\u949F\';document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));\n}\nfunction modeReady(){\n  document.getElementById(\'iconMain\').textContent=\'\\u{1F440}\';document.getElementById(\'titleMain\').textContent=\'\\u4F11\\u606F\\u65F6\\u95F4\\u5230\';document.getElementById(\'subtitle\').textContent=\'\\u8BE5\\u8BA9\\u773C\\u775B\\u4F11\\u606F\\u4E00\\u4E0B\\u4E86\';document.getElementById(\'statusBox\').style.display=\'none\';document.getElementById(\'readyBox\').style.display=\'block\';document.getElementById(\'breakBox\').style.display=\'none\';document.getElementById(\'btnStart\').style.display=\'block\';document.getElementById(\'btnDismiss\').style.display=\'none\';document.getElementById(\'btnSnooze\').style.display=\'block\';document.getElementById(\'timerNum\').textContent=\'0\';document.getElementById(\'timerUnit\').textContent=\'\\u79D2\';document.getElementById(\'progress\').style.strokeDashoffset=C;\n}\nfunction modeBreak(s,p,t){\n  document.getElementById(\'iconMain\').textContent=\'\\u{1F440}\';document.getElementById(\'titleMain\').textContent=\'\\u4F11\\u606F\\u4E00\\u4E0B\';document.getElementById(\'subtitle\').textContent=\'\\u8BA9\\u773C\\u775B\\u653E\\u677E\\u4E00\\u4E0B\\u5427\';document.getElementById(\'statusBox\').style.display=\'none\';document.getElementById(\'readyBox\').style.display=\'none\';document.getElementById(\'breakBox\').style.display=\'block\';document.getElementById(\'btnStart\').style.display=\'none\';document.getElementById(\'btnDismiss\').style.display=\'block\';document.getElementById(\'btnSnooze\').style.display=\'none\';document.getElementById(\'breakText\').innerHTML=t.replace(/\\n/g,\'<br>\');document.getElementById(\'timerNum\').textContent=String(s);document.getElementById(\'timerUnit\').textContent=\'\\u79D2\';document.getElementById(\'progress\').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)));\n}\ndocument.getElementById(\'btnStart\').addEventListener(\'click\',function(e){ripple(e,this);api(\'startBreak\');});\ndocument.getElementById(\'btnDismiss\').addEventListener(\'click\',function(e){ripple(e,this);api(\'dismiss\');});\ndocument.getElementById(\'btnSnooze\').addEventListener(\'click\',function(e){ripple(e,this);api(\'snooze\');});\n</script>\n</body>\n</html>'


# Liquid glass UI (kept self-contained so the reminder still works offline).
HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="dark">
<title>护眼提醒</title>
<style>
:root{
  --ink:#f8fbff;
  --muted:rgba(235,244,255,.58);
  --faint:rgba(235,244,255,.34);
  --accent:#9bd8ff;
  --accent-2:#b9a7ff;
  --accent-rgb:155,216,255;
  --glass-top:rgba(255,255,255,.20);
  --glass-bottom:rgba(255,255,255,.075);
  --ease-out:cubic-bezier(.16,1,.3,1);
}
*{box-sizing:border-box}
html,body{width:100%;min-height:100%;margin:0}
body{
  position:relative;overflow:hidden;
  display:grid;place-items:center;
  min-height:100vh;padding:18px;
  font-family:"Segoe UI Variable Text","Segoe UI","Microsoft YaHei UI",sans-serif;
  color:var(--ink);user-select:none;
  background:
    linear-gradient(145deg,rgba(4,11,28,.74),rgba(13,18,45,.58) 48%,rgba(5,10,24,.76)),
    url("WALLPAPER_PLACEHOLDER") center/cover no-repeat fixed;
  isolation:isolate;
}
button{font:inherit}
.atmosphere,.atmosphere::before,.atmosphere::after,.grain,.rays{position:fixed;inset:-25%;pointer-events:none}
.atmosphere{z-index:-3;filter:saturate(115%);transition:filter 1s ease}
.atmosphere::before,.atmosphere::after{content:"";border-radius:44%;will-change:transform,background}
.atmosphere::before{
  background:
    radial-gradient(circle at 26% 35%,rgba(79,172,254,.76) 0 8%,transparent 31%),
    radial-gradient(circle at 70% 28%,rgba(186,118,255,.62) 0 9%,transparent 33%),
    radial-gradient(circle at 58% 78%,rgba(52,225,197,.45) 0 9%,transparent 32%);
  filter:blur(34px);animation:auroraA 19s ease-in-out infinite alternate;
}
.atmosphere::after{
  inset:-15%;opacity:.55;
  background:conic-gradient(from 110deg at 55% 45%,transparent,#668cff 16%,transparent 34%,#ef8dff 51%,transparent 69%,#55e6d0 83%,transparent);
  filter:blur(62px);animation:auroraB 25s linear infinite;
}
.rays{z-index:-2;inset:0;opacity:.20;background:repeating-linear-gradient(115deg,transparent 0 44px,rgba(255,255,255,.05) 45px,transparent 47px 92px);mask-image:linear-gradient(to bottom,black,transparent 72%);animation:rays 13s ease-in-out infinite alternate}
.grain{z-index:-1;inset:0;opacity:.075;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.88' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.68'/%3E%3C/svg%3E");mix-blend-mode:soft-light}
.float-shape{position:fixed;z-index:-1;pointer-events:none;border:1px solid rgba(255,255,255,.16);background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.02));box-shadow:inset 0 1px 1px rgba(255,255,255,.18),0 20px 60px rgba(0,0,0,.12);backdrop-filter:blur(7px);will-change:transform}
.shape-a{width:100px;height:100px;left:-35px;top:11%;border-radius:34% 66% 56% 44%/46% 40% 60% 54%;animation:driftA 14s ease-in-out infinite alternate}
.shape-b{width:76px;height:76px;right:-24px;bottom:13%;border-radius:50%;animation:driftB 12s ease-in-out infinite alternate}
.shape-c{width:28px;height:28px;right:13%;top:8%;border-radius:50%;background:rgba(255,255,255,.16);animation:driftB 9s -3s ease-in-out infinite alternate}

.shell{width:min(386px,calc(100vw - 28px));perspective:900px}
.glass{
  position:relative;overflow:hidden;
  width:100%;padding:18px 22px 22px;
  border:1px solid rgba(255,255,255,.26);border-radius:34px;
  background:linear-gradient(145deg,var(--glass-top),var(--glass-bottom) 54%,rgba(255,255,255,.045));
  box-shadow:0 32px 80px rgba(0,0,0,.32),0 8px 28px rgba(0,0,0,.14),inset 0 1px 0 rgba(255,255,255,.42),inset 0 -1px 0 rgba(255,255,255,.08);
  backdrop-filter:blur(36px) saturate(160%);-webkit-backdrop-filter:blur(36px) saturate(160%);
  transform-style:preserve-3d;
  animation:cardIn .8s var(--ease-out) both;
}
.glass::before{
  content:"";position:absolute;left:7%;right:7%;top:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.84),transparent);
  opacity:.72;pointer-events:none;
}
.glass::after{
  content:"";position:absolute;width:190px;height:190px;left:var(--shine-x,70%);top:var(--shine-y,-30%);
  transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,rgba(255,255,255,.16),transparent 67%);mix-blend-mode:screen;transition:left .2s ease-out,top .2s ease-out;
}
.topbar{height:34px;display:flex;align-items:center;justify-content:space-between;position:relative;z-index:2}
.brand{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:650;letter-spacing:1.7px;text-transform:uppercase;color:rgba(255,255,255,.62)}
.brand-dot{width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px rgba(var(--accent-rgb),.11),0 0 15px rgba(var(--accent-rgb),.7);transition:.8s ease}
.scene-btn{display:flex;align-items:center;gap:6px;height:30px;padding:0 10px;border:1px solid rgba(255,255,255,.14);border-radius:99px;color:rgba(255,255,255,.68);background:rgba(255,255,255,.075);cursor:pointer;outline:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.13);transition:.25s var(--ease-out)}
.scene-btn svg{width:13px;height:13px}.scene-btn span{font-size:11px}
.scene-btn:hover{color:white;background:rgba(255,255,255,.13);transform:translateY(-1px)}
.scene-btn:active{transform:scale(.93)}

.header{text-align:center;margin-top:8px}
.eye-orb{position:relative;width:64px;height:64px;margin:0 auto 12px;display:grid;place-items:center;border:1px solid rgba(255,255,255,.24);border-radius:23px;background:linear-gradient(145deg,rgba(255,255,255,.22),rgba(255,255,255,.055));box-shadow:0 16px 36px rgba(0,0,0,.18),inset 0 1px 0 rgba(255,255,255,.36);animation:float 4s ease-in-out infinite}
.eye-orb::before{content:"";position:absolute;inset:7px;border-radius:17px;background:radial-gradient(circle at 34% 24%,rgba(255,255,255,.19),transparent 45%)}
.eye-icon{position:relative;width:35px;height:35px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.18))}
.eye-outline{fill:none;stroke:rgba(255,255,255,.92);stroke-width:1.8}
.eye-pupil{fill:var(--accent);transform-origin:center;transition:fill .8s ease;animation:look 6s ease-in-out infinite}
.header h1{margin:0;font-size:23px;line-height:1.25;font-weight:680;letter-spacing:-.7px;text-shadow:0 2px 16px rgba(0,0,0,.14)}
.sub{margin:6px 0 0;font-size:12.5px;line-height:1.5;color:var(--muted);letter-spacing:.2px}

.ring-wrap{display:grid;place-items:center;margin:16px 0 14px}
.ring-svg{position:relative;width:148px;height:148px;filter:drop-shadow(0 15px 28px rgba(0,0,0,.13))}
.ring-svg::before{content:"";position:absolute;inset:13px;border:1px solid rgba(255,255,255,.12);border-radius:50%;background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.025));box-shadow:inset 8px 8px 24px rgba(255,255,255,.025),inset -8px -8px 28px rgba(0,0,0,.1)}
.ring-svg svg{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg);overflow:visible}
.bg-ring{fill:none;stroke:rgba(255,255,255,.09);stroke-width:5}
.progress-ring{fill:none;stroke:url(#grad);stroke-width:5;stroke-linecap:round;stroke-dasharray:424;stroke-dashoffset:0;transition:stroke-dashoffset .55s cubic-bezier(.4,0,.2,1);filter:drop-shadow(0 0 7px rgba(var(--accent-rgb),.64))}
.ring-text{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.ring-num{display:block;font-size:34px;line-height:1;font-weight:680;letter-spacing:-1.5px;font-variant-numeric:tabular-nums;text-shadow:0 4px 18px rgba(0,0,0,.19)}
.ring-unit{display:block;margin-top:6px;font-size:10px;font-weight:600;letter-spacing:2.4px;text-transform:uppercase;color:var(--faint)}
.pulse{position:absolute;right:17px;top:21px;width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 rgba(var(--accent-rgb),.5);animation:pulse 2.2s infinite}

.info-box{position:relative;margin:0 0 14px;padding:12px 14px;border:1px solid rgba(255,255,255,.11);border-radius:17px;background:linear-gradient(135deg,rgba(255,255,255,.095),rgba(255,255,255,.035));box-shadow:inset 0 1px 0 rgba(255,255,255,.10);text-align:center;animation:softIn .45s var(--ease-out) both}
.info-box p{margin:0;font-size:12.5px;line-height:1.65;color:rgba(244,248,255,.66)}
.info-box .hl{color:var(--accent);font-weight:650;text-shadow:0 0 15px rgba(var(--accent-rgb),.35)}
.tip{display:flex;align-items:center;justify-content:center;gap:7px}.tip svg{width:14px;height:14px;color:var(--accent);flex:none}
.actions{display:flex;flex-direction:column;gap:9px}
.btn{position:relative;isolation:isolate;overflow:hidden;width:100%;min-height:44px;padding:11px 16px;border:1px solid rgba(255,255,255,.24);border-radius:16px;outline:none;cursor:pointer;color:#f8fcff;font-size:14px;font-weight:650;letter-spacing:.15px;background:linear-gradient(135deg,rgba(var(--accent-rgb),.44),rgba(149,125,255,.25));box-shadow:0 10px 26px rgba(30,55,120,.2),inset 0 1px 0 rgba(255,255,255,.38),inset 0 -1px 0 rgba(0,0,0,.08);transition:transform .3s var(--ease-out),box-shadow .3s ease,filter .3s ease}
.btn::before{content:"";position:absolute;z-index:-1;inset:-2px;background:linear-gradient(105deg,transparent 25%,rgba(255,255,255,.28) 43%,transparent 59%);transform:translateX(-110%);transition:transform .65s ease}
.btn:hover{transform:translateY(-2px) scale(1.01);box-shadow:0 15px 34px rgba(30,55,120,.28),inset 0 1px 0 rgba(255,255,255,.45);filter:brightness(1.08)}
.btn:hover::before{transform:translateX(110%)}
.btn:active{transform:translateY(1px) scale(.96);transition-duration:.1s}
.btn2{min-height:38px;border-color:rgba(255,255,255,.11);color:rgba(255,255,255,.62);font-size:12px;background:rgba(255,255,255,.045);box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.btn2:hover{color:white;background:rgba(255,255,255,.09);box-shadow:0 10px 24px rgba(0,0,0,.10),inset 0 1px 0 rgba(255,255,255,.12)}
.ripple{position:absolute;z-index:3;border-radius:50%;pointer-events:none;background:radial-gradient(circle,rgba(255,255,255,.7),rgba(255,255,255,.22) 42%,transparent 70%);transform:scale(0);animation:ripple .68s ease-out forwards}
.mode-pop{animation:modePop .52s var(--ease-out)}

body[data-scene="dusk"]{--accent:#ffbdc9;--accent-2:#ffc78c;--accent-rgb:255,189,201}
body[data-scene="dusk"] .atmosphere::before{background:radial-gradient(circle at 22% 26%,rgba(255,130,156,.71),transparent 31%),radial-gradient(circle at 76% 39%,rgba(255,177,91,.60),transparent 31%),radial-gradient(circle at 42% 83%,rgba(122,81,255,.52),transparent 34%)}
body[data-scene="forest"]{--accent:#8fffd1;--accent-2:#83cfff;--accent-rgb:143,255,209}
body[data-scene="forest"] .atmosphere::before{background:radial-gradient(circle at 23% 31%,rgba(36,211,165,.68),transparent 31%),radial-gradient(circle at 77% 35%,rgba(42,133,226,.56),transparent 33%),radial-gradient(circle at 52% 84%,rgba(165,235,113,.42),transparent 32%)}
body[data-scene="berry"]{--accent:#e1b4ff;--accent-2:#ff93c4;--accent-rgb:225,180,255}
body[data-scene="berry"] .atmosphere::before{background:radial-gradient(circle at 20% 35%,rgba(166,89,255,.70),transparent 31%),radial-gradient(circle at 78% 25%,rgba(255,91,164,.56),transparent 32%),radial-gradient(circle at 54% 82%,rgba(82,136,255,.46),transparent 34%)}

@keyframes cardIn{from{opacity:0;transform:translateY(24px) scale(.94) rotateX(4deg)}to{opacity:1;transform:none}}
@keyframes softIn{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
@keyframes modePop{0%{opacity:.45;transform:scale(.96) translateY(5px)}100%{opacity:1;transform:none}}
@keyframes float{0%,100%{transform:translateY(0) rotate(-1deg)}50%{transform:translateY(-5px) rotate(1deg)}}
@keyframes look{0%,38%,100%{transform:translateX(0)}44%,58%{transform:translateX(3px)}64%,78%{transform:translateX(-3px)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(var(--accent-rgb),.55)}70%{box-shadow:0 0 0 8px rgba(var(--accent-rgb),0)}100%{box-shadow:0 0 0 0 rgba(var(--accent-rgb),0)}}
@keyframes ripple{to{transform:scale(2.7);opacity:0}}
@keyframes auroraA{0%{transform:translate3d(-5%,-4%,0) rotate(-8deg) scale(1)}50%{transform:translate3d(5%,3%,0) rotate(4deg) scale(1.08)}100%{transform:translate3d(-1%,8%,0) rotate(10deg) scale(.98)}}
@keyframes auroraB{to{transform:rotate(360deg) scale(1.08)}}
@keyframes rays{to{transform:translateX(45px);opacity:.3}}
@keyframes driftA{to{transform:translate(42px,58px) rotate(46deg)}}
@keyframes driftB{to{transform:translate(-33px,-52px) rotate(-34deg)}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important}}
body::-webkit-scrollbar{display:none}
</style>
</head>
<body data-scene="ocean">
  <div class="atmosphere"></div><div class="rays"></div><div class="grain"></div>
  <div class="float-shape shape-a"></div><div class="float-shape shape-b"></div><div class="float-shape shape-c"></div>
  <svg width="0" height="0" aria-hidden="true"><defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="var(--accent)"/><stop offset="100%" stop-color="var(--accent-2)"/></linearGradient></defs></svg>
  <main class="shell">
    <section class="glass" id="glassCard">
      <div class="topbar">
        <div class="brand"><i class="brand-dot"></i><span>Focus Care</span></div>
        <button class="scene-btn" id="sceneBtn" type="button" title="切换氛围背景" aria-label="切换氛围背景">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3a9 9 0 1 0 9 9c0-1.1-.9-2-2-2h-1.4a2 2 0 0 1-1.8-2.9l.5-1A2.1 2.1 0 0 0 14.4 3H12Z"/><circle cx="7.5" cy="10.5" r="1" fill="currentColor" stroke="none"/><circle cx="10" cy="6.8" r="1" fill="currentColor" stroke="none"/><circle cx="7.7" cy="15" r="1" fill="currentColor" stroke="none"/></svg>
          <span id="sceneLabel">海雾</span>
        </button>
      </div>
      <header class="header" id="modeHeader">
        <div class="eye-orb">
          <svg class="eye-icon" viewBox="0 0 48 48" aria-hidden="true"><path class="eye-outline" d="M4.5 24s7.2-11 19.5-11 19.5 11 19.5 11S36.3 35 24 35 4.5 24 4.5 24Z"/><circle class="eye-outline" cx="24" cy="24" r="7.4"/><circle class="eye-pupil" cx="24" cy="24" r="3.4"/></svg>
        </div>
        <h1 id="titleMain">护眼倒计时</h1>
        <p class="sub" id="subtitle">专注一会儿，也别忘了看看远方</p>
      </header>
      <div class="ring-wrap" id="ringWrap">
        <div class="ring-svg">
          <svg viewBox="0 0 148 148" aria-hidden="true"><circle class="bg-ring" cx="74" cy="74" r="67.5"/><circle class="progress-ring" id="progress" cx="74" cy="74" r="67.5"/></svg>
          <div class="pulse"></div>
          <div class="ring-text"><span class="ring-num" id="timerNum">20:00</span><span class="ring-unit" id="timerUnit">分钟</span></div>
        </div>
      </div>
      <div class="info-box" id="statusBox"><p class="tip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg><span>下一次休息 <strong class="hl" id="nextTimeLabel">--:--</strong></span></p></div>
      <div class="info-box" id="readyBox" hidden><p>时间到了，眺望远处，让眼睛松一口气。</p></div>
      <div class="info-box" id="breakBox" hidden><p id="breakText">看看远处，慢慢眨眼。</p></div>
      <div class="actions">
        <button class="btn" id="btnStart" type="button" hidden>开始 20 秒休息</button>
        <button class="btn" id="btnDismiss" type="button" hidden>我已经休息好了</button>
        <button class="btn btn2" id="btnSnooze" type="button" hidden>5 分钟后提醒我</button>
      </div>
    </section>
  </main>
<script>
var C=424.12;
var scenes=[['ocean','海雾'],['dusk','晚霞'],['forest','森屿'],['berry','星莓']];
var sceneIndex=0;
function byId(id){return document.getElementById(id)}
function show(id,yes){byId(id).hidden=!yes}
function setProgress(p){byId('progress').style.strokeDashoffset=C*(1-Math.max(0,Math.min(1,p)))}
function formatClock(s){var m=Math.floor(s/60),se=s%60;return (m<10?'0':'')+m+':'+(se<10?'0':'')+se}
function animateMode(){var ids=['modeHeader','ringWrap'];ids.forEach(function(id){var el=byId(id);el.classList.remove('mode-pop');void el.offsetWidth;el.classList.add('mode-pop')})}
function setTimerCount(s,p,t){byId('timerNum').textContent=formatClock(s);if(t){byId('nextTimeLabel').textContent=t}setProgress(p)}
function setBreakCount(s,p){byId('timerNum').textContent=String(s);setProgress(p)}
function api(m,n){n=n||0;var f=null;try{f=(window.pywebview&&pywebview.api)?pywebview.api[m]:null}catch(e){}if(typeof f==='function'){try{var r=f();if(r&&typeof r.catch==='function')r.catch(function(){});return}catch(e){}}if(n<40)setTimeout(function(){api(m,n+1)},120)}
function ripple(e,el){var r=el.getBoundingClientRect(),d=Math.max(r.width,r.height)*1.15,x=e&&typeof e.clientX==='number'?e.clientX:r.left+r.width/2,y=e&&typeof e.clientY==='number'?e.clientY:r.top+r.height/2,s=document.createElement('span');s.className='ripple';s.style.width=s.style.height=d+'px';s.style.left=(x-r.left-d/2)+'px';s.style.top=(y-r.top-d/2)+'px';el.appendChild(s);setTimeout(function(){s.remove()},700)}
function modeTimer(s,p,t){byId('titleMain').textContent='护眼倒计时';byId('subtitle').textContent='专注一会儿，也别忘了看看远方';show('statusBox',true);show('readyBox',false);show('breakBox',false);show('btnStart',false);show('btnDismiss',false);show('btnSnooze',false);byId('nextTimeLabel').textContent=t||'--:--';byId('timerNum').textContent=formatClock(s);byId('timerUnit').textContent='分钟';setProgress(p);animateMode()}
function modeReady(){byId('titleMain').textContent='该让眼睛休息了';byId('subtitle').textContent='抬头看向 6 米之外，轻轻眨眼';show('statusBox',false);show('readyBox',true);show('breakBox',false);show('btnStart',true);show('btnDismiss',false);show('btnSnooze',true);byId('timerNum').textContent='20';byId('timerUnit').textContent='秒';setProgress(0);animateMode()}
function modeBreak(s,p,t){byId('titleMain').textContent='正在放松双眼';byId('subtitle').textContent='呼吸放慢一点，让视线自然舒展';show('statusBox',false);show('readyBox',false);show('breakBox',true);show('btnStart',false);show('btnDismiss',true);show('btnSnooze',false);byId('breakText').innerHTML=String(t).replace(/\n/g,'<br>');byId('timerNum').textContent=String(s);byId('timerUnit').textContent='秒';setProgress(p);animateMode()}
function nextScene(){sceneIndex=(sceneIndex+1)%scenes.length;document.body.dataset.scene=scenes[sceneIndex][0];byId('sceneLabel').textContent=scenes[sceneIndex][1];try{localStorage.setItem('eye-scene',String(sceneIndex))}catch(e){}}
try{var saved=parseInt(localStorage.getItem('eye-scene')||'0',10);if(saved>=0&&saved<scenes.length){sceneIndex=saved;document.body.dataset.scene=scenes[saved][0];byId('sceneLabel').textContent=scenes[saved][1]}}catch(e){}
byId('sceneBtn').addEventListener('click',function(e){ripple(e,this);nextScene()});
[['btnStart','startBreak'],['btnDismiss','dismiss'],['btnSnooze','snooze']].forEach(function(x){byId(x[0]).addEventListener('click',function(e){ripple(e,this);api(x[1])})});
var card=byId('glassCard');card.addEventListener('pointermove',function(e){var r=card.getBoundingClientRect();card.style.setProperty('--shine-x',((e.clientX-r.left)/r.width*100)+'%');card.style.setProperty('--shine-y',((e.clientY-r.top)/r.height*100)+'%')});
card.addEventListener('pointerleave',function(){card.style.setProperty('--shine-x','70%');card.style.setProperty('--shine-y','-30%')});
</script>
</body>
</html>'''

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
# Keep the state file truthful from the start; it is only rewritten when the
# schedule actually changes, so a stale value would mislead any diagnosis.
write_state(next_ts)
_reminder_api = ReminderApi()
_done = threading.Event()
_break_end = threading.Event()
_break_started = threading.Event()
_state = {'next_ts': next_ts, 'alive': True, 'user_hidden': False}

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

class _MONITORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.wintypes.DWORD),
                ('rcMonitor', ctypes.wintypes.RECT),
                ('rcWork', ctypes.wintypes.RECT),
                ('dwFlags', ctypes.wintypes.DWORD)]

SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_SHOWWINDOW = 0x0040
MONITOR_DEFAULTTONEAREST = 2
OFFSCREEN_MARGIN = 40

def _window_rect(hwnd):
    try:
        u32 = ctypes.windll.user32
        u32.GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
        u32.GetWindowRect.restype = ctypes.wintypes.BOOL
        r = ctypes.wintypes.RECT()
        if u32.GetWindowRect(hwnd, ctypes.byref(r)):
            return r
    except Exception:
        pass
    return None

def _virtual_screen():
    # Bounds covering every monitor, in physical pixels.
    try:
        u32 = ctypes.windll.user32
        x, y = u32.GetSystemMetrics(76), u32.GetSystemMetrics(77)
        w, h = u32.GetSystemMetrics(78), u32.GetSystemMetrics(79)
        if w > 0 and h > 0:
            return x, y, x + w, y + h
    except Exception:
        pass
    return 0, 0, 1920, 1080

def _work_area(hwnd):
    # Work area (screen minus taskbar) of the monitor nearest to hwnd.
    try:
        u32 = ctypes.windll.user32
        u32.MonitorFromWindow.restype = ctypes.c_void_p
        u32.MonitorFromWindow.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.DWORD]
        u32.GetMonitorInfoW.argtypes = [ctypes.c_void_p, ctypes.POINTER(_MONITORINFO)]
        mon = u32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
        info = _MONITORINFO()
        info.cbSize = ctypes.sizeof(_MONITORINFO)
        if mon and u32.GetMonitorInfoW(mon, ctypes.byref(info)):
            a = info.rcWork
            if a.right > a.left and a.bottom > a.top:
                return a.left, a.top, a.right, a.bottom
    except Exception:
        pass
    return _virtual_screen()

def window_off_screen(hwnd):
    # A hidden WinForms window is parked far outside the desktop at
    # (-32000,-32000), and resize() keeps whatever location the window already
    # has, so that parked coordinate gets written into its normal position.
    # Show() then only makes the window visible off-screen: the reminder stays
    # invisible and the phase loops wait for a click that can never happen.
    if not hwnd:
        return True
    r = _window_rect(hwnd)
    if r is None:
        return False
    left, top, right, bottom = _virtual_screen()
    return not (r.right > left + OFFSCREEN_MARGIN and r.left < right - OFFSCREEN_MARGIN and
                r.bottom > top + OFFSCREEN_MARGIN and r.top < bottom - OFFSCREEN_MARGIN)

def ensure_on_screen(hwnd):
    # Pull a parked window back to a visible spot on its own monitor.
    # A window the user closed on purpose stays closed: dragging it back would
    # undo the close-to-background behaviour, so only re-place windows we are
    # showing ourselves.
    if _state.get('user_hidden'):
        return
    if not hwnd or not window_off_screen(hwnd):
        return
    r = _window_rect(hwnd)
    if r is None:
        return
    w, h = r.right - r.left, r.bottom - r.top
    left, top, right, bottom = _work_area(hwnd)
    x = left + max(0, (right - left - w) // 2)
    y = top + max(0, (bottom - top - h) // 3)
    try:
        u32 = ctypes.windll.user32
        u32.SetWindowPos.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.HWND,
                                     ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                     ctypes.c_int, ctypes.wintypes.UINT]
        u32.SetWindowPos.restype = ctypes.wintypes.BOOL
        u32.SetWindowPos(hwnd, None, x, y, 0, 0,
                         SWP_NOSIZE | SWP_NOZORDER | SWP_SHOWWINDOW)
    except Exception:
        pass

def guard_window():
    # Phase loops can idle for many minutes, and a standby cycle in between
    # parks the window again, so re-check placement periodically.
    try:
        ensure_on_screen(find_hwnd())
    except Exception:
        pass

def window_needs_restore(hwnd):
    if not hwnd:
        return True
    try:
        u32 = ctypes.windll.user32
        u32.IsWindowVisible.restype = ctypes.wintypes.BOOL
        u32.IsIconic.restype = ctypes.wintypes.BOOL
        if (not u32.IsWindowVisible(hwnd)) or bool(u32.IsIconic(hwnd)):
            return True
    except Exception:
        return True
    # An off-screen window still reports as visible, so it takes the same path.
    return window_off_screen(hwnd)

def bring_to_front(win, focus=True):
    # Only touch the window when it is actually hidden or minimised. Resizing or
    # re-activating an already visible window would move it under the cursor and
    # can turn a stray mouse event into an unintended button click.
    if not _state['alive'] or not win:
        return
    global _current_mode
    # Showing on purpose (a reminder firing, or the desktop shortcut) overrides
    # an earlier user-initiated hide.
    _state['user_hidden'] = False
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
    # resize() re-pins whatever location the window had, so a parked window ends
    # up off-screen again right after being shown. Correct it last.
    ensure_on_screen(hwnd)
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
        _state['user_hidden'] = True
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
# Ready adds two actions below the message, so it needs considerably more
# vertical room than the timer card. fit_window() will still clamp these values
# for smaller screens.
MODE_HEIGHTS = {'timer': 540, 'ready': 630, 'break': 720}
FIT_MARGIN = 8
_current_mode = 'timer'

def screen_height():
    try:
        return int(ctypes.windll.user32.GetSystemMetrics(1))
    except Exception:
        return 1080

def measure_card(win):
    js = ("(function(){var g=document.querySelector('.glass');"
          "if(!g){return ''}var s=getComputedStyle(document.body);"
          "var py=(parseFloat(s.paddingTop)||0)+(parseFloat(s.paddingBottom)||0);"
          "return Math.ceil(g.offsetHeight+py)+'|'+window.innerHeight;})()")
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
        ensure_on_screen(find_hwnd())
        return
    h = MODE_HEIGHTS.get(mode, 500)
    try:
        win.resize(WINDOW_WIDTH, h)
        _current_mode = mode
    except Exception:
        pass
    else:
        fit_window(win, h)
    ensure_on_screen(find_hwnd())

def break_phase(win):
    try:
        _break_end.clear()
        _break_started.clear()

        # Phase 1: Ready interface - [开始休息] [5分钟后提醒]
        bring_to_front(win, focus=False)
        eval_js(win, 'modeReady()')
        resize_for_mode(win, 'ready')
        t0 = time.time() + 1800
        g0 = time.time()
        while not _break_started.is_set() and not _break_end.is_set() and not _done.is_set() and _state['alive']:
            if time.time() > t0:
                break
            if time.time() - g0 > 2:
                g0 = time.time()
                guard_window()
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
        g1 = time.time()
        while not _break_end.is_set() and not _done.is_set() and _state['alive']:
            if time.time() - g1 > 2:
                g1 = time.time()
                guard_window()
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
