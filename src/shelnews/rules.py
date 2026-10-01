"""Classification and highlighting rules.

A headline is first checked against NOISE filters (feature articles,
analyst items, price-move commentary). Noise is never assigned to a tab
and never highlighted. Otherwise each tab whose trigger terms match (and
whose excludes don't) claims the headline, and its triggers are
highlighted.
"""
import re
from dataclasses import dataclass, field


def _rx(*patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


# --- Noise: not breaking news ------------------------------------------------

NOISE = {
    # Features, opinion, listicles, awards/rankings.
    "article": _rx(
        r"^(How|Why|What|Here's|Here Is|Is|Are|Should|Can)\b",
        r"--\s*(Barrons|WSJ|MarketWatch|Investor's Business Daily)(\.com)?\s*$",
        r"\b(Opinion|Column|Commentary|Analysis|Explainer|Podcast)\s*:",
        r"\bstocks?\s+to\s+(buy|sell|watch|own)\b",
        r"^\d+\s+[\w\s-]*\bstocks?\b",
        r"\bBest\s+(Workplaces|Places\s+to\s+Work|Companies|Employers)\b",
        r"\b(selected|named|ranked)\s+(by|as|to|among)\b.*\b(list|Best|Top|Most)\b",
    ),
    # Analyst calls, ratings, targets, coverage.
    "analyst": _rx(
        r"\banalysts?\s+(hold|host|holds|hosts|say|says|see|sees|expect|expects)\b",
        r"\banalyst/industry\b",
        r"\bprice\s+target\b",
        r"\b(upgrade[sd]?|downgrade[sd]?)\b",
        r"\b(initiat\w*|resum\w*|assum\w*)\s+coverage\b",
        r"\breiterat\w*\b",
        r"\b(Buy|Sell|Hold|Neutral|Overweight|Underweight|Outperform|Underperform)\s+rating\b",
    ),
    # Price action / market colour.
    "market_commentary": _rx(
        r"(?<![\w$])[+-]\d+(\.\d+)?%",
        r"\bshares?\s+(at|hit|hits|near|touch\w*)\s+(new\s+|session\s+|52-week\s+|record\s+)?(lows?|highs?)\b",
        r"\bopens?\s+(trading\s+)?at\s+\$",
        r"\baround\s+\$[\d.,]+\s+level\b",
        r"\bafter\b.*\bheadlines\b",
    ),
}


# --- Shared patterns ---------------------------------------------------------

# Government debt buybacks/offerings (e.g. the US Treasury) are not company
# actions. "Treasury shares"/"treasury stock" is a corporate concept, so it
# does not count as Treasury context.
TREASURY_CONTEXT = _rx(
    r"\bU\.?\s?S\.?\s+Treasury\b(?!\s+(shares?|stock))",
    r"\bTreasury\s+(Department|Dept|Secretary|Sec\.?|buy\s?-?backs?|auctions?|notes|bonds|bills)\b",
    r"\bTreasur(y|ies)\b(?!\s+(shares?|stock))[^.]*\bbuy\s?-?backs?\b",
    r"\bbuy\s?-?backs?\b[^.]*\bTreasur(y|ies)\b(?!\s+(shares?|stock))",
    r"\b(Bessent|Yellen)\b",
)

BUYBACK_TERMS = _rx(
    r"\bbuy\s?-?backs?\b",
    r"\bbuy(s|ing)?\s+back\b",
    r"\b(share|stock)\s+repurchases?\b",
    r"\brepurchases?\s+(program|programme|plan|authori[sz]ation)\b",
)

OFFERING_TERMS = _rx(
    r"\b(public|secondary|follow-on|registered\s+direct|private)\s+(offering|placement)\b",
    r"\b(convertible|senior)\s+notes?\s+offering\b",
    r"\bat-the-market\b",
    r"\bprices?\s+(upsized\s+)?(IPO|offering)\b",
    r"\bpricing\s+of\b",
    r"\bupsized\b",
)


@dataclass(frozen=True)
class TabRule:
    name: str
    triggers: list
    exclude: list = field(default_factory=list)


TABS = [
    TabRule(
        "mna_deals",
        triggers=_rx(
            r"\b(definitive\s+)?(merger\s+)?agreements?\b",
            r"\bbid\s+for\b",
            r"\bdeal\b",
            r"\b(to\s+)?acquir(e|es|ed|ing)\b",
            r"\bacquisition\b",
            r"\bmerger\b",
            r"\btakeover\b",
            r"\btender\s+offer\b",
            r"\bcontract\s+(award|with)\b",
            r"\bwins?\s+[\w$.\s-]{0,30}contract\b",
            r"\bawarded\b",
            r"\bstake\s+in\b",
        ),
    ),
    TabRule(
        "biotech",
        triggers=_rx(
            r"\bphase\s+(1|2|3|I|II|III|1/2|2/3)\b(\s+(trial|study|data))?",
            r"\b(FDA|EMA|court|regulatory)\s+approv\w*\b",
            r"\bapprov(al|es|ed)\b",
            r"\btopline\b",
            r"\bPDUFA\b",
            r"\b(BLA|NDA|sNDA|MAA)\b",
            r"\bcomplete\s+response\s+letter\b|\bCRL\b",
            r"\bbreakthrough\s+therapy\b",
            r"\bfast\s+track\b",
            r"\borphan\s+drug\b",
            r"\bsettlement\b",
        ),
    ),
    TabRule(
        "offerings_buybacks",
        triggers=BUYBACK_TERMS + OFFERING_TERMS,
        exclude=TREASURY_CONTEXT,
    ),
    TabRule(
        "macro",
        triggers=_rx(
            r"\bFed\b", r"\bFederal Reserve\b", r"\bFOMC\b", r"\bPowell\b",
            r"\bCPI\b", r"\bPPI\b", r"\bPCE\b", r"\bGDP\b", r"\bPMI\b",
            r"\b(non-?farm\s+)?payrolls\b", r"\bjobless\s+claims\b",
            r"\bunemployment\s+rate\b", r"\binflation\b", r"\bretail\s+sales\b",
            r"\brate\s+(cut|hike)s?\b", r"\bECB\b", r"\bBOJ\b", r"\bBOE\b",
            r"\bTreasur(y|ies)\b(?!\s+(shares?|stock))",
            *[p.pattern for p in TREASURY_CONTEXT],
        ),
    ),
]

# Highlighting is per tab, but macro is context only: nothing in macro is
# red (in particular, Treasury buybacks are never red).
UNHIGHLIGHTED_TABS = {"macro"}
HIGHLIGHT_COLOR = "red"
