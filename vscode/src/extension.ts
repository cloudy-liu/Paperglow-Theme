import path from "node:path";

import * as vscode from "vscode";

import { createMarkdownRenderer } from "./markdownRenderer";
import { buildWebviewHtml } from "./webviewHtml";
import {
  baseName,
  isExternalHref,
  isMarkdownDocumentInfo,
  makePreviewTitle,
} from "./extensionSupport";

interface PreviewEntry {
  document: vscode.TextDocument;
  panel: vscode.WebviewPanel;
}

export function activate(context: vscode.ExtensionContext): void {
  const manager = new PaperglowPreviewManager(context);
  context.subscriptions.push(
    vscode.commands.registerCommand("paperglow.openPreview", () =>
      manager.openPreviewFromActiveEditor(),
    ),
    manager,
  );
}

export function deactivate(): void {
  // VS Code disposes subscriptions registered on the extension context.
}

class PaperglowPreviewManager implements vscode.Disposable {
  private readonly previews = new Map<string, PreviewEntry>();
  private readonly updateTimers = new Map<string, NodeJS.Timeout>();
  private readonly disposables: vscode.Disposable[] = [];

  constructor(private readonly context: vscode.ExtensionContext) {
    this.disposables.push(
      vscode.workspace.onDidChangeTextDocument((event) =>
        this.schedulePreviewUpdate(event.document),
      ),
    );
  }

  async openPreviewFromActiveEditor(): Promise<void> {
    const document = vscode.window.activeTextEditor?.document;

    if (!document || !isMarkdownDocumentInfo(document)) {
      void vscode.window.showInformationMessage(
        "Open a Markdown file before running Paperglow Preview.",
      );
      return;
    }

    await this.openPreview(document);
  }

  async openPreview(document: vscode.TextDocument): Promise<void> {
    const key = document.uri.toString();
    const existing = this.previews.get(key);
    if (existing) {
      existing.panel.reveal(vscode.ViewColumn.Active);
      this.updatePreview(existing);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      "paperglowPreview",
      makePreviewTitle(document.fileName),
      vscode.ViewColumn.Active,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [
          this.context.extensionUri,
          vscode.Uri.file(path.dirname(document.uri.fsPath)),
        ],
      },
    );

    const entry: PreviewEntry = { document, panel };
    this.previews.set(key, entry);

    panel.onDidDispose(
      () => {
        this.previews.delete(key);
        const timer = this.updateTimers.get(key);
        if (timer) {
          clearTimeout(timer);
          this.updateTimers.delete(key);
        }
      },
      undefined,
      this.disposables,
    );

    panel.webview.onDidReceiveMessage(
      (message: unknown) => this.handleWebviewMessage(entry, message),
      undefined,
      this.disposables,
    );

    this.updatePreview(entry);
  }

  dispose(): void {
    for (const timer of this.updateTimers.values()) {
      clearTimeout(timer);
    }
    this.updateTimers.clear();

    for (const disposable of this.disposables) {
      disposable.dispose();
    }
  }

  private schedulePreviewUpdate(document: vscode.TextDocument): void {
    const key = document.uri.toString();
    const entry = this.previews.get(key);
    if (!entry) {
      return;
    }

    const existingTimer = this.updateTimers.get(key);
    if (existingTimer) {
      clearTimeout(existingTimer);
    }

    const timer = setTimeout(() => {
      this.updateTimers.delete(key);
      this.updatePreview(entry);
    }, 120);
    this.updateTimers.set(key, timer);
  }

  private updatePreview(entry: PreviewEntry): void {
    const styleUri = entry.panel.webview.asWebviewUri(
      vscode.Uri.joinPath(this.context.extensionUri, "media", "paperglow-preview.css"),
    );
    const renderer = createMarkdownRenderer({
      resolveImageSrc: (src) => this.resolveImageSrc(src, entry.document, entry.panel.webview),
      resolveLinkHref: (href) => href,
    });

    const bodyHtml = renderer.render(entry.document.getText());
    entry.panel.title = makePreviewTitle(entry.document.fileName);
    entry.panel.webview.html = buildWebviewHtml({
      fileName: baseName(entry.document.fileName),
      bodyHtml,
      styleUri: styleUri.toString(),
      cspSource: entry.panel.webview.cspSource,
      nonce: createNonce(),
    });
  }

  private async handleWebviewMessage(
    entry: PreviewEntry,
    message: unknown,
  ): Promise<void> {
    if (!isRecord(message) || typeof message.type !== "string") {
      return;
    }

    if (message.type === "openSource") {
      await vscode.window.showTextDocument(entry.document, {
        viewColumn: entry.panel.viewColumn ?? vscode.ViewColumn.Active,
        preview: false,
      });
      entry.panel.dispose();
      return;
    }

    if (message.type === "openExternal" && typeof message.href === "string") {
      await this.openHref(message.href, entry.document);
    }
  }

  private async openHref(href: string, document: vscode.TextDocument): Promise<void> {
    if (isExternalHref(href)) {
      await vscode.env.openExternal(vscode.Uri.parse(href));
      return;
    }

    if (document.uri.scheme !== "file") {
      return;
    }

    const targetPath = path.resolve(path.dirname(document.uri.fsPath), stripHash(href));
    try {
      const targetDocument = await vscode.workspace.openTextDocument(vscode.Uri.file(targetPath));
      await vscode.window.showTextDocument(targetDocument, vscode.ViewColumn.Active);
    } catch {
      void vscode.window.showWarningMessage(`Unable to open link: ${href}`);
    }
  }

  private resolveImageSrc(
    src: string,
    document: vscode.TextDocument,
    webview: vscode.Webview,
  ): string {
    if (/^(https?:|data:|vscode-resource:|vscode-webview-resource:)/i.test(src)) {
      return src;
    }

    if (document.uri.scheme !== "file") {
      return src;
    }

    const [pathPart, suffix] = splitResourceSuffix(src);
    const targetPath = path.isAbsolute(pathPart)
      ? pathPart
      : path.resolve(path.dirname(document.uri.fsPath), pathPart);

    return `${webview.asWebviewUri(vscode.Uri.file(targetPath)).toString()}${suffix}`;
  }
}

function createNonce(): string {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let nonce = "";
  for (let index = 0; index < 32; index += 1) {
    nonce += alphabet[Math.floor(Math.random() * alphabet.length)];
  }
  return nonce;
}

function splitResourceSuffix(src: string): [string, string] {
  const match = src.match(/^([^?#]*)([?#].*)?$/);
  if (!match) {
    return [src, ""];
  }
  return [match[1] ?? src, match[2] ?? ""];
}

function stripHash(href: string): string {
  return href.split("#", 1)[0] || href;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
