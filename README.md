> **Moved (2026-11-08):** the plans now live in [bensonlabs/projects](https://github.com/bensonlabs/projects)
> under `site/workouts/`, with this history. Justin's plan is at bensonlabs.org/projects/workouts/justin/,
> the CL plan at /projects/workouts/cl/, and /projects/workouts/ lists every plan. This repo is archived.

# Workouts

Source repository for the workout plans published on [bensonlabs.org](https://bensonlabs.org/projects/workouts/).

## Plans

| Plan | Source file | Published route | Status |
|---|---|---|---|
| Justin | `justin/index.html` | [/projects/workouts/](https://bensonlabs.org/projects/workouts/) | Live |
| CL Strength Restart | `cl/index.html` | [/projects/workouts/cl/](https://bensonlabs.org/projects/workouts/cl/) | Live |

Each plan is a self-contained, mobile-first HTML document. It has no build dependencies and can be opened directly in a browser for local preview.

## Publishing

This repository publishes the plans as versioned releases; the
[bensonlabs/blog](https://github.com/bensonlabs/blog) pins one release and puts it on bensonlabs.org.

1. Edit a plan here and merge it to `main`. CI packs both pages as a check.
2. Tag a version, such as `v1.0.1`. The release workflow publishes `workouts-v1.0.1.tar.gz` and its sha256.
3. In the blog, `python3 .github/scripts/components.py bump workouts v1.0.1` pins that release in
   `_data/components.json`. Merging that PR deploys the site.

Justin's plan (`justin/index.html`) is published at `/projects/workouts/`, and the restart plan
(`cl/index.html`) at `/projects/workouts/cl/`. Both stay standalone pages here; the blog wraps them in
its site header. To see what a release contains, run `python3 tools/pack.py` and open `dist/projects/workouts/`.

Edit plans in this repository, never in the blog: its `projects/workouts/` folder is filled in at build time.
