import pytest

from shelnews import classify


def red_words(headline):
    return [h.text for h in classify(headline).highlights if h.color == "red"]


def test_agreement_is_red():
    h = ("Nexalin Technology Signs Definitive Exclusive Distribution and Local "
         "Manufacturing Agreement for Brazil and South America")
    assert red_words(h) == ["Agreement"]


@pytest.mark.parametrize("headline", [
    "Apple Announces $110 Billion Share Buyback",
    "XYZ Corp Board Authorizes New Stock Repurchase Program",
    "Acme to Buy Back Up to 10% of Shares",
    "Acme Completes Buyback, Cancels Treasury Shares",
])
def test_company_buybacks(headline):
    result = classify(headline)
    assert "buybacks" in result.categories
    assert red_words(headline)


@pytest.mark.parametrize("headline", [
    "US Treasury Buyback Operation: Accepts $2B in 10-Year Notes",
    "U.S. Treasury Announces Results of Buyback Operation",
    "Treasury Department to Expand Debt Buybacks",
    "Treasury Buybacks Draw Strong Offers",
    "Bessent Says Buybacks Will Support Market Liquidity",
])
def test_treasury_buybacks_not_buyback_and_not_red(headline):
    result = classify(headline)
    assert "buybacks" not in result.categories
    assert "macro" in result.categories
    assert red_words(headline) == []


def test_macro_headline():
    assert "macro" in classify("Fed Holds Rates Steady, Powell Signals Patience").categories
