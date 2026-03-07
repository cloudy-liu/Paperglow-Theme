# Markdown Themes

各类 Markdown 编辑器 / 笔记应用的自定义主题合集。

## 主题列表

| 应用 | 主题名 | 风格 | 路径 |
|------|--------|------|------|
| Typora | Claude | Claude artifact amber 暖色调 | [`typora/claude/`](typora/claude/) |
| Obsidian | WizNote | 为知笔记风格还原 | [`obsidian/wiznote/`](obsidian/wiznote/) |

## 安装

每个主题目录下有独立的 README 说明安装方法。

### Typora - Claude 主题

将 `typora/claude/claude.css` 复制到 Typora 主题目录。详见 [typora/claude/README.md](typora/claude/README.md)。

### Obsidian - WizNote 主题

将 `obsidian/wiznote/` 目录下的 `theme.css` 和 `manifest.json` 复制到 Obsidian vault 的 `.obsidian/themes/WizNote/` 目录。

## 项目结构

```
markdown-themes/
├── typora/
│   └── claude/          # Typora Claude 主题
│       ├── claude.css
│       ├── demo.png
│       ├── test-layout.md
│       └── README.md
├── obsidian/
│   └── wiznote/         # Obsidian WizNote 主题
│       ├── theme.css
│       └── manifest.json
├── .gitignore
├── LICENSE
└── README.md
```

## 许可证

Apache License 2.0
