# Pico Pad 引脚和参数配置
# 接线说明见 hardware/README.md。改接线时只改这个文件。
import board

# ---------- 摇杆 ----------
# 摇杆模块的 VCC 接 3V3（36 脚），GND 接 AGND（33 脚）。不要接 5V。
JOY_X_PIN = board.GP26  # ADC0，31 脚
JOY_Y_PIN = board.GP27  # ADC1，32 脚

# 方向不对时改这里，不用改接线
INVERT_X = False
INVERT_Y = True  # 很多模块往上推时读数变小，所以默认反转 Y
SWAP_XY = False  # 模块转了 90 度装的话设为 True

# 死区：摇杆松开时的抖动小于这个比例就当作 0（0.10 = 10%）
DEADZONE = 0.10

# 每次读 ADC 取几次平均，越大越稳、越慢
ADC_SAMPLES = 4

# 开机校准中心点时采样多少次（期间不要碰摇杆）
CALIBRATION_SAMPLES = 64

# ---------- 按键 ----------
# 默认是 PicoBlock 扩展板：4 个蓝色按键从板子上的 UP/DOWN/LEFT/RIGHT 排针接出来。
# 顺序决定按键编号（之后 HID 手柄的按键 1、2、3…也按这个顺序）。
BUTTONS = (
    ("STICK", board.GP2),   # 摇杆模块的 SW，4 脚
    ("UP", board.GP10),     # 板子方向键排针 UP，14 脚
    ("DOWN", board.GP11),   # DOWN，15 脚
    ("LEFT", board.GP12),   # LEFT，16 脚
    ("RIGHT", board.GP13),  # RIGHT，17 脚
    # 以后想多两个键：面包板上插两个按键（一脚接 GPIO、一脚接 GND），再打开下面两行
    # ("START", board.GP14),  # 19 脚
    # ("SELECT", board.GP15), # 20 脚
)

# 按键按下是高电平还是低电平：
#   "auto"：开机时自动判断（推荐）。板子上的按键自带上拉或下拉电阻，散装按键什么都不带，都能认出来
#   "low"：全部按"按下 = 低电平"处理（按键接 GND）
#   "high"：全部按"按下 = 高电平"处理（按键接 3V3，外面要有下拉电阻）
# 开机检测时不要按任何键。
BUTTON_MODE = "auto"

# 消抖时间（秒）
DEBOUNCE = 0.02

# ---------- 输出（M5 才用，先占位） ----------
OLED_SDA_PIN = board.GP4   # 6 脚
OLED_SCL_PIN = board.GP5   # 7 脚
PIXEL_PIN = board.GP16     # WS2812 数据，21 脚
BUZZER_PIN = board.GP18    # 24 脚
RUMBLE_PIN = board.GP19    # 经三极管驱动震动马达，25 脚

# ---------- 调试输出 ----------
# False：人看的文字；True：(x, y) 元组，可以直接用 Mu / Thonny 的 Plotter 画曲线
PLOTTER = False

# 打印间隔（秒）。只有数值变化时才打印。
PRINT_INTERVAL = 0.05
