# minify-tw-html

This is a convenient CLI and Python lib wrapper for
[html-minifier-terser](https://github.com/terser/html-minifier-terser) (the highly
configurable, well-tested, JavaScript-based HTML minifier) and the
[Tailwind v4 CLI](https://tailwindcss.com/docs/installation/tailwind-cli).

- It lets you use the [Play CDN](https://tailwindcss.com/docs/installation/play-cdn) for
  rapid development, then lets you minify your HTML/CSS/JavaScript and Tailwind CSS with
  a single command.

- It can be added as a Python dependency to a Python project

- It can be used as a library from Python.

It checks for an npm installation and uses that, raising an error if not available.
If it finds npm it does its own `npm install` so it's self-contained.

Why?

It seems like modern minification and Tailwind v4 minification should be a simple
operation.

I had been using the [minify-html](https://github.com/wilsonzlin/minify-html) (which has
a convenient [Python package](https://pypi.org/project/minify-html/)) previously.
It is great and fast, but ran into some unfixed bugs and the need for Tailwind support,
so switched to this approach.

## Installation and Use

As a CLI: `uvx minify-tw-html --help`.

As a library: `uv add minify-tw-html` (or `pip install minify-tw-html` etc.).

* * *

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
