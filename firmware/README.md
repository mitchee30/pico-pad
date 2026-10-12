# 固件（CircuitPython）

| 文件 | 作用 |
|---|---|
| `config.py` | 引脚和参数（死区、消抖、方向反转）。改接线只改这里 |
| `code.py` | 主程序。现在是 M1：读摇杆和按键，打印到串口 |
| `boot.py` | 还没有。M3 加：自定义 USB 手柄描述符 + 打开 data 串口 |
| `requirements.txt` | 要装到板子上的库（用 circup 装） |
| `deploy.sh` | 一键复制到 CIRCUITPY 盘 |

## 第一次刷 CircuitPython

1. 到 [circuitpython.org/downloads](https://circuitpython.org/downloads) 搜你的板子，下载最新 Stable 版的 `.uf2`：
   - Pico → `raspberry_pi_pico`
   - Pico W → `raspberry_pi_pico_w`
   - Pico 2 → `raspberry_pi_pico2`
2. 按住板子上的 BOOTSEL 键再插 USB，电脑上会出现 `RPI-RP2`（Pico 2 是 `RP2350`）盘。
3. 把 `.uf2` 拖进去。板子自动重启，出现 `CIRCUITPY` 盘就成功了。

插上没出现盘？先换一根能传数据的线。

## 把代码放到板子上

```bash
cd firmware
chmod +x deploy.sh   # 第一次需要
./deploy.sh
```

板子检测到 `code.py` 变化会自动重跑。

## 看串口输出

任选一种：

- **Thonny**：右下角选解释器 `CircuitPython (generic)`，下面的 Shell 就是串口。
- **Mu**：选 CircuitPython 模式，点 Serial。把 `config.py` 里的 `PLOTTER` 改成 `True`，再点 Plotter 就能看到摇杆曲线。
- **终端**（macOS）：
  ```bash
  ls /dev/tty.usbmodem*
  screen /dev/tty.usbmodemXXXX 115200
  ```
  退出：`Ctrl+A` 然后 `K`，再按 `y`。

串口里按 `Ctrl+C` 停止程序进入 REPL，按 `Ctrl+D` 软重启（会重新校准摇杆，这时别碰摇杆）。

正常的输出大概是这样：

```
Pico Pad 0.1.0-m1
Calibrating joystick, don't touch it...
  X center=32890 noise=+/-96 (0.1%)
  Y center=33410 noise=+/-120 (0.2%)
Buttons (don't press anything now):
  STICK  GP2   plain switch, pressed=LOW
  UP     GP10  board pull-up, pressed=LOW
  DOWN   GP11  board pull-up, pressed=LOW
  LEFT   GP12  board pull-up, pressed=LOW
  RIGHT  GP13  board pull-up, pressed=LOW
Ready. Buttons: STICK, UP, DOWN, LEFT, RIGHT
X +0.43 (raw 46200)   Y +0.00 (raw 33380)   held: -
[btn] UP down
X +0.43 (raw 46180)   Y +0.00 (raw 33402)   held: UP
[btn] UP up
```

`Buttons` 那几行是开机时自动判断的按键极性：板子上的按键自带上拉或下拉电阻，散装按键什么都不带，固件会分别处理。板子上的 4 个键显示 `pull-up` 还是 `pull-down` 取决于扩展板的设计，两种都没问题。

## 装库（M2 开始需要）

```bash
pip install circup
cd firmware
circup install -r requirements.txt
```

circup 会自动找到插着的 CIRCUITPY 盘，并装和你的 CircuitPython 版本匹配的库。装好的库在板子的 `lib/` 里，不放进 git。

## 常见问题

| 现象 | 原因 / 解决 |
|---|---|
| `center looks off` | 摇杆 VCC 没接 3V3、GND 松了，或者 X/Y 线接反到别的脚 |
| 摇杆方向反了 | 改 `config.py` 的 `INVERT_X` / `INVERT_Y`，横竖反了改 `SWAP_XY` |
| 松开后读数不是 0 | 校准时碰了摇杆（`Ctrl+D` 重来），或者把 `DEADZONE` 调大一点 |
| 一个按键一直是 down | 开机时按着它了（拔插重来），或者排针接错了脚。实在不行把 `BUTTON_MODE` 改成 `"low"` 或 `"high"` 试试 |
| 按键完全没反应 | 方向键排针那根线没插到对应的 GP 排针；或者 Pico 还插在面包板上，没插进扩展板的黑色排母 |
| `ValueError: GPxx in use` | 同一个引脚在 `config.py` 里写了两次 |
| CIRCUITPY 里多了 `._` 开头的文件 | macOS 用 Finder 拖文件产生的，用 `deploy.sh` 就不会有，删掉即可 |
