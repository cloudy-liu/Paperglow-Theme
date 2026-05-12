export interface WebviewHtmlOptions {
  fileName: string;
  bodyHtml: string;
  markdownText: string;
  styleUri: string;
  cspSource: string;
  nonce: string;
}

export function buildWebviewHtml(options: WebviewHtmlOptions): string {
  const fileName = escapeHtml(options.fileName);
  const markdownText = escapeHtml(options.markdownText);
  const csp = [
    "default-src 'none'",
    `img-src ${options.cspSource} https: data:`,
    `style-src ${options.cspSource}`,
    `font-src ${options.cspSource} https: data:`,
    `script-src 'nonce-${options.nonce}'`,
  ].join("; ");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="${csp}">
  <link rel="stylesheet" href="${escapeAttribute(options.styleUri)}">
  <title>${fileName} Preview</title>
</head>
<body>
  <header class="pg-doc-header" aria-label="Paperglow preview header">
    <div class="pg-file-identity" title="${fileName}">
      <span class="pg-md-icon" aria-hidden="true">M↓</span>
      <span class="pg-file-name">${fileName}</span>
    </div>
    <nav class="pg-mode-switch" aria-label="Markdown view mode">
      <button class="pg-mode pg-mode-button is-active" type="button" data-command="setMode" data-mode-target="preview" aria-pressed="true">Preview</button>
      <button class="pg-mode pg-mode-button" type="button" data-command="setMode" data-mode-target="markdown" aria-pressed="false">Markdown</button>
    </nav>
  </header>
  <main class="pg-preview-shell">
    <section class="pg-mode-panel pg-preview-panel" data-mode-panel="preview">
      <article class="pg-reading-card">
${options.bodyHtml}
      </article>
    </section>
    <section class="pg-mode-panel pg-markdown-panel" data-mode-panel="markdown" hidden>
      <pre class="pg-markdown-source" tabindex="0"><code>${markdownText}</code></pre>
    </section>
  </main>
  <script nonce="${escapeAttribute(options.nonce)}">
    const vscode = acquireVsCodeApi();
    const modeButtons = Array.from(document.querySelectorAll("[data-mode-target]"));
    const modePanels = Array.from(document.querySelectorAll("[data-mode-panel]"));

    function setMode(nextMode) {
      const mode = nextMode === "markdown" ? "markdown" : "preview";
      document.body.dataset.viewMode = mode;
      for (const button of modeButtons) {
        const active = button.dataset.modeTarget === mode;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", String(active));
      }
      for (const panel of modePanels) {
        panel.hidden = panel.dataset.modePanel !== mode;
      }
      vscode.setState({ mode });
    }

    const previousState = vscode.getState();
    setMode(previousState && previousState.mode === "markdown" ? "markdown" : "preview");

    document.addEventListener("click", (event) => {
      const target = event.target instanceof Element
        ? event.target.closest("[data-command], a[data-href]")
        : null;
      if (!target) {
        return;
      }
      if (target instanceof HTMLButtonElement && target.dataset.command === "setMode") {
        event.preventDefault();
        setMode(target.dataset.modeTarget);
        return;
      }
      if (target instanceof HTMLAnchorElement && target.dataset.href) {
        event.preventDefault();
        vscode.postMessage({ type: "openExternal", href: target.dataset.href });
      }
    });
  </script>
</body>
</html>`;
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value: string): string {
  return escapeHtml(value);
}
