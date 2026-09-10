import html


def render_legacy_text(value: str) -> str:
    """Legacy diary HTML is treated as untrusted text until sanitization is added."""
    return html.escape(value, quote=False)
