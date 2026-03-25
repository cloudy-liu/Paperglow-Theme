# Claude Theme for Typora

以 Claude artifact 的结构语气为骨架，使用暖纸面、陶土色强调和 Montserrat 排版构建的 Typora 主题。

![Preview](demo.png)

## 特性

- 暖纸面 light 配色与独立 dark 配色
- 卡片式正文容器与更克制的阴影层次
- Montserrat / Noto Sans SC / JetBrains Mono 统一字体体系
- 16px 圆角代码块、暖灰引用块、陶土色链接
- 保留 Windows `Unibody` 顶栏适配

## 安装

### 一键安装

```bash
python install.py typora
```

如需覆盖默认目录或安装到自定义位置：

```bash
python install.py typora --target-dir "C:\path\to\Typora\themes"
```

### 手动安装

把以下两个文件一起复制到 Typora 主题目录：

- `themes/typora/claude/claude.css`
- `themes/typora/claude/claude-dark.css`

系统默认目录：

- Windows: `%APPDATA%\Typora\themes\`
- macOS: `~/Library/Application Support/abnerworks.Typora/themes/`
- Linux: `~/.config/Typora/themes/`

`claude-dark.css` 会 `@import` `./claude.css`，所以两个文件必须同时存在。

## 测试

```bash
python themes/typora/claude/test/test_theme.py
```

脚本会检查：

- `claude.css` 的核心 token 与 Windows Unibody selector
- `claude-dark.css` 是否正确导入 `claude.css`
- README 是否包含 `python install.py typora`、`claude-dark.css` 和 Unibody 说明
- 示例 Markdown 是否覆盖常见组件与新的仓库路径

## 文件

```text
themes/typora/claude/
├── claude.css
├── claude-dark.css
├── demo.png
├── README.md
└── test/
    ├── test-theme.md
    └── test_theme.py
```

## Windows 顶栏 / 菜单栏说明

- Typora 主题 CSS 可以稳定覆盖正文区、侧栏、搜索面板和部分 HTML UI。
- Windows 默认窗口样式下，最上方菜单栏是系统原生控件，不会被主题 CSS 改色。
- 如果希望顶部区域也跟随 Claude 主题，请在 Typora 的 `Settings / 偏好设置 -> Appearance / 外观 -> Window Style` 中切换到 `Unibody`，然后重启 Typora。

## 许可证

Apache License 2.0
