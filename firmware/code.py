# Pico Pad 固件 - M1：读摇杆和按键，打印到串口
#
# 验收标准：
#   - 摇杆松开时 X、Y 都稳定在 0
#   - 推到底接近 +1 / -1，方向和你想的一致（不一致就改 config.py 的 INVERT_*）
#   - 每个按键按一次只出现一次 down / up，没有连跳
#
# 重新校准：不碰摇杆，在串口里按 Ctrl+D（软重启）。
import time

import analogio
import board
import digitalio
import keypad

import config

VERSION = "0.1.0-m1"
ADC_MAX = 65535


class Axis:
    """一个摇杆轴：读 ADC、扣掉中心偏移、加死区，输出 -1.0 ~ 1.0。"""

    def __init__(self, pin, invert):
        self.adc = analogio.AnalogIn(pin)
        self.invert = invert
        self.center = ADC_MAX // 2
        self.noise = 0
        self.last_raw = self.center

    def raw(self):
        total = 0
        for _ in range(config.ADC_SAMPLES):
            total += self.adc.value
        self.last_raw = total // config.ADC_SAMPLES
        return self.last_raw

    def calibrate(self):
        total = 0
        low = ADC_MAX
        high = 0
        for _ in range(config.CALIBRATION_SAMPLES):
            r = self.raw()
            total += r
            low = min(low, r)
            high = max(high, r)
            time.sleep(0.003)
        self.center = total // config.CALIBRATION_SAMPLES
        self.noise = (high - low) // 2

    def read(self):
        r = self.raw()
        # 中心不一定在正中间，所以正负两边分别按各自的行程换算
        if r >= self.center:
            span = ADC_MAX - self.center
        else:
            span = self.center
        v = (r - self.center) / span if span else 0.0
        if self.invert:
            v = -v
        return apply_deadzone(v, config.DEADZONE)


def apply_deadzone(v, dz):
    """死区内归零；死区外重新拉伸到 0~1，避免一出死区就跳到 0.1。"""
    mag = abs(v)
    if mag <= dz:
        return 0.0
    mag = (mag - dz) / (1.0 - dz)
    if mag > 1.0:
        mag = 1.0
    return mag if v > 0 else -mag


def make_led():
    try:
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        return led
    except (AttributeError, ValueError):
        return None


def blink(led, times, gap=0.08):
    if led is None:
        return
    for _ in range(times):
        led.value = True
        time.sleep(gap)
        led.value = False
        time.sleep(gap)


def main():
    led = make_led()
    print()
    print("Pico Pad", VERSION)
    print("Calibrating joystick, don't touch it...")
    blink(led, 3)

    x_axis = Axis(config.JOY_X_PIN, config.INVERT_X)
    y_axis = Axis(config.JOY_Y_PIN, config.INVERT_Y)
    for name, axis in (("X", x_axis), ("Y", y_axis)):
        axis.calibrate()
        pct = axis.noise * 100 / ADC_MAX
        print("  %s center=%d noise=+/-%d (%.1f%%)" % (name, axis.center, axis.noise, pct))
        # 中心离正中间太远，多半是接线问题（比如 VCC 接错或者某根线松了）
        if abs(axis.center - ADC_MAX // 2) > ADC_MAX * 0.2:
            print("  ! %s center looks off. Check VCC=3V3, GND, and the %s wire." % (name, name))
        if pct * 2 > config.DEADZONE * 100:
            print("  ! %s noise is bigger than DEADZONE, raise DEADZONE in config.py" % name)

    names = [b[0] for b in config.BUTTONS]
    keys = keypad.Keys(
        tuple(b[1] for b in config.BUTTONS),
        value_when_pressed=False,
        pull=True,
        interval=config.DEBOUNCE,
    )
    event = keypad.Event()
    held = set()

    print("Ready. Buttons:", ", ".join(names))
    if led:
        led.value = True

    last_print = 0.0
    last_state = None

    while True:
        # 按键事件：keypad 在后台扫描和消抖，这里只取事件
        while keys.events.get_into(event):
            name = names[event.key_number]
            if event.pressed:
                held.add(name)
                print("[btn] %s down" % name)
            else:
                held.discard(name)
                print("[btn] %s up" % name)

        now = time.monotonic()
        if now - last_print >= config.PRINT_INTERVAL:
            last_print = now
            x = x_axis.read()
            y = y_axis.read()
            if config.SWAP_XY:
                x, y = y, x

            if config.PLOTTER:
                print((round(x, 3), round(y, 3)))
            else:
                # 只在处理后的值变化时打印，串口不刷屏（原始值一直在抖，不参与比较）
                held_text = " ".join(n for n in names if n in held) or "-"
                state = (round(x, 2), round(y, 2), held_text)
                if state != last_state:
                    last_state = state
                    print("X %+.2f (raw %5d)   Y %+.2f (raw %5d)   held: %s" % (
                        x, x_axis.last_raw, y, y_axis.last_raw, held_text))

        time.sleep(0.002)


main()
