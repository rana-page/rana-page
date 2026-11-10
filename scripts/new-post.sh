#!/bin/sh
# Create a new post skeleton: scripts/new-post.sh my-post-slug "My Post Title"
# Add --draft to put it in drafts/ instead of blog/.
set -eu
dir=blog; draft=""
if [ "${1:-}" = "--draft" ]; then dir=drafts; draft="draft: true"; shift; fi
slug=${1:?usage: new-post.sh [--draft] <slug> [title]}
title=${2:-$(echo "$slug" | sed 's/-/ /g')}
root=$(cd "$(dirname "$0")/.." && pwd)
target="$root/$dir/$slug/index.qmd"
[ -e "$target" ] && { echo "$target already exists" >&2; exit 1; }
mkdir -p "$(dirname "$target")"
{
  echo "---"
  echo "title: \"$title\""
  echo "date: $(date +%Y-%m-%d)"
  echo "categories: []"
  [ -n "$draft" ] && echo "$draft"
  echo "---"
  echo
} > "$target"
echo "$target"
