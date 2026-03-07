# Obsidian WizNote Theme

基于为知笔记 (WizNote) 源码 CSS/JS 提取，忠实还原其视觉风格的 Obsidian 主题。

## 安装

1. 将 `theme.css` 和 `manifest.json` 复制到 Obsidian vault 的 `.obsidian/themes/WizNote/` 目录
2. 在 Obsidian 设置 → 外观 中选择 **WizNote** 主题

## 特性

- 基于 WizNote 源码精确提取，非截图估算
- 亮色 / 暗色双模式
- 字体大小、间距完全匹配 WizNote 编辑器（renderer.dev.js）
- Markdown 渲染样式完整适配 github2.css
- 配色：`#448aff` 蓝色强调，`#07142a` 深海军蓝正文
- 行内代码绯红色 `#c7254e`，代码块浅灰底 `#f8f8f8`

## 数据来源

| 文件 | 提取内容 |
|------|----------|
| `renderer.dev.js` | 字体大小、行高、间距、编辑器配色 |
| `renderer.dev.css` | UI 组件样式、滚动条、阴影、圆角 |
| `github2.css` | Markdown 渲染规则（代码、表格、引用、列表等） |
