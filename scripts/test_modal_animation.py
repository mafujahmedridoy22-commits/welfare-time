import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STYLE_CSS = os.path.join(REPO_ROOT, "static", "assets", "style.css")
BASEOF_HTML = os.path.join(REPO_ROOT, "layouts", "_default", "baseof.html")

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def test_modal_animation():
    """モーダルが開くときのアニメーションが実際に再生されることを検証する。

    .animate-in が animation-duration / animation-timing-function を持たないと、
    animation-duration の既定値 0s のためアニメーションは一瞬で終わる。
    また duration-200 は transition-duration を指すので、アニメーションには効かない。
    """
    failures = []

    style = read(STYLE_CSS)
    m = re.search(r"\.animate-in\s*\{[^}]*\}", style)
    if not m:
        failures.append(".animate-in rule not found in style.css")
    else:
        block = m.group(0)
        if "animation-duration: 200ms" not in block:
            failures.append(".animate-in must set animation-duration: 200ms")
        if "animation-timing-function: ease-out" not in block:
            failures.append(".animate-in must set animation-timing-function: ease-out")

    baseof = read(BASEOF_HTML)
    for modal_id in ("filterModal", "sortModal", "statusModal", "qrModal"):
        m = re.search(r'<div id="%s"[^>]*class="[^"]*"' % modal_id, baseof)
        if not m:
            failures.append(f"{modal_id} not found in baseof.html")
            continue
        classes = m.group(0)
        if "animate-in" not in classes:
            failures.append(f"{modal_id} must use animate-in")
        if "duration-200" in classes:
            failures.append(f"{modal_id} must not carry the ineffective duration-200")

    if failures:
        raise AssertionError("\n  - " + "\n  - ".join(failures))

    print("Regression test passed: modal animations have a real duration and no dead duration-200.")

if __name__ == "__main__":
    try:
        test_modal_animation()
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
