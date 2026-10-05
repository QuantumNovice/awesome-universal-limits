// A deliberately small Markdown renderer for the explainers: headings, paragraphs,
// lists, bold, italics, inline code and links. Input is escaped first.

export const REPO = "https://github.com/QuantumNovice/awesome-universal-limits";

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function resolveLink(href: string): string {
  if (/^https?:\/\//.test(href)) return href;
  if (href.startsWith("#")) return href;
  // explainer-relative repo path, e.g. ../../data/spin.csv
  const parts = ["docs", "explainers"];
  for (const seg of href.split("/")) {
    if (seg === "..") parts.pop();
    else if (seg !== ".") parts.push(seg);
  }
  return `${REPO}/blob/main/${parts.join("/")}`;
}

function inline(s: string): string {
  let out = escapeHtml(s);
  out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, text: string, href: string) => {
    const url = resolveLink(href.replace(/&amp;/g, "&"));
    return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${text}</a>`;
  });
  return out;
}

export function renderMarkdown(md: string): string {
  const lines = md.replace(/\r/g, "").split("\n");
  const html: string[] = [];
  let para: string[] = [];
  let list: { ordered: boolean; items: string[] } | null = null;

  const flushPara = () => {
    if (para.length) html.push(`<p>${inline(para.join(" "))}</p>`);
    para = [];
  };
  const flushList = () => {
    if (list) {
      const tag = list.ordered ? "ol" : "ul";
      html.push(`<${tag}>${list.items.map((i) => `<li>${inline(i)}</li>`).join("")}</${tag}>`);
    }
    list = null;
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    const h = /^(#{1,4})\s+(.*)$/.exec(line);
    const ul = /^\s*[-*]\s+(.*)$/.exec(line);
    const ol = /^\s*\d+\.\s+(.*)$/.exec(line);
    if (h) {
      flushPara();
      flushList();
      const level = Math.min(h[1].length + 1, 4);
      html.push(`<h${level}>${inline(h[2])}</h${level}>`);
    } else if (ul || ol) {
      flushPara();
      const ordered = Boolean(ol);
      if (!list || list.ordered !== ordered) {
        flushList();
        list = { ordered, items: [] };
      }
      list.items.push((ul ?? ol)![1]);
    } else if (/^\s+\S/.test(line) && list) {
      list.items[list.items.length - 1] += " " + line.trim();
    } else if (line.trim() === "") {
      flushPara();
      flushList();
    } else {
      flushList();
      para.push(line.trim());
    }
  }
  flushPara();
  flushList();
  return html.join("\n");
}
