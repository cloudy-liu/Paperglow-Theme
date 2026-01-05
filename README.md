# Claude Theme for Typora

一个完全复刻 [Claude Code 官方文档](https://code.claude.com/docs) 设计风格的 Typora Markdown 主题。

## ✨ 特性

- 🎨 **官网精准配色** - 使用官网暖白背景 `#FDFDF7` 与深调衬底 `#f0eee6`
- 🃏 **卡片式布局** - 优雅的悬浮卡片设计，配合柔和阴影
- 🔶 **标志性橙色强调** - Claude 品牌色 `#D4A27F` 用于侧边栏高亮
- 📝 **清晰的排版** - 优化的标题层级、段落间距和行高
- 💻 **现代代码风格** - 纯白背景 + 16px 大圆角代码块
- 📊 **简洁表格** - 底部分隔线风格
- 💬 **提示卡片样式** - 暖棕色圆角卡片（Note/Tip），与主色调完美融合
- ✅ **侧边栏橙色高亮** - 大纲悬浮/选中时显示品牌橙色

## 📦 安装方法

### 方法一：手动安装

1. 下载 `claude.css` 文件

2. 打开 Typora 的主题文件夹：
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Linux**: `~/.config/Typora/themes/`

3. 将 `claude.css` 复制到主题文件夹

4. 重启 Typora

5. 在 `主题` 菜单中选择 **"Claude"**

### 方法二：通过 Typora 打开主题文件夹

1. 打开 Typora
2. 进入 `文件` → `偏好设置` → `外观` → `打开主题文件夹`
3. 将 `claude.css` 复制到打开的文件夹中
4. 重启 Typora
5. 选择 Claude 主题

## 🎨 颜色方案

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 全局衬底 | `#f0eee6` | 深米色背景 |
| 内容卡片 | `#FDFDF7` | 温暖亮白 |
| 代码块背景 | `#FFFFFF` | 纯白 |
| 内联代码背景 | `#EEEEEE` | 浅灰 |
| 主文本 | `#3E3E3E` | 官网灰黑色 |
| 次要文本 | `#73726C` | 中灰色 |
| 强调色 | `#D4A27F` | Claude 棕橙色 |
| 边框 | `#E5E7EB` | 浅灰色 |
| 提示卡片 | `rgba(212, 162, 127, 0.08)` | 暖棕色 |

## 🔤 字体

- **正文字体**: Anthropic Sans / System UI
  ```
  "Anthropic Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
  ```

- **标题字体**: Georgia (衬线)
  ```
  "Georgia", "Times New Roman", serif
  ```

- **代码字体**: JetBrains Mono
  ```
  "JetBrains Mono", "SF Mono", Menlo, Monaco, Consolas, monospace
  ```

## 📁 文件说明

```
typroa-copy-theme/
├── claude.css             # 主题文件（安装此文件）
├── test-claude-theme.md    # 测试用 Markdown 文件
├── preview.html            # 浏览器预览文件
└── README.md               # 说明文档
```

## 🖼️ 支持的元素

- 六级标题 (H1-H6)
- 段落和文本格式（加粗、斜体、删除线、下划线、高亮）
- 链接（细下划线样式）
- 代码（无边框内联代码 + 大圆角代码块）
- 引用块 / 提示卡片
- 有序/无序列表
- 任务列表
- 表格
- 图片
- 水平分割线
- 脚注
- 数学公式
- YAML Front Matter
- 目录 (TOC)

## 🌈 代码高亮

基于 One Light 配色方案：

| 类型 | 颜色 |
|------|------|
| 关键字 | `#A626A4` 紫色 |
| 字符串 | `#50A14F` 绿色 |
| 数字 | `#986801` 橙色 |
| 注释 | `#A0A1A7` 灰色 |
| 函数 | `#4078F2` 蓝色 |
| 属性 | `#D4A27F` 棕橙色 |

## 📜 许可证

MIT License

## 🙏 致谢

- 设计灵感来自 [Claude Code 官方文档](https://code.claude.com/docs)
- 感谢 [Typora](https://typora.io) 提供优秀的 Markdown 编辑器

---

*Made with ❤️ for Claude fans*
