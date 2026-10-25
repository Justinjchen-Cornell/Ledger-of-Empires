# 互动故事原型

第 1 章《此朝无钱胜有钱》的可玩版本：选 A/B/C/D → 看短期后果 → 历史揭晓 → 本章机制。

## 本地预览

```bash
cd 05-输出/工作台
python -m http.server 8000
```

打开 http://localhost:8000/story.html

> 必须用本地服务器，不能直接双击 `story.html`；`fetch` 在 `file://` 下会被浏览器拦截。

## 结构

- `story.html` / `story.css` / `story.js`：静态引擎
- `stories/ch01.json`：第 1 章场景图

## 加一章

1. 复制 `stories/ch01.json` 为 `stories/ch02.json`，改 `id`、`title`、`scenes`。
2. 打开 `story.html?story=ch02`。
3. `pytest tests/test_story_json.py` 会自动校验 `stories/` 下所有 JSON。

## 约束

- 纯静态，无后端、无账号、无数据库。
- 每个场景必须有 `text`，并且有 `choices` / `next` / `card` 之一。
- 所有 `next` 必须指向存在的场景。
- 至少 3 幕 + 1 个 `card` 结尾。
