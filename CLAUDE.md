# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal blog built with Quarto (`project.type: website`). It is a port of a Hakyll (Haskell) site; the design goal is to look and behave like the original: a 768px centred column, a bold brand left / nav right header with a 2px rule, Solarized-light code blocks, a plain `<a>title</a> - date` post list, and date-based "Posted on … / Tags: …" post headers. Keep changes within that aesthetic unless asked otherwise.

## Commands

```sh
quarto preview                 # dev server with live reload
quarto render                  # full build into _site/ (gitignored)
quarto render blog/foo/index.qmd   # one page (theme CSS is rebuilt too)
scripts/new-post.sh [--draft] <slug> ["Title"]   # new post skeleton
python3 scripts/import-hakyll-posts.py ../site   # re-import posts from the Hakyll tree
```

No tests or linters. `quarto render` prints `WARN`/`ERROR` lines for broken YAML or missing resources; a clean run prints only the page progress list.

## How the site fits together

- `_quarto.yml` is the only configuration. Content types are directories: `blog/<slug>/index.qmd`, `drafts/<slug>/index.qmd` (front matter `draft: true`, `draft-mode: unlinked` renders them but keeps them out of listings, the feed, sitemap and search), `about/`, `talks/`, `archive/`.
- Listings: `index.qmd` (20 newest, also generates the RSS feed `index.xml`) and `archive/index.qmd` (all posts, `categories: true`). Both use `templates/post-list.ejs`. That template must keep the `ul.list` wrapper and the base64 `data-categories` attribute on each `li`; Quarto's List.js filter reads them, and the category filter silently stops working without them.
- `templates/title-block.html` replaces Quarto's title block via `template-partials`. Keep `header.quarto-title-block` and `.quarto-category` in it: `includes/category-links.html` (an `include-after-body` script) wraps each tag in a link to `archive/#category=<tag>`. Quarto's own category linking is disabled because `search: false` suppresses the `quarto:offset` meta tag it depends on; if search is ever turned on, that script still takes precedence by checking for an existing `<a>`.
- `css/custom.scss` ports the original `default.css` on top of the `litera` Bootswatch theme. The block under `@media (min-width: 992px)` deliberately rewrites Quarto's page grid: pages that have a margin sidebar (the archive's category list) would otherwise push the body column off-centre, so the sidebar is moved into the body column above the content and the grid rows are set to `max-content` to avoid a gap.
- `css/solarized-light.theme` is a Pandoc highlight theme; it is the old `syntax.css` colours expressed as token styles. The original site highlighted Haskell with `ghc-syntax-highlighter`; Quarto uses Pandoc's skylighting lexer, so token classes differ slightly but the palette is the same.
- `includes/mathjax-config.html` loads the `color`, `cancel` and `textmacros` MathJax extensions; it is injected in `<head>` before the MathJax script tag, which is required for the config to apply.
- `scripts/import-hakyll-posts.py` documents every transformation applied to the imported posts (frontmatter fence, `published` → `date`, `tags` → `categories`, date-based internal links → `/blog/<slug>/`). The currently imported posts are the original author's and are expected to be deleted before the site goes live.

## Gotchas

- Links in listing templates come from `item.path`, which is the source path (`…/index.qmd`). The template strips `index.qmd` to produce clean directory URLs; Quarto would otherwise rewrite it to `index.html`.
- `site-url` in `_quarto.yml` is a placeholder; feed and sitemap URLs are wrong until it is set.
- Headless-Chrome screenshots at widths below about 500px clip the right edge because of a minimum window size, not because of a layout bug; verify narrow layouts inside an iframe instead.
