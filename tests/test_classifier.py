import pytest

from shelnews import classify


def red(headline):
    return [h.text for h in classify(headline).highlights]


# --- Should be excluded entirely (no tab, nothing red) -----------------------

@pytest.mark.parametrize("headline, reason", [
    # M&A tab feedback: articles, not breaking news.
    ("Robert Half selected by Fortune as one of the Best Workplaces in "
     "Consulting & Professional Services 2026", "article"),
    ("3 high-conviction SMID-cap biotech stocks to buy: Jefferies", "article"),
    ("$USO WTI crude pop, +2.6% to $92.87 after troop deployment headlines",
     "market_commentary"),
    # Biotech tab feedback.
    ("How Eli Lilly Just Extended Its Lead in the Weight-Loss Drug Market -- Barrons.com",
     "article"),
    ("Mizuho biotech analysts hold an analyst/industry conference call", "analyst"),
    ("JPMorgan SMid biotech analysts hold an analyst/industry conference call", "analyst"),
    ("Goldman upgrades Moderna to Buy, raises price target", "analyst"),
    # Offerings & Buybacks feedback.
    ("$VKTX shares at lows -4.7% around $31 level", "market_commentary"),
    ("Chilwa Minerals opens at $6, ADSs and warrants priced at $5.60 in U.S. IPO",
     "market_commentary"),
])
def test_noise_excluded(headline, reason):
    result = classify(headline)
    assert result.noise == reason
    assert result.categories == []
    assert result.highlights == []


# --- Should be included and red ---------------------------------------------

@pytest.mark.parametrize("headline, tab", [
    ("BAE weighs bid for Robin Radar in possible $2.3B deal, Reuters reports", "mna_deals"),
    ("Telos announces contract award from U.S. Department of Commerce", "mna_deals"),
    ("Telos wins Xacta contract with Commerce Dept. Inspector General", "mna_deals"),
    ("Nexalin Technology Signs Definitive Exclusive Distribution and Local "
     "Manufacturing Agreement for Brazil and South America", "mna_deals"),
    ("AGs Seek Court Approval of $400M Settlement With Sandoz", "biotech"),
    ("$REGN Regeneron Pharmaceuticals, - to advance ubamatamab into confirmatory "
     "phase 3 trial for lgsoc", "biotech"),
    ("Vinci to Buy Back Up to $305.9 Million in Shares", "offerings_buybacks"),
    ("Press Release: VINCI: Implementation of the share buyback programme",
     "offerings_buybacks"),
    ("Societe Generale Completes EUR1.5B Share Buyback", "offerings_buybacks"),
    ("Acme Completes Buyback, Cancels Treasury Shares", "offerings_buybacks"),
])
def test_good_headlines(headline, tab):
    result = classify(headline)
    assert result.noise is None
    assert tab in result.categories
    assert red(headline)


def test_specific_triggers():
    assert red("Telos announces contract award from U.S. Department of Commerce") == ["contract award"]
    assert "phase 3 trial" in red("$REGN to advance ubamatamab into confirmatory phase 3 trial")


# --- Treasury buybacks: not in buybacks, in macro, never red -----------------

@pytest.mark.parametrize("headline", [
    "$TLT $TBT US Treasury bought $6B in 10-20 yr debt in October 1 buyback "
    "operationUS Treasury notes $46.39B offered in 10-20 yr buyback operation",
    "U.S. Treasury Announces Results of Buyback Operation",
    "Treasury Department to Expand Debt Buybacks",
    "Bessent Says Buybacks Will Support Market Liquidity",
])
def test_treasury_buybacks(headline):
    result = classify(headline)
    assert "offerings_buybacks" not in result.categories
    assert "macro" in result.categories
    assert result.highlights == []
