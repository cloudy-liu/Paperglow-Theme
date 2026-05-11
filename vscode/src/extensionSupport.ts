export interface DocumentInfo {
  languageId: string;
  fileName: string;
}

export function isMarkdownDocumentInfo(document: DocumentInfo): boolean {
  return (
    document.languageId === "markdown" ||
    /\.(md|markdown|mdown|mkdn)$/i.test(document.fileName)
  );
}

export function makePreviewTitle(fileName: string): string {
  return `${baseName(fileName)} Preview`;
}

export function baseName(fileName: string): string {
  const normalized = fileName.replaceAll("\\", "/");
  return normalized.split("/").filter(Boolean).pop() ?? fileName;
}

export function isExternalHref(href: string): boolean {
  return /^(https?:|mailto:)/i.test(href);
}
