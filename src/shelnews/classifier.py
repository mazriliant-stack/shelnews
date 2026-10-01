from dataclasses import dataclass, field

from . import rules


@dataclass
class Highlight:
    start: int
    end: int
    text: str
    color: str


@dataclass
class Classification:
    categories: list = field(default_factory=list)
    highlights: list = field(default_factory=list)


def _any(patterns, text):
    return any(p.search(text) for p in patterns)


def classify(headline, categories=None, highlights=None):
    categories = rules.CATEGORIES if categories is None else categories
    highlights = rules.HIGHLIGHTS if highlights is None else highlights

    result = Classification()
    for cat in categories:
        if _any(cat.include, headline) and not _any(cat.exclude, headline):
            result.categories.append(cat.name)

    spans = []
    for hl in highlights:
        if _any(hl.unless, headline):
            continue
        for p in hl.terms:
            spans.extend((m.start(), m.end(), hl.color) for m in p.finditer(headline))

    # Drop spans overlapping an earlier (or longer) one.
    last_end = -1
    for start, end, color in sorted(spans, key=lambda s: (s[0], -s[1])):
        if start >= last_end:
            result.highlights.append(Highlight(start, end, headline[start:end], color))
            last_end = end
    return result
