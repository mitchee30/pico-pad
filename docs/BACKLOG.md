# Pico Pad 路线图

每一步做完都打勾。验收标准写在每步最后一项。

## M0 准备
- [ ] 刷 CircuitPython（步骤见 [firmware/README.md](../firmware/README.md)）
- [ ] 装好 Thonny 或 Mu，能看到串口
- [ ] 验收：改 `code.py` 保存后板子自动重跑

## M1 读硬件 ← 现在在这
- [x] `config.py`：引脚、死区、消抖、方向反转
- [x] `code.py`：开机校准中心点、ADC 取平均、死区、`keypad` 消抖、串口打印
- [ ] 按 [hardware/README.md](../hardware/README.md) 在面包板上接摇杆和 6 个按键
- [ ] 记下校准时打印的 noise，确定 `DEADZONE`
- [ ] 验收：摇杆松开稳在 0，推到底接近 ±1，方向正确；每个按键按一次只有一次 down / up

## M2 当键盘
- [ ] `circup install -r requirements.txt` 装 `adafruit_hid`
- [ ] 摇杆 → 方向键（过阈值才按下，回中松开），A → 空格，B → Z，START → Enter
- [ ] 验收：用自己的手柄玩通一局 Chrome 小恐龙（`chrome://dino`）

## M3 当手柄
- [ ] `boot.py`：自定义 gamepad 报告描述符（16 键 + 4 轴），同时打开 `usb_cdc` 的 data 口
- [ ] 轴值映射到 -127~127，只在状态变化时发报告
- [ ] 开机模式选择：按住 SELECT 插线进键盘模式
- [ ] 测一下报告率（`game/tester.html` 上有显示）
- [ ] 验收：`game/tester.html` 上轴平滑变化，每个按键编号对得上

## M4 游戏："接珍珠"
- [ ] `game/index.html` + Canvas，固定步长主循环
- [ ] `input.js`：键盘和手柄统一成 `{ x, dash, pause }`
- [ ] 规则：摇杆左右移动杯子，A 冲刺，漏接 3 颗结束，越来越快
- [ ] 调试浮层：显示原始轴值和按键
- [ ] 验收：键盘和手柄都能完整玩一局，60 fps 不掉帧

## M5 反馈回路
- [ ] Pico 端实现 [串口协议](protocol.md)：非阻塞读、震动/音效按结束时间关
- [ ] 接震动马达、蜂鸣器、WS2812、OLED（电路见 hardware/README.md）
- [ ] 网页加"连接手柄"按钮（Web Serial），漏接 → `V 200` + `L n`，得分 → `S n`
- [ ] 验收：漏接时手柄震动，灯和命数同步，屏幕显示分数，操作不卡

## M6 实体化
- [ ] 从面包板换到洞洞板
- [ ] USB 线做固定，防止拉扯
- [ ] 外壳（纸盒 / 3D 打印 / 激光切割），贴按键标签
- [ ] 验收：拿在手里玩 10 分钟没有松线

## M7 展示
- [ ] 接线图（Fritzing 或 KiCad）放进 `hardware/`
- [ ] README 加演示 GIF 和照片
- [ ] GitHub Pages 发布 `game/`
- [ ] 写设计取舍：死区、消抖、为什么 HID + 串口双通道、延迟实测
- [ ] 验收：别人只看 README 就能照着做出来

## 之后可以做
- [ ] MPU6050 体感：倾斜控制
- [ ] 两个手柄双人模式
- [ ] 用 Pico C SDK + TinyUSB 重写固件，对比延迟
- [ ] Pico W 蓝牙无线
- [ ] 圆形死区（现在是每个轴单独算的方形死区，斜推时手感不一样）
- [ ] 把"接珍珠"放进 Hi Tea 的订单等待页

## 已完成
- [x] 2026-10-11 建仓库：README、路线图、硬件清单和引脚表、串口协议草案、M1 固件、手柄测试页
