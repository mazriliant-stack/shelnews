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
    noise: str | None = None


def _any(patterns, text):
    return any(p.search(text) for p in patterns)


def classify(headline, tabs=None, noise=None):
    tabs = rules.TABS if tabs is None else tabs
    noise = rules.NOISE if noise is None else noise

    result = Classification()
    for reason, patterns in noise.items():
        if _any(patterns, headline):
            result.noise = reason
            return result

    spans = []
    for tab in tabs:
        if _any(tab.exclude, headline):
            continue
        matches = [m for p in tab.triggers for m in p.finditer(headline)]
        if not matches:
            continue
        result.categories.append(tab.name)
        if tab.name not in rules.UNHIGHLIGHTED_TABS:
            spans.extend((m.start(), m.end()) for m in matches)

    # Merge overlapping trigger spans.
    for start, end in sorted(spans):
        last = result.highlights[-1] if result.highlights else None
        if last and start <= last.end:
            last.end = max(last.end, end)
            last.text = headline[last.start:last.end]
        else:
            result.highlights.append(
                Highlight(start, end, headline[start:end], rules.HIGHLIGHT_COLOR))
    return result
