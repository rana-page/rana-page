THEE RANA PAGE
==============

Source for my website, a [Quarto](https://quarto.org) site. The layout and
behaviour are a port of [Vaibhav Sagar's Hakyll site](https://github.com/vaibhavsagar/website).

## Working on it

```sh
quarto preview        # live-reloading local server
quarto render         # build everything into _site/
```

Quarto is the only tool you need (`brew install --cask quarto`).

## Writing

Posts live in `blog/<slug>/index.qmd` and are served at `/blog/<slug>/`.
`scripts/new-post.sh my-slug "My Title"` creates the skeleton (`--draft` puts
it in `drafts/`):

```markdown
---
title: "A Post"
date: 2026-01-31
categories: [programming, haskell]
---

Body in Pandoc/Quarto markdown. Fenced code with a language gets highlighted.
```

- Put a post in `drafts/<slug>/index.qmd` with `draft: true` to have it rendered
  at `/drafts/<slug>/` without being listed anywhere or in the feed. Move it to
  `blog/` and drop the `draft` line to publish.
- Images go next to the post and are referenced relatively, or in `images/`.
- The home page shows the 20 most recent posts, `/archive/` shows all of them
  with a tag filter, and the RSS feed (last 10) is at `/index.xml`.

## Before going live

Search `_quarto.yml` for `TODO`: set `site-url` to the real domain. The
`about/` and `talks/` pages are placeholders.

Deployment: `.github/workflows/publish.yml` renders and pushes to the
`gh-pages` branch on every push to `main`. One-time setup, per the
[Quarto docs](https://quarto.org/docs/publishing/github-pages.html):

1. Run `quarto publish gh-pages` locally once. It creates the branch and a
   `_publish.yml` file; commit that file.
2. In the repo's Settings → Actions → General, set Workflow permissions to
   "Read and write".
3. In Settings → Pages, make sure the source is the `gh-pages` branch.

For a custom domain, add a `CNAME` file at the project root and uncomment it
under `project.resources` in `_quarto.yml` (same for `.well-known/`).
