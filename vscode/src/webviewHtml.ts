export interface WebviewHtmlOptions {
  fileName: string;
  bodyHtml: string;
  styleUri: string;
  cspSource: string;
  nonce: string;
}

export function buildWebviewHtml(options: WebviewHtmlOptions): string {
  const fileName = escapeHtml(options.fileName);
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
      <span class="pg-mode is-active" aria-current="page">Preview</span>
      <button class="pg-mode pg-mode-button" type="button" data-command="openSource">Markdown</button>
    </nav>
  </header>
  <main class="pg-preview-shell">
    <article class="pg-reading-card">
${options.bodyHtml}
    </article>
  </main>
  <script nonce="${escapeAttribute(options.nonce)}">
    const vscode = acquireVsCodeApi();
    document.addEventListener("click", (event) => {
      const target = event.target instanceof Element
        ? event.target.closest("[data-command], a[data-href]")
        : null;
      if (!target) {
        return;
      }
      if (target instanceof HTMLButtonElement && target.dataset.command === "openSource") {
        event.preventDefault();
        vscode.postMessage({ type: "openSource" });
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
