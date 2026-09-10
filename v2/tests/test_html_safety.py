from mylife.html_safety import render_legacy_text


def test_legacy_html_is_not_executed():
    assert render_legacy_text("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
