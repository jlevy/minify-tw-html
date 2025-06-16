# minify-tw-html

This is a convenient CLI and Python lib wrapper for
[html-minifier-terser](https://github.com/terser/html-minifier-terser) (the highly
configurable, well-tested, JavaScript-based HTML minifier) and the
[Tailwind v4 CLI](https://tailwindcss.com/docs/installation/tailwind-cli) (the recently
updated Tailwind compiler).

## Simple, Modern Minification of Static HTML/CSS/JavaScript Pages

This is a convenient CLI and Python library to fully minify HTML, CSS, and JavaScript
using html-minifier-terser one of the best modern minifiers.

If you’re using Python, it can be added as a PyPI dependency to a project and used as a
minification library from Python and it internally handles (and caches) the Node
dependencies.

Once it is installed, you can just use it on static files with a single command, with no
package.json or npm project setup!

Internally, it checks for an npm installation and uses that, raising an error if not
available.
Once it finds npm, it does its own internal `npm install` of required tools so
it’s self-contained.
The required npm packages are installed locally within the Python site-packages
directory.

### Simple Tailwind v4 Compilation

In addition to general minification, minify-tw-html also compiles Tailwind CSS v4.

You might think Tailwind v4 compilation would be a simple operation, like a single CLI
command, but it’s not quite that simple.
The modern Tailwind CLI seems to assume you have a full hot-reloading JavaScript app
setup. This is great if you do, but quite inconvenient if you don’t want a build process
and just want to compile and minify a static page.

Simple static page development is easy via the
[Play CDN](https://tailwindcss.com/docs/installation/play-cdn).
To do this, you put a tag like `<script
src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>` in your code.

However, that setup is not recommended by Tailwind for production use due to its poor
performance (scanning the whole page at load time to find Tailwind classes).

This tool helps if you want to use Tailwind as a sort of “drop in” to static web pages
so it works with zero build, using the script tag.
If you then run minify-tw-html, it will detect the Tailwind CDN script and compile and
inline the production Tailwind CSS necessary for your page (and then minify everything
else, including HTML and JavaScript).

## Are There Alternatives?

Previously I had been using the [minify-html](https://github.com/wilsonzlin/minify-html)
(which has a convenient [Python package](https://pypi.org/project/minify-html/)) for
general minification.
It is great and fast.
But I found I kept running into
[issues](https://github.com/wilsonzlin/minify-html/issues/236) and in any case wanted
proper Tailwind v4 compilation, so switched to this of combining Tailwind compilation
with robust HTML/CSS/JS minification.

## Installation

I recommend you [use uv](installation.md):

```shell
uv tool install --upgrade minify-tw-html
```

## Example Usage

```shell
$ minify-tw-html --help
usage: minify-tw-html [-h] [--version] [--no_minify] [--preflight] [--tailwind] [--verbose] src_html dest_html

HTML minification with Tailwind CSS v4 compilation

positional arguments:
  src_html       Input HTML file.
  dest_html      Output HTML file.

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
  --no_minify    Skip HTML minification (only compile Tailwind if present).
  --preflight    Enable Tailwind's preflight CSS reset (disabled by default to preserve custom styles).
  --tailwind     Force Tailwind CSS compilation even if CDN script is not present.
  --verbose, -v  Enable verbose logging.

CLI for HTML minification with Tailwind CSS v4 compilation.

This script can be used for general HTML minification (including inline CSS/JS) and/or
Tailwind CSS v4 compilation and inlining (replacing CDN script with compiled CSS).

Minification includes:
- HTML structure: whitespace removal, comment removal
- Inline CSS: all <style> tags and style attributes are minified
- Inline JavaScript: all <script> tags are minified (not external JS files)

minify-tw-html v0.1.3.dev4+d976d28
```

Now take a file you want to minimize.
Let’s put this file into `page.html`. Note we are using the Play CDN for simple
zero-build development:

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
$ minify-tw-html page.html page.min.html --verbose
Tailwind v4 CDN script detected: will compile and inline Tailwind CSS
Found 1 <style> tags in body size 1091 bytes, returning CSS of size 245 bytes
Tailwind input CSS:
   @import "tailwindcss";
   @source "/Users/levy/wrk/github/minify-tw-html/page.html";
           /* Custom CSS that will be minified alongside Tailwind */
           .custom-shadow { 
               box-shadow:…
Tailwind config: /Users/levy/wrk/github/minify-tw-html/tmp4g35wsgu/tailwind.config.js:
   module.exports = {
     "content": [
       "page.html"
     ],
     "corePlugins": {
       "preflight": false
     },
     "theme": {
       "extend": {}
     },
     "plugins": []
   };
Running: npx @tailwindcss/cli --input - --output /Users/levy/wrk/github/minify-tw-html/tmp4g35wsgu/tailwind.min.css --config /Users/levy/wrk/github/minify-tw-html/tmp4g35wsgu/tailwind.config.js --minify
Tailwind stderr: ≈ tailwindcss v4.1.8

Done in 54ms

Tailwind CSS v4 compiled and inlined successfully
Minifying HTML (including inline CSS and JS)...
Running: npx html-minifier-terser --collapse-whitespace --remove-comments --minify-css true --minify-js true -o /Users/levy/wrk/github/minify-tw-html/page.min.htmlk5geeie0v48wv.partial /Users/levy/wrk/github/minify-tw-html/page.mindwa99o7p.html
HTML minified and written: page.min.html
Tailwind CSS compiled, HTML minified: 1091 bytes → 6893 bytes (+531.8%) in 1s

$ cat page.min.html 
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Test HTML</title><style>/*! tailwindcss v4.1.8 | MIT License | https://tailwindcss.com */@layer properties{@supports (((-webkit-hyphens:none)) and (not (margin-trim:inline))) or ((-moz-orient:inline) and (not (color:rgb(from red r g b)))){*,::backdrop,:after,:before{--tw-font-weight:initial;--tw-duration:initial}}}@layer theme{:host,:root{--font-sans:ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";--font-mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;--color-blue-500:oklch(62.3% .214 259.815);--color-blue-600:oklch(54.6% .245 262.881);--color-blue-700:oklch(48.8% .243 264.376);--color-gray-50:oklch(98.5% .002 247.839);--color-gray-100:oklch(96.7% .003 264.542);--color-gray-700:oklch(37.3% .034 259.733);--color-white:#fff;--spacing:.25rem;--text-2xl:1.5rem;--text-2xl--line-height:calc(2/1.5);--font-weight-bold:700;--radius-lg:.5rem … .custom-shadow{box-shadow:0 4px 8px #0000001a}@property --tw-font-weight{syntax:"*";inherits:false}@property --tw-duration{syntax:"*";inherits:false}</style></head><body class="m-0 p-5 bg-gray-50"><div class="custom-shadow bg-gray-100 p-4 m-2 rounded-lg"><h1 class="text-2xl font-bold text-blue-600 mb-3">Test Header</h1><p class="text-gray-700 mb-4">This is a test paragraph with some content.</p><button onclick="testFunction()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200">Click Me</button></div><script>function testFunction(){return console.log("Hello from test function!"),alert("Button was clicked!"),"Some return value"}</script></body></html>…
```

(Last output truncated for clarity.)

Note because of the Tailwind compilation this page actually grew because we’ve compiled
in the CSS for instant loading (for large pages it is more likely to shrink).

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
