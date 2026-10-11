#!/usr/bin/env bash
# 把固件复制到 Pico 的 CIRCUITPY 盘（macOS / Linux）
# 用法：./deploy.sh            自动找 CIRCUITPY
#       ./deploy.sh /path/to/CIRCUITPY
set -euo pipefail
cd "$(dirname "$0")"

DEST="${1:-}"
if [ -z "$DEST" ]; then
  for d in /Volumes/CIRCUITPY "/media/${USER:-}/CIRCUITPY" "/run/media/${USER:-}/CIRCUITPY"; do
    if [ -d "$d" ]; then DEST="$d"; break; fi
  done
fi
if [ -z "$DEST" ] || [ ! -d "$DEST" ]; then
  echo "找不到 CIRCUITPY 盘。确认 Pico 已经刷好 CircuitPython 并插上，或者把盘的路径作为参数传进来。"
  exit 1
fi

# code.py 放最后：它一保存 Pico 就会自动重跑，先把它依赖的文件放好
files=(config.py)
[ -f boot.py ] && files+=(boot.py)
files+=(code.py)

if [[ "${OSTYPE:-}" == darwin* ]]; then
  cp -X "${files[@]}" "$DEST"/   # -X：不复制 macOS 的扩展属性，避免盘里出现 ._ 文件
else
  cp "${files[@]}" "$DEST"/
fi
sync

echo "已复制 ${files[*]} 到 $DEST"
if [ -f boot.py ]; then
  echo "注意：boot.py 只在上电时运行，改了它要拔插一次 USB 才生效。"
fi
