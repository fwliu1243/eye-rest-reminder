# 护眼提醒 (Eye Rest Reminder)

一个轻量的 Windows 桌面护眼提醒小工具：**每 20 分钟提醒你休息眼睛**（20-20-20 法则），开机自启，后台静默运行。

## 特性

- ⏰ 每 20 分钟弹出置顶提醒窗口，遵循 20-20-20 法则（看 20 英尺外 20 秒）
- 🔔 提醒窗口带 20 秒倒计时 + "5 分钟后提醒"推迟按钮
- 🚀 开机自启（注册表 HKCU Run，无需管理员权限）
- 🔄 提醒循环执行，不依赖一次性定时器；系统睡眠/挂起后自动补弹，不漏提醒
- 🕐 计时以**开机时刻**为基准（开机后每 20 分钟一个提醒节点），双击快捷方式只查询状态，不影响计时
- 📊 双击快捷方式可查看"下次提醒时间"
- 📝 间隔、休息时长、提示文案均可配置

## 快速开始

### 1. 下载/克隆

```bash
git clone https://github.com/LIO-H-ZEN/eye-rest-reminder.git
cd eye-rest-reminder
```

### 2. 启动（需安装 Python 3）

```powershell
# 静默后台运行（无控制台窗口）
pythonw.exe eye_rest.py

# 立即弹窗测试
python eye_rest.py --test
```

### 3. 开机自启

注册表方式（当前用户级，免管理员）：

```powershell
# 添加自启（路径替换为你的实际路径）
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" `
  -Name "EyeRestReminder" `
  -Value '"C:\path\to\pythonw.exe" "C:\path\to\eye_rest.py"'

# 取消自启
Remove-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name EyeRestReminder
```

> 提示：也可以创建桌面快捷方式指向 `pythonw.exe eye_rest.py`，双击查询状态、未运行时启动。

## 配置

首次运行后在同目录生成 `eye_rest_config.json`（不存在时手动创建）：

```json
{
  "interval_min": 20,
  "break_sec": 20,
  "text": "该休息眼睛了！\n\n看看远处 20 英尺（约 6 米）以外的物体\n至少 20 秒，让睫状肌放松\n\n（20-20-20 法则）"
}
```

| 字段 | 默认 | 说明 |
|------|------|------|
| `interval_min` | 20 | 提醒间隔（分钟） |
| `break_sec` | 20 | 倒计时秒数（20-20-20 法则） |
| `text` | 默认文案 | 提醒窗口正文 |

## 工作原理

- **计时基准**：使用 `GetTickCount64()` 获取系统开机时刻，提醒节点 = 开机时刻 + N × 间隔（N 使节点在未来）。
- **轮询检查**：每 10 秒检查一次是否到达节点；到达即弹窗，弹窗后自动指向下一个节点。睡眠/挂起不会丢提醒。
- **单实例**：通过本地端口（28940）绑定检测，重复启动时弹状态提示并退出，不会双开、不重置计时。
- **`--test` 模式**：立即弹窗验证，不受单实例限制。

## 目录结构

```
eye_rest.py            # 主程序（无第三方依赖，仅标准库）
eye_rest_config.json   # 用户配置（运行时生成/读取）
eye_rest_state.json    # 运行时状态（下次提醒时间，勿提交）
```

## 技术栈

- Python 3（标准库 tkinter / socket / ctypes，零第三方依赖）
- Windows 10/11

## License

[MIT](LICENSE) © 2026 LIO-H-ZEN
