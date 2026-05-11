export type MarkdownFeatureStatus = "supported" | "deferred" | "unsupported";

export interface MarkdownFeatureSupport {
  heading: MarkdownFeatureStatus;
  paragraph: MarkdownFeatureStatus;
  blockquote: MarkdownFeatureStatus;
  list: MarkdownFeatureStatus;
  taskList: MarkdownFeatureStatus;
  table: MarkdownFeatureStatus;
  codeBlock: MarkdownFeatureStatus;
  image: MarkdownFeatureStatus;
  link: MarkdownFeatureStatus;
  horizontalRule: MarkdownFeatureStatus;
  frontmatter: MarkdownFeatureStatus;
  mermaid: MarkdownFeatureStatus;
  math: MarkdownFeatureStatus;
  obsidianCallout: MarkdownFeatureStatus;
  customContainer: MarkdownFeatureStatus;
}

export function getMarkdownFeatureSupport(): MarkdownFeatureSupport {
  return {
    heading: "supported",
    paragraph: "supported",
    blockquote: "supported",
    list: "supported",
    taskList: "supported",
    table: "supported",
    codeBlock: "supported",
    image: "supported",
    link: "supported",
    horizontalRule: "supported",
    frontmatter: "deferred",
    mermaid: "deferred",
    math: "deferred",
    obsidianCallout: "deferred",
    customContainer: "deferred",
  };
}
