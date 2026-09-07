# 维护记录 (Maintenance Log)

本文件记录已发生的线上缺陷、根因分析、修复方式与验证手段，供后续维护参考。

---

## 2026-09-07 · 睡眠唤醒后提醒窗口永久不可见

### 现象

程序进程存活、端口正常监听，但到点后**提醒窗口完全不出现**，用户既看不到也点不到。
表现为「护眼提醒失效了」。

实测现场（2026-09-07）：

| 项目 | 观测值 |
| --- | --- |
| 进程 | PID 29516 存活，运行 7.7 小时 |
| CPU | 39.1s / 7.7h ≈ **0.14%**（无忙等，不是死循环） |
| 线程 | 10 个，数量稳定 |
| 窗口 | `WS_VISIBLE=True`，但矩形为 `(-32000,-32000)-(-31560,-31387)` |
| 状态文件 | 停在 `10:21:41` 写入的 `next_reminder: 10:31`，此后不再更新 |
| 系统事件 | `10:26:59` 进入 Modern Standby，`11:25:25` 唤醒 |

### 定位过程

用 `py-spy dump --pid <pid>` 抓取活线程栈，四次采样位置不变：

```
Thread 27936 (idle): "Thread-2 (<lambda>)"
    break_phase (eye_rest.py:375)      <- ready 阶段等待循环 time.sleep(0.1)
    timer_loop  (eye_rest.py:441)
```

调度线程确实卡在 ready 等待循环里。再看窗口几何，`GetWindowPlacement` 的
`rcNormalPosition` **也是** `(-32000,-32000)` —— 这说明该坐标不是临时停靠，
而是已经被写进了窗口的「正常位置」。

### 根因

Windows 隐藏 WinForms 窗口时，会把它停放到屏幕外的 `(-32000,-32000)`。
pywebview 的 `resize()` 实现会**沿用窗口当前 Location**：

```python
# webview/platforms/winforms.py :: resize()
x = self.Location.X      # 隐藏时 = -32000
y = self.Location.Y      # 隐藏时 = -32000
windll.user32.SetWindowPos(self.Handle, None, x, y, phys_width, phys_height, 64)
```

于是形成故障链：

1. 用户关闭窗口 → `on_closing` 调 `hide()` → 窗口被停放到 `(-32000,-32000)`
2. 机器进入睡眠，唤醒后 `next_ts` 已逾期，`break_phase` 立即触发
3. `bring_to_front()` → `resize_for_mode()` → `win.resize()`
   把 `-32000` 当作正常坐标写死进 `rcNormalPosition`
4. 随后的 `Show()` 只是把 `WS_VISIBLE` 置位，窗口**可见但在屏幕外**
5. `window_needs_restore()` 只检查 `IsWindowVisible` / `IsIconic`，
   两者都返回「正常」，于是后续每次 `bring_to_front()` 都判定无需处理
6. ready 循环等用户点击「开始休息」/「5 分钟后提醒」，而窗口永远看不见、
   点不到，直到 1800 秒超时才继续；下一个节点重复整个过程

第 5 步是关键：判断条件漏掉了「窗口虽可见但不在任何显示器上」这一状态，
使故障**自我固化**，重启前无法自愈。

### 修复

新增基于虚拟屏幕边界的离屏检测与纠偏，并在所有可能移动窗口的路径末尾调用：

- `_window_rect()` / `_virtual_screen()` / `_work_area()` — 取窗口矩形、
  所有显示器合并边界、就近显示器工作区（扣除任务栏）
- `window_off_screen(hwnd)` — 与虚拟屏幕求交，判断是否完全落在屏幕外
  （`OFFSCREEN_MARGIN = 40` 容差，避免贴边窗口被误判）
- `ensure_on_screen(hwnd)` — 用 `SetWindowPos(SWP_NOSIZE | SWP_NOZORDER | SWP_SHOWWINDOW)`
  把离屏窗口搬回就近显示器工作区内（水平居中、垂直约 1/3 处），**不改变尺寸**

接入点：

| 位置 | 作用 |
| --- | --- |
| `window_needs_restore()` | 追加离屏判断，使停放的窗口走还原分支 |
| `bring_to_front()` | `resize_for_mode()` **之后**再纠偏（顺序关键，否则 resize 又把坐标写回离屏） |
| `resize_for_mode()` | 两条出口（模式未变 / 已 resize）都纠偏；同时把 `except: return` 改为 `except: pass` + `else:`，避免 resize 异常时跳过 `fit_window` |
| `break_phase()` 两个循环 | 每 2 秒调一次 `guard_window()` |

循环内守护的必要性：ready 阶段最长空转 1800 秒，期间若发生一次睡眠唤醒，
窗口会被再次停放，只在进入阶段时检查一次不足以覆盖。

### 回归：守护不能对抗用户的隐藏意图

首版守护会**无条件**把离屏窗口拉回来，导致用户在休息阶段主动点 X 关闭后，
窗口在 2 秒内被强行拽回 —— 破坏了「关闭转后台」这一既有特性。

修复方式是让守护尊重用户意图：

- `_state` 增加 `'user_hidden': False`
- `on_closing()` 隐藏前置 `True`
- `ensure_on_screen()` 开头 `if _state.get('user_hidden'): return`
- `bring_to_front()` 入口置回 `False`（提醒到点、或用户点桌面快捷方式，
  都属于「主动要显示」，应当覆盖之前的隐藏）

### 顺带修复：状态文件长期失真

`write_state()` 只在重排时调用，进程启动时不写。若某次启动后一直未重排，
`eye_rest_state.json` 会长期保留上一次的旧值，诊断时严重误导。
现在启动时即写入一次真实的 `next_ts`。

### 验证

对**实际发布的进程**做端到端验证（`--test` 模式启动独立实例复现，
真实实例验证单实例与唤回）：

| 场景 | 做法 | 结果 |
| --- | --- | --- |
| 待机停放自动恢复 | `SetWindowPos` 把 ready 窗口搬到 `-32000`，观察守护 | **2.0s** 自动回到 `(1060,259)` 且可见 |
| 用户关闭后保持隐藏 | 投递 `WM_CLOSE`，观察 8s | 保持 `IsWindowVisible=False`，未被拽回 |
| 快捷方式唤回 | 隐藏后向 28940 发 `SHOW` | **0.5s** 还原，尺寸不变 |
| 已可见时重复 SHOW | 连发两次 `SHOW` | 坐标不变，不跳动、不抢焦点 |
| 单实例 | 重复启动一次 | 无新增窗口，次进程立即退出 |

辅助验证：

- 用真实卡死窗口 `0x20758` 校验 `window_off_screen()` 返回 `True`、
  `window_needs_restore()` 返回 `True`
- 枚举 14 个可见应用窗口，离屏误报 **0 个**（唯一被标记的正是故障窗口本身）
- 用 `CreateWindowExW` 造真实窗口验证 `ensure_on_screen()`：
  parked → `(1060,259)`，尺寸 `440x613` 保持不变，二次调用为 no-op

编码完整性：33494 字符，613 行全 CRLF，无裸 LF，无 U+FFFD，UTF-8 解码正常。

### 排查手法备忘

本例进程「活着但不工作」，常规手段（任务管理器、端口探测）看不出异常，
起作用的是这两招：

1. **`py-spy dump --pid <pid>`** —— 无需重启即可拿到 Python 线程栈。
   多次采样对比位置，能立刻区分「死循环忙等」与「阻塞等待」。
   栈里的行号还能反推进程加载的是哪个版本的代码。
2. **窗口几何 + `GetWindowPlacement`** —— `IsWindowVisible` 会骗人，
   `(-32000,-32000)` 这类停放坐标才是真正的判据；`rcNormalPosition`
   能区分「临时隐藏」与「坐标已被写死」。

注意 CPU 占用低（0.14%）**不代表**线程健康 —— 本例线程是阻塞睡眠，
不消耗 CPU。

---

## 2026-09-07 · README 代码块围栏损坏（文档缺陷）

上一版提交（`9747681`）写入 README 时把三反引号围栏降级成了单反引号，
GitHub 渲染后所有代码块都散成普通文本；`bash` 代码块还混入了一个
`\x08`（退格）字节，变成 `` `\x08ash ``。

| 版本 | ``` 数量 | ` 数量 | `\x08` |
| --- | --- | --- | --- |
| `afa9e8d`（原始） | 10 | 46 | 0 |
| `9747681`（上一版） | **0** | 26 | **1** |
| 修复后 | 10 | — | 0 |

已把 10 处围栏还原为三反引号并清除退格字节，逐块校验配对与语言标签
（`bash` / `powershell` ×2 / `json` / 目录结构块），同时确认行内反引号
（如 `interval_min`、`SHOW`、`closing`）未被误改。

**教训**：改文档后要核对字节层面的结构标记，不能只看渲染后的观感；
反引号、控制字符这类问题在终端里很容易被忽略。

---

## 2026-09-06 · 按钮无法点击 + 倒计时冻结

### 根因

- **按钮点不到**：`MODE_HEIGHTS` 给的是整窗高度，页面只拿得到客户区高度
  （差约 39px 标题栏），卡片被 `overflow:hidden` 裁掉，底部按钮落在裁剪区外。
- **倒计时停在 4:45**：`break_phase` 抛异常时没有重排 `next_ts`，
  `timer_loop` 在逾期时间戳上空转；同时 `evaluate_js` 每 100ms 全量重绘，
  同步往返占满 UI 线程，点击事件无法投递。

### 修复

- `measure_card()` 实测卡片高度，`fit_window()` 补偿 chrome 并限制在屏幕高度内
- `break_phase` 异常分支补重排守卫，`timer_loop` 加 0.2s 让出
- 倒计时改为 1Hz、仅在秒数变化时刷新
- 配置健壮性：`_coerce_int()` 夹取区间、`utf-8-sig` 读取（兼容记事本 BOM）、
  `MAX_TEXT_LEN=600`、休息 `1..600s`、间隔 `1..1440min`
  （防 `interval_min: 0` 触发 `ZeroDivisionError`）

### 新增

点击水波纹反馈；单实例 IPC（端口 28940，`SHOW` 指令唤回）；
关闭窗口转后台不退出进程。
