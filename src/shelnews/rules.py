"""Classification and highlighting rules.

Each category is a set of include patterns, optionally vetoed by exclude
patterns. Highlight rules mark matching terms in a colour, optionally
suppressed when the headline matches a veto pattern.
"""
import re
from dataclasses import dataclass, field


def _rx(*patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


# Government debt buybacks (e.g. the US Treasury buying back its own
# securities) are not company buybacks. "Treasury shares"/"treasury stock"
# is a corporate concept, so it does not count as Treasury context.
TREASURY_CONTEXT = _rx(
    r"\bU\.?\s?S\.?\s+Treasury\b(?!\s+(shares?|stock))",
    r"\bTreasury\s+(Department|Dept|Secretary|Sec\.?|buy\s?-?backs?|auctions?)\b",
    r"\bTreasur(y|ies)\b(?!\s+(shares?|stock))[^.]*\bbuy\s?-?backs?\b",
    r"\bbuy\s?-?backs?\b[^.]*\bTreasur(y|ies)\b(?!\s+(shares?|stock))",
    r"\b(Bessent|Yellen)\b",
)

BUYBACK_TERMS = _rx(
    r"\bbuy\s?-?backs?\b",
    r"\bbuy(s|ing)?\s+back\b",
    r"\b(share|stock)\s+repurchases?\b",
    r"\brepurchases?\s+(program|plan|authori[sz]ation)\b",
)


@dataclass(frozen=True)
class CategoryRule:
    name: str
    include: list
    exclude: list = field(default_factory=list)


@dataclass(frozen=True)
class HighlightRule:
    terms: list
    color: str = "red"
    unless: list = field(default_factory=list)


CATEGORIES = [
    # Company-specific buybacks only.
    CategoryRule("buybacks", include=BUYBACK_TERMS, exclude=TREASURY_CONTEXT),
    CategoryRule(
        "macro",
        include=_rx(
            r"\bFed\b", r"\bFederal Reserve\b", r"\bFOMC\b", r"\bPowell\b",
            r"\bCPI\b", r"\bPPI\b", r"\bPCE\b", r"\bGDP\b", r"\bPMI\b",
            r"\b(non-?farm )?payrolls\b", r"\bjobless claims\b",
            r"\bunemployment rate\b", r"\binflation\b", r"\bretail sales\b",
            r"\brate (cut|hike)s?\b", r"\bECB\b", r"\bBOJ\b", r"\bBOE\b",
            *[p.pattern for p in TREASURY_CONTEXT],
            r"\bTreasur(y|ies)\b(?!\s+(shares?|stock))",
        ),
    ),
]

HIGHLIGHTS = [
    HighlightRule(_rx(r"\bagreements?\b")),
    # Buyback wording is red only for company buybacks, never for Treasury
    # buybacks (including when the headline shows up under macro).
    HighlightRule(BUYBACK_TERMS, unless=TREASURY_CONTEXT),
]
