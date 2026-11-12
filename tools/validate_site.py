from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.anchors = []
        self.references = []
        self.images = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and values.get("href"):
            self.anchors.append(values["href"])
        if tag in {"img", "script", "link"}:
            key = "src" if tag in {"img", "script"} else "href"
            if values.get(key):
                self.references.append(values[key])
        if tag == "img":
            self.images.append(values)


def main():
    html = INDEX.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(html)
    errors = []
    if parser.h1 != 1:
        errors.append(f"Expected one h1, found {parser.h1}")
    for href in parser.anchors:
        if href.startswith("#") and href[1:] not in parser.ids:
            errors.append(f"Missing anchor target: {href}")
    for ref in parser.references:
        parsed = urlparse(ref)
        if parsed.scheme or ref.startswith("#"):
            continue
        if not (ROOT / parsed.path).exists():
            errors.append(f"Missing file: {ref}")
    for image in parser.images:
        if image.get("alt") is None:
            errors.append(f"Missing alt: {image.get('src')}")
        src = image.get("src", "")
        if src.endswith(".webp"):
            with Image.open(ROOT / src) as file:
                if file.width < 1000:
                    errors.append(f"Image too small: {src}")
    private_tokens = ["CFUPK0197K", "AIRP0000001"]
    for token in private_tokens:
        if token in html:
            errors.append(f"Private token leaked: {token}")
    if errors:
        raise SystemExit("VALIDATION FAILED\n- " + "\n- ".join(errors))
    print("VALIDATION PASSED")
    print(f"Anchors checked: {sum(x.startswith('#') for x in parser.anchors)}")
    print(f"Images checked: {len(parser.images)}")
    print("Private certificate identifiers checked: 2")


if __name__ == "__main__":
    main()
