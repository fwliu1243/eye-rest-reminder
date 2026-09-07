# 👁️ 护眼提醒 (Eye Rest Reminder)

一个轻量的 Windows 桌面护眼提醒小工具，基于 **20-20-20 法则**，每 20 分钟提醒你休息眼睛。

采用 **Liquid Glass** 液态玻璃视觉风格，融合桌面壁纸、动态极光与细腻光影。

## 特性

- 🕐 每 20 分钟弹出置顶提醒窗口，遵循 20-20-20 法则
- 🪟 **Liquid Glass** 液态玻璃 UI，桌面壁纸与动态极光融合
- ⏱ 20 秒休息倒计时，可随时提前结束休息
- ⏰ **5 分钟后提醒** — 推迟到下次提醒
- 🔒 单实例运行，重复启动不新开进程，而是把已有窗口唤回前台
- 🫥 关闭窗口不退出程序，转入后台继续计时，到点自动浮出
- 🛡 窗口离屏自动纠偏，睡眠唤醒后提醒依然可见
- 🌈 海雾、晚霞、森屿、星莓 4 套动态氛围，一键切换并记忆选择
- 💧 按钮带悬浮流光、弹性按压和水波纹反馈
- ✨ 漂浮玻璃体、呼吸光点和指针高光跟随，支持系统“减少动态效果”设置
- 📝 间隔、休息时长、提示文案均可配置
- 🚀 开机自启（注册表 HKCU Run，无需管理员权限）
- ⏫ 计时基于开机时间，睡眠/挂起不影响节奏

## 快速开始

### 1. 下载

```bash
git clone https://github.com/fwliu1243/eye-rest-reminder.git
cd eye-rest-reminder
```

### 2. 启动（需安装 Python 3 + pywebview）

```powershell
# 安装依赖
pip install pywebview

# 静默后台运行（无控制台窗口）
pythonw.exe eye_rest.py

# 测试弹窗
python eye_rest.py --test
```

### 3. 开机自启

```powershell
# 添加自启（替换路径为实际路径）
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" \
  -Name "EyeRestReminder" \
  -Value '"C:\path\to\pythonw.exe" "C:\path\to\eye_rest.py"'

# 取消自启
Remove-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name EyeRestReminder
```

## 配置

首次运行后在同目录生成 eye_rest_config.json：

```json
{
  "interval_min": 20,
  "break_sec": 20,
  "text": "该休息眼睛了！\n\n看看远处 20 英尺（约 6 米）以外的物体\n至少 20 秒，让睫状肌放松\n\n（20-20-20 法则）"
}
```

| 字段 | 默认 | 说明 |
|------|------|------|
| interval_min | 20 | 提醒间隔（分钟） |
| break_sec | 20 | 倒计时秒数 |
| text | 默认文案 | 提醒窗口正文 |

配置文件由人工编辑，因此所有取值都会被校验并钳制到安全区间，写错不会让程序崩溃：

| 字段 | 合法区间 | 越界/非法时的处理 |
|------|----------|-------------------|
| interval_min | 1 ~ 1440 | 钳制到区间内；无法解析（字符串/null）则回退默认 20 |
| break_sec | 1 ~ 600 | 同上 |
| text | 最长 600 字符 | 非字符串或空白回退默认文案，超长部分截断 |

> `interval_min` 为 0 或负数会让提醒永久处于「已逾期」状态，计时循环将空转并卡死倒计时，
> 因此下限被强制为 1 分钟。文件以 `utf-8-sig` 读取，用记事本或
> `Set-Content -Encoding UTF8` 保存（带 BOM）也能正常识别。

## 工作原理

- **计时基准**：使用 GetTickCount64() 获取系统开机时刻，提醒节点 = 开机时刻 + N × 间隔
- **轮询检查**：每 1 秒检查一次是否到达节点，到达即弹出窗口
- **离屏纠偏**：Windows 隐藏窗口时会把它停放到屏幕外的 `(-32000,-32000)`，
  而 pywebview 的 `resize()` 会沿用窗口当前坐标，导致该停放坐标被写死成
  「正常位置」——此后 `Show()` 只能让窗口在屏幕外可见，提醒永久看不见。
  `window_off_screen()` 以虚拟屏幕边界判定离屏，`ensure_on_screen()` 用
  `SetWindowPos` 把窗口搬回就近显示器工作区（尺寸不变）。用户主动关闭的窗口
  由 `user_hidden` 标记保护，守护不会把它强行拽回
- **单实例**：通过本地端口（28940）绑定检测；重复启动时向已运行实例发送
  `SHOW` 指令，由其把窗口从隐藏/最小化状态还原到前台，随后立即退出
- **关闭窗口**：拦截 `closing` 事件，只隐藏窗口不退出进程；到点提醒时会自动重新浮出
- **阶段循环守护**：Ready 阶段最长空转 30 分钟，期间若发生睡眠唤醒窗口会被再次
  停放，故两个阶段循环每 2 秒复检一次窗口位置
- **窗口高度自适应**：`MODE_HEIGHTS` 给的是整窗高度，页面却只拿得到客户区高度
  （差值约 39px 标题栏），卡片被 `overflow:hidden` 裁掉后底部按钮点不到。
  现在渲染后实测卡片高度并补偿 chrome，同时限制在屏幕高度内
- **界面**：基于 **pywebview**（WebView2 / Edge Chromium）+ HTML/CSS，三个模式切换：
  - Timer — 距下次休息倒计时
  - Ready — 显示「开始休息」和「5 分钟后提醒」
  - Break — 20 秒休息倒计时 + 「我已经休息好了」

休息倒计时只在秒数变化时刷新一次（而非每 100ms 全量重绘），避免 `evaluate_js`
的同步往返占满 UI 线程、导致点击事件无法投递。

## 目录结构

```
eye_rest.py            # 主程序（Python + pywebview + HTML/CSS）
eye_rest_config.json   # 用户配置（可选，缺省时使用内置默认值）
eye_rest_state.json    # 运行时状态（下次提醒时间）
MAINTENANCE.md         # 维护记录（缺陷根因与修复验证）
```

## 技术栈

- Python 3 + pywebview（WebView2）
- HTML/CSS — Apple Glassmorphism 风格
- Windows 10/11（需要 Edge Chromium / WebView2 运行时）

## License

MIT
