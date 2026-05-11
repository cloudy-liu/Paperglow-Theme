import MarkdownIt from "markdown-it";
import taskLists from "markdown-it-task-lists";

export interface MarkdownRendererOptions {
  resolveImageSrc?: (src: string) => string;
  resolveLinkHref?: (href: string) => string;
}

export interface MarkdownRenderer {
  render(markdown: string): string;
}

export function createMarkdownRenderer(
  options: MarkdownRendererOptions = {},
): MarkdownRenderer {
  const markdownIt = new MarkdownIt({
    html: false,
    linkify: true,
    typographer: true,
  }).use(taskLists, {
    enabled: false,
    label: true,
    labelAfter: true,
  });

  const defaultImageRenderer =
    markdownIt.renderer.rules.image ??
    ((tokens, index, markdownOptions, env, self) =>
      self.renderToken(tokens, index, markdownOptions));

  markdownIt.renderer.rules.image = (tokens, index, markdownOptions, env, self) => {
    const token = tokens[index];
    const src = token.attrGet("src");
    if (src && options.resolveImageSrc) {
      token.attrSet("src", options.resolveImageSrc(src));
    }
    return defaultImageRenderer(tokens, index, markdownOptions, env, self);
  };

  markdownIt.renderer.rules.link_open = (tokens, index, markdownOptions, env, self) => {
    const token = tokens[index];
    const href = token.attrGet("href");
    if (href) {
      token.attrSet("data-href", href);
      token.attrSet("href", options.resolveLinkHref ? options.resolveLinkHref(href) : href);
      token.attrSet("rel", "noopener noreferrer");
    }
    return self.renderToken(tokens, index, markdownOptions);
  };

  return {
    render(markdown: string): string {
      return markdownIt.render(markdown);
    },
  };
}
