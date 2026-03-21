# Claude Theme for Typora

基于 Claude artifact 的结构语言设计，并吸收 Claude-Like Theme 的暖纸面 light 配色；保留 Montserrat 几何无衬线排版，同时新增一份更耐看的 dark 版本。

![Preview](demo.png)

## ✨ 特性

- **暖纸面 / 陶土色配色** - 吸收 Claude-Like Theme 的 light 场景色板，改成更像纸张与编辑稿的暖中性色
- **卡片式布局** - 16px 大圆角悬浮卡片，配合柔和阴影
- **Montserrat 字体** - 标题与正文统一使用 Montserrat，中文回退 Noto Sans SC / PingFang SC
- **现代代码风格** - 纯白背景 + 16px 大圆角代码块
- **编辑感引用卡片** - 陶土边框 + 米白底色 + 更克制的阴影层次
- **简洁表格** - 大写表头 + 底部分隔线风格
- **侧边栏高亮** - 大纲悬浮/选中时显示 terracotta 强调色
- **独立 dark 版本** - 新增 `claude-dark.css`，延续同一套结构与交互语义

## 📦 安装方法

### 方法一：一键安装脚本

在仓库根目录运行：

```bash
python typora/claude/install_theme.py
```

脚本会自动识别当前系统的 Typora 主题目录，并复制：

- `claude.css`
- `claude-dark.css`

如果你想安装到自定义目录，可以显式传入目标路径：

```bash
python typora/claude/install_theme.py --target-dir "C:\path\to\Typora\themes"
```

### 方法二：手动安装

1. 下载 `claude.css` 和 `claude-dark.css` 文件

2. 打开 Typora 的主题文件夹：
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Linux**: `~/.config/Typora/themes/`

3. 将两个文件都复制到主题文件夹

   - `claude.css` 是 light 主题
   - `claude-dark.css` 是 dark 主题，并且 imports ./claude.css，所以需要与 `claude.css` 一起复制

4. 重启 Typora

5. 在 `主题` 菜单中选择 **"Claude"** 或 **"claude-dark"**

### 方法三：通过 Typora 打开主题文件夹

1. 打开 Typora
2. 进入 `文件` → `偏好设置` → `外观` → `打开主题文件夹`
3. 将 `claude.css` 和 `claude-dark.css` 一起复制到打开的文件夹中
4. 重启 Typora
5. 选择 Claude 或 claude-dark 主题

## 🎨 配色方案

以 Claude artifact 的版式语气为骨架，light 模式吸收 Claude-Like Theme 的暖纸面与陶土强调色，dark 模式则延续同一语义关系。

### Light 表面色系

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 背景 | `#F7F2EB` | 暖纸面背景 |
| 卡片 | `#FCFAF6` | 更亮一点的正文卡片 |
| 侧栏 | `#EFE7DC` | 比正文略深的 UI 面板 |
| 边框 | `#DDD5CA` | 低对比暖灰边框 |

### Light 文本色系

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 主文本 | `#2B2621` | 深褐正文 |
| 次要文本 | `#61574F` | 次级说明 |
| 元信息 | `#7B6F64` | 辅助信息 / 注释 |

### Light 强调色

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 主强调 | `#BC6A3A` | terracotta 主色 |
| 链接 | `#8F4B28` | 深陶土链接色 |
| 引用背景 | `#F3EDE5` | 米白引用底色 |
| 引用文本 | `#625950` | 暖灰褐引用文本 |

### Dark 核心色系

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 背景 | `#151210` | 深墨纸面背景 |
| 卡片 | `#1B1714` | 正文卡片 |
| 主文本 | `#DDD4CA` | 暖米白正文 |
| 主强调 | `#D59567` | 夜间 terracotta 强调色 |

## 🔤 字体规范

主题使用 Google Fonts 自动在线加载，**无需手动安装字体**。

- **标题 & 正文字体**: Montserrat (无衬线)
  ```
  "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans SC", "PingFang SC", sans-serif
  ```

- **代码字体**: JetBrains Mono
  ```
  "JetBrains Mono", "SF Mono", SFMono-Regular, Menlo, Monaco, Consolas, monospace
  ```

> 离线使用：如需离线使用，可从 [Google Fonts](https://fonts.google.com) 下载并安装 Montserrat 和 Noto Sans SC 字体。

## 📁 文件说明

```
typora/claude/
├── claude.css         # light 主题
├── claude-dark.css    # dark 主题（imports ./claude.css）
├── install_theme.py   # 一键复制主题到 Typora 目录
├── test/
│   ├── test-theme.md  # Markdown 全样式测试文档
│   └── test_theme.py  # 主题静态自检脚本
├── README.md          # 说明文档
└── demo.png           # 预览图片
```

## 🧪 测试

运行合并后的测试脚本：

```bash
python typora/claude/test/test_theme.py
```

脚本会检查：

- `claude.css` 中的核心语义 token 是否存在
- Windows Unibody 顶栏相关 selector 是否仍然保留
- `claude-dark.css` 是否正确导入 `claude.css` 并覆盖暗色 token
- `install_theme.py` 是否存在并能复制主题文件到目标目录
- `README.md` 是否包含 dark 主题与 Unibody 的安装说明

## 🖼️ 支持的元素

- 六级标题 (H1-H6)
- 段落和文本格式（加粗、斜体、删除线、下划线、高亮）
- 链接
- 代码（内联代码 + 大圆角代码块）
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

| 类型 | 颜色 | 色值 |
|------|------|------|
| 关键字 | 紫色 | `#7B47C2` |
| 字符串/引用 | 绿色 | `#2F8F2F` |
| 函数定义/链接 | 蓝色 | `#2C5EC6` |
| 数字/原子值 | 橙黄 | `#C06A2A` |
| 属性/变量2 | 橙棕 | `#B26147` |
| 注释 | 灰褐 | `#9B8F83` |
| 变量/运算符 | 深褐 | `#342D27` |

## 📜 许可证

MIT License

## 🙏 致谢

- 配色方案延续 Claude artifact 的结构感，并吸收 Typora Claude-Like Theme 的 light/dark 氛围
- 字体方案参考 laper.ai (Montserrat + Noto Sans SC)
- 感谢 [Typora](https://typora.io) 提供优秀的 Markdown 编辑器
- 字体由 [Google Fonts](https://fonts.google.com) 提供

## Windows 顶栏 / 菜单栏说明

- Typora 主题 CSS 可以稳定覆盖正文区、侧栏、搜索面板和部分 HTML UI。
- Windows 默认窗口样式下，最上方菜单栏是系统原生控件，不会被主题 CSS 改色。
- 如果希望顶部区域也跟随 Claude 主题，请在 Typora 的 `Settings / 偏好设置 -> Appearance / 外观 -> Window Style` 中切换到 `Unibody`，然后重启 Typora。
- 本主题从 `3.1.0` 开始补充了 `Unibody` 顶栏样式，标题栏、窗口标题和顶部按钮会与正文背景统一。

---

**Version 3.2.0** | Claude editorial paper palette + dark variant + Windows Unibody title bar support
