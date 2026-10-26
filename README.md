# Workouts

Source repository for the workout plans published on [bensonlabs.org](https://bensonlabs.org/projects/workouts/).

## Plans

| Person | Source file | Published route | Status |
|---|---|---|---|
| Justin | `justin/index.html` | [/projects/workouts/](https://bensonlabs.org/projects/workouts/) | Live |
| Carlos | `carlos/index.html` | [/projects/workouts/carlos/](https://bensonlabs.org/projects/workouts/carlos/) | Live |

Each plan is a self-contained, mobile-first HTML document. It has no build dependencies and can be opened directly in a browser for local preview.

## Publishing

The [bensonlabs/blog](https://github.com/bensonlabs/blog) Pages workflow checks out this public repository during its build.

- Justin's file is converted into the blog's Jekyll `project` layout and published at `/projects/workouts/`.
- Carlos's file is converted into the same layout and published at `/projects/workouts/carlos/`.
- A push here does not trigger the blog deployment automatically. After changing Justin's plan, run **Deploy Jekyll to GitHub Pages** from the blog repository's Actions tab, or make a normal commit to the blog repository.

Edit plans in this repository, never in the temporary `projects/workouts/` directory created inside the blog build workspace.
