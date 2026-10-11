# 网页端

| 文件 | 作用 |
|---|---|
| `tester.html` | 手柄测试页：轴、按键、1 秒抖动、更新频率。直接双击用浏览器打开就行 |
| `index.html` | 还没有。M4 写游戏"接珍珠" |

M5 的 Web Serial 要求页面在 `https` 或 `localhost` 下，本地开发时用：

```bash
cd game
python3 -m http.server 8000
# 打开 http://localhost:8000/tester.html
```
