# shelnews

API over the SHEL News Gateway that classifies headlines and highlights key terms.

## Rules (`src/shelnews/rules.py`)

1. **Noise filters run first.** A match means no tab and no highlighting.
   - `article`: features ("How…", "-- Barrons.com"), listicles ("stocks to buy"), awards/rankings
   - `analyst`: analyst calls, ratings, upgrades/downgrades, price targets, coverage
   - `market_commentary`: price action ("+2.6%", "shares at lows", "opens at $6")
2. **Tabs** claim a headline when a trigger matches; triggers are highlighted red.
   - `mna_deals`: agreement, bid for, deal, acquire, merger, contract award/with, wins … contract
   - `biotech`: phase N trial, approval, topline, PDUFA, BLA/NDA, CRL, settlement
   - `offerings_buybacks`: company buybacks and offerings; US Treasury buybacks/offerings excluded
   - `macro`: Fed, CPI, payrolls, Treasury…; never highlighted

## Run

    pip install -e .[test]
    uvicorn shelnews.app:app --reload
    pytest

`POST /classify {"headline": "..."}` → `{"categories": [...], "highlights": [{start, end, text, color}]}`
