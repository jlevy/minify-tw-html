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

## CLI Use

Save a file like this for example as `page.html`. Note we are using the Play CDN for
simple zero-build development:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test HTML</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        /* Custom CSS that will be minified alongside Tailwind */
        .custom-shadow { 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
        }
    </style>
</head>
<body class="m-0 p-5 bg-gray-50">

<!-- This comment should be removed -->

<div class="custom-shadow bg-gray-100 p-4 m-2 rounded-lg">
  <h1 class="text-2xl font-bold text-blue-600 mb-3">Test Header</h1>
  <p class="text-gray-700 mb-4">This is a test paragraph with some content.</p>
  <button 
      onclick="testFunction()" 
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200">
      Click Me
  </button>
</div>
<script>
  // This JavaScript should get minified
  function testFunction() {
      console.log('Hello from test function!');
      alert('Button was clicked!');
      return 'Some return value';
  }
</script>
</body>
</html>
```

If you want to minify it and compile all Tailwind CSS:

```shell
$ minify-tw-html --help
usage: minify-tw-html [-h] [--no-minify] [--verbose] src_html dest_html

CLI for HTML minification with Tailwind CSS v4 compilation.

This script can be used for general HTML minification (including inline CSS/JS) and/or
Tailwind CSS v4 compilation and inlining (replacing CDN script with compiled CSS).

Minification includes:
- HTML structure: whitespace removal, comment removal
- Inline CSS: all <style> tags and style attributes are minified
- Inline JavaScript: all <script> tags are minified (not external JS files)

positional arguments:
  src_html       Input HTML file.
  dest_html      Output HTML file.

options:
  -h, --help     show this help message and exit
  --no-minify    Skip HTML minification (only compile Tailwind if present).
  --verbose, -v  Enable verbose logging.

$ minify-tw-html page.html page.min.html --verbose
Tailwind v4 CDN script detected - will compile and inline Tailwind CSS
Installing npm dependencies...
Running: npm install
Running: npx @tailwindcss/cli -i [...]/input.css -o [...]/tailwind.min.css --minify
Tailwind stderr: ≈ tailwindcss v4.1.8

Done in 21ms

Tailwind CSS v4 compiled and inlined successfully
Minifying HTML (including inline CSS and JS)...
Running: npx html-minifier-terser --collapse-whitespace --remove-comments --minify-css true --minify-js true -o [...]/page.min.html [...]/tmpf8bfzeic.html
HTML minified and written to page.min.html
Tailwind CSS compiled, HTML minified: 1223 bytes → 4680 bytes (+282.7%)

$ cat page.min.html 
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Test HTML</title><style>/*! tailwindcss v4.1.8 | MIT License | https://tailwindcss.com */@layer theme{:host,:root{--font-sans:ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";--font-mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;--default-font-family:var(--font-sans);--default-mono-font-family:var(--font-mono)}}@layer base{*,::backdrop,:after,:before{box-sizing:border-box;border:0 solid;margin:0;padding:0}::file-selector-button{box-sizing:border-box;border:0 solid;margin:0;padding:0}:host,html{-webkit-text-size-adjust:100%;tab-size:4;line-height:1.5;font-family:var(--default-font-family,ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji");font-feature-settings:var(--default-font-feature-settings,normal);font-variation-settings:var(--default-font-variation-settings,normal);-webkit-tap-highlight-color:transparent}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;-webkit-text-decoration:inherit;-webkit-text-decoration:inherit;-webkit-text-decoration:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,pre,samp{font-family:var(--default-mono-font-family,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace);font-feature-settings:var(--default-mono-font-feature-settings,normal);font-variation-settings:var(--default-mono-font-variation-settings,normal);font-size:1em}small{font-size:80%}sub,sup{vertical-align:baseline;font-size:75%;line-height:0;position:relative}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}:-moz-focusring{outline:auto}progress{vertical-align:baseline}summary{display:list-item}menu,ol,ul{list-style:none}audio,canvas,embed,iframe,img,object,svg,video{vertical-align:middle;display:block}img,video{max-width:100%;height:auto}button,input,optgroup,select,textarea{font:inherit;font-feature-settings:inherit;font-variation-settings:inherit;letter-spacing:inherit;color:inherit;opacity:1;background-color:#0000;border-radius:0}::file-selector-button{font:inherit;font-feature-settings:inherit;font-variation-settings:inherit;letter-spacing:inherit;color:inherit;opacity:1;background-color:#0000;border-radius:0}:where(select:is([multiple],[size])) optgroup{font-weight:bolder}:where(select:is([multiple],[size])) optgroup option{padding-inline-start:20px}::file-selector-button{margin-inline-end:4px}::placeholder{opacity:1}@supports (not ((-webkit-appearance:-apple-pay-button))) or (contain-intrinsic-size:1px){::placeholder{color:currentColor}@supports (color:color-mix(in lab,red,red)){::placeholder{color:color-mix(in oklab,currentcolor 50%,transparent)}}}textarea{resize:vertical}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-date-and-time-value{min-height:1lh;text-align:inherit}::-webkit-datetime-edit{display:inline-flex}::-webkit-datetime-edit-fields-wrapper{padding:0}::-webkit-datetime-edit{padding-block:0}::-webkit-datetime-edit-year-field{padding-block:0}::-webkit-datetime-edit-month-field{padding-block:0}::-webkit-datetime-edit-day-field{padding-block:0}::-webkit-datetime-edit-hour-field{padding-block:0}::-webkit-datetime-edit-minute-field{padding-block:0}::-webkit-datetime-edit-second-field{padding-block:0}::-webkit-datetime-edit-millisecond-field{padding-block:0}::-webkit-datetime-edit-meridiem-field{padding-block:0}:-moz-ui-invalid{box-shadow:none}button,input:where([type=button],[type=reset],[type=submit]){appearance:button}::file-selector-button{appearance:button}::-webkit-inner-spin-button{height:auto}::-webkit-outer-spin-button{height:auto}[hidden]:where(:not([hidden=until-found])){display:none!important}}</style><style>.custom-shadow{box-shadow:0 4px 8px rgba(0,0,0,.1)}</style></head><body class="m-0 p-5 bg-gray-50"><div class="custom-shadow bg-gray-100 p-4 m-2 rounded-lg"><h1 class="text-2xl font-bold text-blue-600 mb-3">Test Header</h1><p class="text-gray-700 mb-4">This is a test paragraph with some content.</p><button onclick="testFunction()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200">Click Me</button></div><script>function testFunction(){return console.log("Hello from test function!"),alert("Button was clicked!"),"Some return value"}</script></body></html>
```

Note because of the Tailwind compilation this page actually grew because we've compiled
in the CSS for instant loading.
But for large pages it of course shrinks.

## Python Use

As a library: `uv add minify-tw-html` (or `pip install minify-tw-html` etc.). Then:

```python
from pathlib import Path
from minify_tw_html import minify_tw_html

minify_tw_html(Path("page.html"), Path("page.min.html"))
```

* * *

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
