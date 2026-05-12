import MarkdownIt from "markdown-it";
import taskLists from "markdown-it-task-lists";
import sanitizeHtml from "sanitize-html";

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
    html: true,
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
      return sanitizeRenderedHtml(markdownIt.render(markdown), options);
    },
  };
}

function sanitizeRenderedHtml(
  html: string,
  options: MarkdownRendererOptions,
): string {
  return sanitizeHtml(html, {
    allowedTags: [
      ...sanitizeHtml.defaults.allowedTags,
      "article",
      "aside",
      "details",
      "figcaption",
      "figure",
      "footer",
      "header",
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
      "hr",
      "img",
      "input",
      "main",
      "nav",
      "section",
      "summary",
      "table",
      "tbody",
      "td",
      "tfoot",
      "th",
      "thead",
      "tr",
    ],
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      a: ["href", "name", "target", "rel", "data-href", "title"],
      blockquote: ["cite"],
      code: ["class"],
      img: ["src", "alt", "title", "width", "height", "loading"],
      input: ["type", "checked", "disabled"],
      p: ["align"],
      pre: ["class"],
      table: ["align"],
      td: ["align", "colspan", "rowspan"],
      th: ["align", "colspan", "rowspan", "scope"],
    },
    allowedClasses: {
      code: [/^language-[\w-]+$/],
      pre: [/^language-[\w-]+$/],
    },
    allowedSchemes: [
      "http",
      "https",
      "mailto",
      "data",
      "safe-image",
      "safe-link",
      "vscode-resource",
      "vscode-webview-resource",
    ],
    transformTags: {
      a: (tagName, attribs) => {
        const href = attribs["data-href"] ?? attribs.href;
        if (!href) {
          return { tagName, attribs };
        }
        return {
          tagName,
          attribs: {
            ...attribs,
            href: options.resolveLinkHref ? options.resolveLinkHref(href) : href,
            "data-href": href,
            rel: "noopener noreferrer",
          },
        };
      },
      img: (tagName, attribs) => {
        const src = attribs.src;
        if (!src) {
          return { tagName, attribs };
        }
        const resolvedSrc = hasScheme(src)
          ? src
          : options.resolveImageSrc
            ? options.resolveImageSrc(src)
            : src;
        return {
          tagName,
          attribs: {
            ...attribs,
            src: resolvedSrc,
          },
        };
      },
    },
  });
}

function hasScheme(value: string): boolean {
  return /^[a-z][a-z0-9+.-]*:/i.test(value);
}
