from importlib.metadata import version

APP_NAME = "minify-tw-html"

DESCRIPTION = """HTML minification with Tailwind CSS v4 compilation"""


def get_version_name() -> str:
    """Get formatted version string"""
    try:
        app_version = version(APP_NAME)
        return f"{APP_NAME} v{app_version}"
    except Exception:
        return "(unknown version)"
