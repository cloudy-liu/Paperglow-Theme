import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { PNG } from "pngjs";

interface ExtensionPackage {
  displayName?: string;
  description?: string;
  activationEvents?: string[];
  categories?: string[];
  dependencies?: Record<string, string>;
  icon?: string;
  keywords?: string[];
  main?: string;
  scripts?: Record<string, string>;
  contributes?: {
    themes?: ThemeContribution[];
    "markdown.previewStyles"?: string[];
    commands?: unknown[];
    menus?: unknown;
  };
}

interface ThemeContribution {
  label?: string;
  uiTheme?: string;
  path?: string;
}

interface ThemeFile {
  name?: string;
  type?: string;
  colors?: Record<string, string>;
  semanticTokenColors?: Record<string, string>;
  tokenColors?: TokenColor[];
}

interface TokenColor {
  name?: string;
  scope?: string | string[];
  settings?: {
    foreground?: string;
    fontStyle?: string;
  };
}

interface PngAlphaBounds {
  alphaBoxHeight: number;
  alphaBoxWidth: number;
  height: number;
  width: number;
}

const packageRoot = path.resolve(__dirname, "../..");
const packageJsonPath = path.join(packageRoot, "package.json");
const readmePath = path.join(packageRoot, "README.md");
const vscodeIgnorePath = path.join(packageRoot, ".vscodeignore");

function readJsonFile<T>(filePath: string): T {
  return JSON.parse(readFileSync(filePath, "utf8")) as T;
}

function readPackageJson(): ExtensionPackage {
  return readJsonFile<ExtensionPackage>(packageJsonPath);
}

function getThemeContributions(): ThemeContribution[] {
  return readPackageJson().contributes?.themes ?? [];
}

function getThemeContribution(label: string): ThemeContribution {
  const theme = getThemeContributions().find((contribution) => contribution.label === label);
  assert.ok(theme, `Expected ${label} to be contributed as a VS Code color theme`);
  return theme;
}

function readContributedTheme(label: string): ThemeFile {
  const contribution = getThemeContribution(label);
  assert.ok(contribution.path, `${label} should declare a theme file path`);

  const themePath = path.resolve(packageRoot, contribution.path);
  assert.ok(existsSync(themePath), `${label} theme file should exist at ${contribution.path}`);
  return readJsonFile<ThemeFile>(themePath);
}

function readPngAlphaBounds(filePath: string): PngAlphaBounds {
  const png = PNG.sync.read(readFileSync(filePath));
  const bytesPerPixel = 4;
  let minX = png.width;
  let minY = png.height;
  let maxX = -1;
  let maxY = -1;

  for (let y = 0; y < png.height; y += 1) {
    for (let x = 0; x < png.width; x += 1) {
      const alpha = png.data[(png.width * y + x) * bytesPerPixel + 3] ?? 0;
      if (alpha > 10) {
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      }
    }
  }

  return {
    alphaBoxHeight: maxY - minY + 1,
    alphaBoxWidth: maxX - minX + 1,
    height: png.height,
    width: png.width,
  };
}

test("positions the VS Code extension as a complete Paperglow theme with native Markdown preview styling", () => {
  const packageJson = readPackageJson();

  assert.equal(packageJson.displayName, "Paperglow Theme");
  assert.match(packageJson.description ?? "", /complete Paperglow VS Code theme/i);
  assert.match(packageJson.description ?? "", /native Markdown preview/i);
  assert.doesNotMatch(packageJson.description ?? "", /custom Markdown preview/i);
  assert.ok(packageJson.categories?.includes("Themes"));
});

test("does not contribute a custom Paperglow preview command or runtime", () => {
  const packageJson = readPackageJson();

  assert.equal(packageJson.main, undefined);
  assert.equal(packageJson.activationEvents, undefined);
  assert.equal(packageJson.contributes?.commands, undefined);
  assert.equal(packageJson.contributes?.menus, undefined);
  assert.equal(packageJson.dependencies, undefined);
});

test("contributes Paperglow Light and Dark color themes", () => {
  const light = getThemeContribution("Paperglow Light");
  const dark = getThemeContribution("Paperglow Dark");

  assert.equal(light.uiTheme, "vs");
  assert.equal(light.path, "./themes/paperglow-light-color-theme.json");
  assert.equal(dark.uiTheme, "vs-dark");
  assert.equal(dark.path, "./themes/paperglow-dark-color-theme.json");

  assert.equal(readContributedTheme("Paperglow Light").name, "Paperglow Light");
  assert.equal(readContributedTheme("Paperglow Dark").name, "Paperglow Dark");
});

test("uses the Paperglow logo as the VS Code extension icon", () => {
  const packageJson = readPackageJson();
  const svgIconPath = path.resolve(packageRoot, "media/paperglow-icon.svg");

  assert.equal(packageJson.icon, "media/paperglow-icon.png");
  assert.ok(
    existsSync(path.resolve(packageRoot, packageJson.icon)),
    "extension icon should exist in the packaged media directory",
  );
  assert.ok(existsSync(svgIconPath), "high-quality SVG source icon should be kept with packaged media");
  const svgIcon = readFileSync(svgIconPath, "utf8");

  assert.match(svgIcon, /viewBox="0 0 128 128"/);
  assert.match(svgIcon, /paperglow-icon-title/);
  assert.match(svgIcon, /paperglow-paper-mark/);
  assert.doesNotMatch(svgIcon, /<text\b/);
  assert.doesNotMatch(svgIcon, /icon-bg/);
  assert.doesNotMatch(svgIcon, /icon-glow/);

  const pngBounds = readPngAlphaBounds(path.resolve(packageRoot, packageJson.icon));
  assert.equal(pngBounds.width, 512);
  assert.equal(pngBounds.height, 512);
  assert.ok(
    pngBounds.alphaBoxWidth >= 420,
    `extension icon visible width should align with Marketplace list icons; got ${pngBounds.alphaBoxWidth}px`,
  );
  assert.ok(
    pngBounds.alphaBoxHeight >= 455,
    `extension icon visible height should align with Marketplace list icons; got ${pngBounds.alphaBoxHeight}px`,
  );
});

test("uses VS Code native Markdown preview styling instead of a custom Webview preview", () => {
  const packageJson = readPackageJson();
  const previewStyles = packageJson.contributes?.["markdown.previewStyles"] ?? [];

  assert.deepEqual(previewStyles, ["./media/paperglow-markdown-preview.css"]);
  assert.ok(
    existsSync(path.resolve(packageRoot, "./media/paperglow-markdown-preview.css")),
    "native Markdown preview stylesheet should be packaged",
  );
});

test("theme files cover the visible workbench surfaces that prevent preview color drift", () => {
  const requiredColors = [
    "activityBar.background",
    "activityBar.foreground",
    "activityBarBadge.background",
    "badge.background",
    "breadcrumb.background",
    "button.background",
    "editor.background",
    "editor.foreground",
    "editor.findMatchBackground",
    "editor.lineHighlightBackground",
    "editor.selectionBackground",
    "editorCursor.foreground",
    "editorGroupHeader.tabsBackground",
    "editorGroup.border",
    "focusBorder",
    "input.background",
    "list.activeSelectionBackground",
    "list.hoverBackground",
    "list.inactiveSelectionBackground",
    "notificationCenterHeader.background",
    "panel.background",
    "quickInput.background",
    "scrollbarSlider.background",
    "sideBar.background",
    "sideBar.foreground",
    "sideBarSectionHeader.background",
    "statusBar.background",
    "tab.activeBackground",
    "tab.inactiveBackground",
    "terminal.background",
    "titleBar.activeBackground",
  ];

  for (const label of ["Paperglow Light", "Paperglow Dark"]) {
    const theme = readContributedTheme(label);
    assert.ok(theme.colors, `${label} should define workbench colors`);

    for (const colorName of requiredColors) {
      assert.ok(theme.colors[colorName], `${label} should define ${colorName}`);
    }
  }
});

test("list and tree selection states stay subtle in both Paperglow themes", () => {
  const expectedSelectionColors: Record<string, Record<string, string>> = {
    "Paperglow Light": {
      "list.activeSelectionBackground": "#E1CCBA",
      "list.focusBackground": "#E4D2C0",
      "list.hoverBackground": "#E8D9CA",
      "list.inactiveSelectionBackground": "#EADFD4",
    },
    "Paperglow Dark": {
      "list.activeSelectionBackground": "#3B332E",
      "list.focusBackground": "#332D29",
      "list.inactiveSelectionBackground": "#2E2A27",
    },
  };

  for (const [label, expectedColors] of Object.entries(expectedSelectionColors)) {
    const theme = readContributedTheme(label);
    assert.ok(theme.colors, `${label} should define workbench colors`);

    for (const [colorName, expectedColor] of Object.entries(expectedColors)) {
      assert.equal(theme.colors[colorName], expectedColor, `${label} ${colorName}`);
    }
  }
});

test("dark theme foreground brightness follows Atom One Dark's quieter reading level", () => {
  const dark = readContributedTheme("Paperglow Dark");
  assert.ok(dark.colors, "Paperglow Dark should define workbench colors");

  assert.equal(dark.colors.foreground, "#BDB1A4");
  assert.equal(dark.colors["editor.foreground"], "#BDB1A4");
  assert.equal(dark.colors["sideBar.foreground"], "#BDB1A4");
  assert.equal(dark.colors["terminal.foreground"], "#BDB1A4");
  assert.equal(dark.colors["tab.activeForeground"], "#D8CDC0");

  const variables = dark.tokenColors?.find((token) => token.name === "Variables");
  assert.equal(variables?.settings?.foreground, "#BDB1A4");
  assert.equal(dark.semanticTokenColors?.variable, "#BDB1A4");
});

test("status bar stays visually quiet instead of becoming a heavy bottom band", () => {
  const expectedStatusBarColors: Record<string, Record<string, string>> = {
    "Paperglow Light": {
      "statusBar.background": "#E8DED2",
      "statusBar.foreground": "#4A4038",
      "statusBar.border": "#D8CABD",
      "statusBar.noFolderBackground": "#E3D6C8",
      "statusBarItem.activeBackground": "#DCCAB8",
      "statusBarItem.errorBackground": "#E2B9AE",
      "statusBarItem.errorForeground": "#4A302B",
      "statusBarItem.focusBorder": "#BC6A3A",
      "statusBarItem.hoverBackground": "#DCCAB8",
      "statusBarItem.offlineBackground": "#E2B9AE",
      "statusBarItem.offlineForeground": "#4A302B",
      "statusBarItem.prominentBackground": "#E3D6C8",
      "statusBarItem.prominentForeground": "#4A4038",
      "statusBarItem.prominentHoverBackground": "#DCCAB8",
      "statusBarItem.remoteBackground": "#E3D6C8",
      "statusBarItem.remoteForeground": "#4A4038",
      "statusBarItem.warningBackground": "#E7CDA8",
      "statusBarItem.warningForeground": "#4A4038",
    },
    "Paperglow Dark": {
      "statusBar.background": "#2D2926",
      "statusBar.foreground": "#D8CDC0",
      "statusBar.border": "#3C3936",
      "statusBar.noFolderBackground": "#2B2825",
      "statusBarItem.hoverBackground": "#3A302B",
    },
  };

  for (const [label, expectedColors] of Object.entries(expectedStatusBarColors)) {
    const theme = readContributedTheme(label);
    assert.ok(theme.colors, `${label} should define workbench colors`);

    for (const [colorName, expectedColor] of Object.entries(expectedColors)) {
      assert.equal(theme.colors[colorName], expectedColor, `${label} ${colorName}`);
    }
  }
});

test("theme files cover baseline syntax scopes for writing and Markdown reading", () => {
  const requiredScopeGroups = [
    ["comment"],
    ["string"],
    ["keyword", "storage.type"],
    ["entity.name.function", "support.function"],
    ["entity.name.type", "entity.name.class", "support.type"],
    ["variable", "identifier"],
    ["constant", "constant.numeric"],
    ["markup.heading"],
    ["markup.underline.link", "string.other.link"],
    ["markup.quote"],
    ["markup.inline.raw", "markup.raw.block"],
  ];

  for (const label of ["Paperglow Light", "Paperglow Dark"]) {
    const theme = readContributedTheme(label);
    assert.ok(theme.tokenColors?.length, `${label} should define TextMate token colors`);
    const scopes = new Set(
      theme.tokenColors.flatMap((token) =>
        typeof token.scope === "string" ? [token.scope] : token.scope ?? [],
      ),
    );

    for (const group of requiredScopeGroups) {
      assert.ok(
        group.some((scope) => scopes.has(scope)),
        `${label} should define one of these scopes: ${group.join(", ")}`,
      );
    }
  }
});

test("docs and package metadata describe the complete theme plus preview workflow", () => {
  const packageJson = readPackageJson();
  const readme = readFileSync(readmePath, "utf8");
  const vscodeIgnore = readFileSync(vscodeIgnorePath, "utf8");

  assert.ok(packageJson.keywords?.includes("theme"));
  assert.ok(packageJson.keywords?.includes("paperglow"));
  assert.ok(packageJson.keywords?.includes("markdown-preview"));
  assert.equal(packageJson.scripts?.["package:vsix"], "vsce package --out paperglow-theme.vsix");

  assert.match(readme, /Paperglow Light/);
  assert.match(readme, /Paperglow Dark/);
  assert.match(readme, /Color Theme/);
  assert.match(readme, /built-in Markdown preview/i);
  assert.doesNotMatch(readme, /Open Paperglow Preview/);
  assert.doesNotMatch(readme, /custom Webview/i);
  assert.doesNotMatch(readme, /owns only the preview Webview/i);
  assert.doesNotMatch(readme, /Product Boundary/i);
  assert.doesNotMatch(vscodeIgnore, /^themes\//m);
  assert.doesNotMatch(vscodeIgnore, /^media\//m);
});
