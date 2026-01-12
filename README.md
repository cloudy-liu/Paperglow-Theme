# Claude Theme for Typora

基于 [Anthropic 官方品牌指南](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md) 设计的 Typora Markdown 主题。

![Preview](demo.png)

## ✨ 特性

- 🎨 **官方品牌配色** - 严格遵循 Anthropic 官方品牌指南的配色方案
- 🔶 **三色强调系统** - Orange `#d97757` / Blue `#6a9bcc` / Green `#788c5d`
- 🃏 **卡片式布局** - 优雅的悬浮卡片设计，配合柔和阴影
- 🔤 **官方字体规范** - Poppins (标题) + Lora (正文)，自动从 Google Fonts 加载
- 💻 **现代代码风格** - 纯白背景 + 16px 大圆角代码块 + 三色代码高亮
- 📊 **简洁表格** - 底部分隔线风格
- 💬 **温暖提示卡片** - Orange 色调圆角卡片（Note/Tip）
- ✅ **侧边栏高亮** - 大纲悬浮/选中时显示品牌 Orange 色

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

## 🎨 Anthropic 官方配色方案

基于 [官方品牌指南](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md)：

### 主色系

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| Dark | `#141413` | 主文本色 |
| Light | `#faf9f5` | 浅色背景 |
| Mid Gray | `#b0aea5` | 次要元素 |
| Light Gray | `#e8e6dc` | 边框/内联代码背景 |

### 强调色系

| 用途 | 颜色值 | 应用场景 |
|------|--------|----------|
| Orange | `#d97757` | 主强调色、关键字、链接悬停、高亮 |
| Blue | `#6a9bcc` | 次要强调、函数定义、内置函数 |
| Green | `#788c5d` | 第三强调、字符串 |

## 🔤 字体规范

主题使用 Google Fonts 自动在线加载，**无需手动安装字体**。

- **标题字体**: Poppins (无衬线)
  ```
  "Poppins", "Arial", system-ui, sans-serif
  ```

- **正文字体**: Lora (衬线)
  ```
  "Lora", "Georgia", "Times New Roman", serif
  ```

- **代码字体**: JetBrains Mono
  ```
  "JetBrains Mono", "SF Mono", Menlo, Monaco, Consolas, monospace
  ```

> 💡 **离线使用**：如需离线使用，可从 [Google Fonts](https://fonts.google.com) 下载并安装 Poppins 和 Lora 字体。

## 📁 文件说明

```shell
Typora-claude-theme/
├── claude.css             # 主题文件（安装此文件）
├── test-claude-theme.md   # 测试用 Markdown 文件
├── README.md              # 说明文档
└── demo.png               # 预览图片
```

## 🖼️ 支持的元素

- 六级标题 (H1-H6)
- 段落和文本格式（加粗、斜体、删除线、下划线、高亮）
- 链接（悬停显示 Orange 强调色）
- 代码（Light Gray 内联代码 + 大圆角代码块）
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

基于 Anthropic 官方三色系统：

| 类型 | 颜色 | 说明 |
|------|------|------|
| 关键字/标签 | `#d97757` | Orange |
| 字符串/引用 | `#788c5d` | Green |
| 函数定义/链接 | `#6a9bcc` | Blue |
| 数字/原子值 | `#c45a3a` | Orange 变体 |
| 注释 | `#b0aea5` | Mid Gray |
| 变量/运算符 | `#141413` | Dark |

## 📜 许可证

MIT License

## 🙏 致谢

- 设计规范来自 [Anthropic 官方品牌指南](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md)
- 感谢 [Typora](https://typora.io) 提供优秀的 Markdown 编辑器
- 字体由 [Google Fonts](https://fonts.google.com) 提供

---

*Made with ❤️ for Claude fans*

**Version 2.0.0** | 基于 Anthropic 官方品牌指南
