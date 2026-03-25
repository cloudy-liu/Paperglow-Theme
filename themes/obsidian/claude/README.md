# Claude Theme for Obsidian

将 Typora Claude 主题的暖纸面、陶土强调色、Montserrat 排版和编辑稿式卡片语言迁移到 Obsidian 的视觉等价版本。

## 安装

### 一键安装

```bash
python install.py obsidian --vault "/path/to/your/vault"
```

安装脚本会把以下文件写入你的 vault：

- `.obsidian/themes/Claude/theme.css`
- `.obsidian/themes/Claude/manifest.json`

如需覆盖已有版本，追加 `--force`。

### 手动安装

1. 打开目标 vault 的 `.obsidian/themes/` 目录
2. 新建 `Claude/` 目录
3. 将 `themes/obsidian/claude/theme.css` 和 `themes/obsidian/claude/manifest.json` 复制进去
4. 在 Obsidian 的 `设置 -> 外观 -> 主题` 中选择 **Claude**

## 特性

- 延续 Typora Claude 的暖纸面 light 配色与夜间深墨 dark 配色
- 统一 Montserrat / Noto Sans SC / JetBrains Mono 字体体系
- Markdown 预览与编辑区都采用更像纸面稿件的卡片式阅读容器
- 16px 圆角代码块、暖灰引用块、陶土色链接和 callout
- 侧栏、标签页、导航项也同步映射到 Claude 的 UI 语气

## 文件

```text
themes/obsidian/claude/
├── theme.css
├── manifest.json
├── README.md
└── test/
    └── test_theme.py
```

## 测试

```bash
python themes/obsidian/claude/test/test_theme.py
```

## 许可证

Apache License 2.0
