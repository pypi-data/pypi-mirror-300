import gibson.core.Colors as Colors
from gibson.display.Header import Header


def test_render():
    text = "abc def ghi"
    assert Header().render(text) == (
        "///////////////////////////////// abc def ghi /////////////////////////////////"
    )
    assert Header().render(text, Colors.red) == (
        f"///////////////////////////////// {Colors.red(text)} /////////////////////////////////"
    )
