import re
import subprocess
import tempfile
from pathlib import Path


def test_cli_html_minification_with_percentage():
    """Test CLI minification of HTML with percentage reduction logging."""

    # Create test HTML content
    test_html = """<!DOCTYPE html>
<html>
<head>
    <title>Test HTML</title>
    <style>
        body { margin: 0; padding: 20px; }
        .test-class { 
            background-color: #f0f0f0; 
            padding: 10px; 
            margin: 5px; 
        }
    </style>
</head>
<body>
    <!-- This comment should be removed -->
    <div class="test-class">
        <h1>Test Header</h1>
        <p>This is a test paragraph with some content.</p>
        <button onclick="testFunction()">Click Me</button>
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
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input file
        input_file = Path(tmpdir) / "test_input.html"
        output_file = Path(tmpdir) / "test_output.html"

        input_file.write_text(test_html, encoding="utf8")
        initial_size = input_file.stat().st_size

        # Run the CLI
        result = subprocess.run(
            ["uv", "run", "minify-tw-html", str(input_file), str(output_file), "--verbose"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,  # Run from project root
        )

        # Check command succeeded
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"

        # Check output file exists and is smaller
        assert output_file.exists(), "Output file was not created"
        final_size = output_file.stat().st_size
        assert final_size < initial_size, "Output file should be smaller than input"

        # Check percentage logging is present in output
        output_text = result.stderr
        percentage_pattern = r"HTML minified: \d+ bytes → \d+ bytes \(-\d+\.\d+%\)"
        assert re.search(percentage_pattern, output_text), (
            f"Expected percentage logging not found in: {output_text}"
        )

        # Verify content was actually minified (no comments, compressed)
        output_content = output_file.read_text(encoding="utf8")
        assert "<!-- This comment should be removed -->" not in output_content
        assert len(output_content.strip()) > 0

        # Verify CSS and JS were minified (check for compressed formatting)
        assert "margin:0;padding:20px" in output_content or "margin:0" in output_content


def test_cli_tailwind_compilation_with_percentage():
    """Test CLI Tailwind CSS compilation with percentage increase logging."""

    # Create test HTML with Tailwind CDN
    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailwind Test</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
    <div class="bg-blue-500 text-white p-4 rounded-lg">
        <h1 class="text-2xl font-bold">Hello Tailwind!</h1>
        <p class="text-sm opacity-80">Testing Tailwind compilation.</p>
    </div>
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input file
        input_file = Path(tmpdir) / "test_tailwind.html"
        output_file = Path(tmpdir) / "test_tailwind_output.html"

        input_file.write_text(test_html, encoding="utf8")
        initial_size = input_file.stat().st_size

        # Run the CLI
        result = subprocess.run(
            ["uv", "run", "minify-tw-html", str(input_file), str(output_file), "--verbose"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,  # Run from project root
        )

        # Check command succeeded
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"

        # Check output file exists and is larger (due to compiled CSS)
        assert output_file.exists(), "Output file was not created"
        final_size = output_file.stat().st_size
        assert final_size > initial_size, (
            "Output file should be larger due to compiled Tailwind CSS"
        )

        # Check percentage logging shows increase
        output_text = result.stderr
        percentage_pattern = (
            r"Tailwind CSS compiled, HTML minified: \d+ bytes → \d+ bytes \(\+\d+\.\d+%\)"
        )
        assert re.search(percentage_pattern, output_text), (
            f"Expected Tailwind percentage logging not found in: {output_text}"
        )

        # Verify Tailwind CDN script was replaced with compiled CSS
        output_content = output_file.read_text(encoding="utf8")
        assert "@tailwindcss/browser" not in output_content, (
            "Tailwind CDN script should be replaced"
        )
        assert "<style>" in output_content, "Compiled CSS should be present"
        assert "tailwindcss" in output_content.lower(), (
            "Tailwind CSS should be compiled and included"
        )


def test_cli_no_minify_option():
    """Test CLI --no-minify option preserves formatting while still compiling Tailwind."""

    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>No Minify Test</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
    <div class="bg-red-500 text-white p-2">
        <p>Test content</p>
    </div>
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "test_no_minify.html"
        output_file = Path(tmpdir) / "test_no_minify_output.html"

        input_file.write_text(test_html, encoding="utf8")

        # Run CLI with --no-minify
        result = subprocess.run(
            [
                "uv",
                "run",
                "minify-tw-html",
                str(input_file),
                str(output_file),
                "--no-minify",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert output_file.exists()

        # Should show Tailwind compilation but no minification
        output_text = result.stderr
        assert "Tailwind CSS compiled:" in output_text
        assert "no minification" in output_text

        # Verify percentage logging
        percentage_pattern = r"Tailwind CSS compiled: \d+ bytes → \d+ bytes \(\+\d+\.\d+%\)"
        assert re.search(percentage_pattern, output_text), (
            f"Expected no-minify percentage logging not found in: {output_text}"
        )


def test_cli_without_tailwind():
    """Test CLI with regular HTML that has no Tailwind (should just minify)."""

    test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Regular HTML Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .content {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <!-- This is a comment that should be removed -->
    <div class="content">
        <h1>Regular HTML Page</h1>
        <p>This page has no Tailwind CSS, just regular HTML/CSS/JS.</p>
        <button onclick="showAlert()">Click Me</button>
    </div>

    <script>
        function showAlert() {
            alert('Hello from regular JavaScript!');
            console.log('Button clicked');
        }
    </script>
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "test_regular.html"
        output_file = Path(tmpdir) / "test_regular_output.html"

        input_file.write_text(test_html, encoding="utf8")
        initial_size = input_file.stat().st_size

        # Run the CLI
        result = subprocess.run(
            ["uv", "run", "minify-tw-html", str(input_file), str(output_file), "--verbose"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert output_file.exists()

        final_size = output_file.stat().st_size
        assert final_size < initial_size, "Output should be smaller after minification"

        # Should NOT mention Tailwind, only HTML minification
        output_text = result.stderr
        assert "No Tailwind v4 CDN script found" in output_text
        assert "HTML minified:" in output_text
        assert "Tailwind CSS compiled" not in output_text

        # Verify percentage shows reduction
        percentage_pattern = r"HTML minified: \d+ bytes → \d+ bytes \(-\d+\.\d+%\)"
        assert re.search(percentage_pattern, output_text), (
            f"Expected HTML-only percentage logging not found in: {output_text}"
        )

        # Verify content was minified
        output_content = output_file.read_text(encoding="utf8")
        assert "<!-- This is a comment that should be removed -->" not in output_content
        assert "margin:0" in output_content  # CSS should be minified


def test_cli_with_older_tailwind_versions():
    """Test CLI with older Tailwind versions (v3, v2) - should be ignored and just minify HTML."""

    test_cases = [
        # Tailwind v3 CDN
        """<!DOCTYPE html>
<html>
<head>
    <title>Tailwind v3 Test</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div class="bg-blue-500 p-4">Old Tailwind v3</div>
</body>
</html>""",
        # Tailwind v2 CDN
        """<!DOCTYPE html>
<html>
<head>
    <title>Tailwind v2 Test</title>
    <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
    <div class="bg-red-500 p-4">Old Tailwind v2</div>
</body>
</html>""",
        # Generic Tailwind CSS link
        """<!DOCTYPE html>
<html>
<head>
    <title>Generic Tailwind Test</title>
    <link rel="stylesheet" href="https://cdn.tailwindcss.com/3.3.0/tailwind.min.css">
</head>
<body>
    <div class="bg-green-500 p-4">Generic Tailwind CSS</div>
</body>
</html>""",
    ]

    for i, test_html in enumerate(test_cases):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / f"test_old_tailwind_{i}.html"
            output_file = Path(tmpdir) / f"test_old_tailwind_output_{i}.html"

            input_file.write_text(test_html, encoding="utf8")
            initial_size = input_file.stat().st_size

            # Run the CLI
            result = subprocess.run(
                ["uv", "run", "minify-tw-html", str(input_file), str(output_file), "--verbose"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent,
            )

            assert result.returncode == 0, f"CLI failed on test case {i}: {result.stderr}"
            assert output_file.exists()

            final_size = output_file.stat().st_size
            assert final_size < initial_size, (
                f"Output should be smaller after minification for test case {i}"
            )

            # Should NOT detect Tailwind v4, should treat as regular HTML
            output_text = result.stderr
            assert "No Tailwind v4 CDN script found" in output_text, (
                f"Should not detect v4 in test case {i}"
            )
            assert "HTML minified:" in output_text, (
                f"Should show HTML minification for test case {i}"
            )
            assert "Tailwind CSS compiled" not in output_text, (
                f"Should not compile non-v4 Tailwind in test case {i}"
            )

            # Verify percentage shows reduction (HTML minification only)
            percentage_pattern = r"HTML minified: \d+ bytes → \d+ bytes \(-\d+\.\d+%\)"
            assert re.search(percentage_pattern, output_text), (
                f"Expected HTML-only percentage logging not found in test case {i}: {output_text}"
            )

            # Verify old Tailwind CDN/links are preserved (not replaced)
            output_content = output_file.read_text(encoding="utf8")
            if "cdn.tailwindcss.com" in test_html:
                assert "cdn.tailwindcss.com" in output_content, (
                    f"Old Tailwind CDN should be preserved in test case {i}"
                )
            elif "unpkg.com/tailwindcss@^2" in test_html:
                assert "unpkg.com/tailwindcss@^2" in output_content, (
                    f"Old Tailwind v2 CDN should be preserved in test case {i}"
                )
