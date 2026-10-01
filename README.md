# shelnews

API over the SHEL News Gateway that classifies headlines and highlights key terms.

## Rules (`src/shelnews/rules.py`)

- **buybacks**: company-specific buybacks only. US Treasury / government debt
  buybacks are excluded. Corporate "treasury shares" still count as company buybacks.
- **macro**: Fed, CPI, payrolls, Treasury, etc. Treasury buybacks appear here, but
  their buyback wording is **not** highlighted red.
- **Red highlights**: "Agreement"; buyback wording on company buybacks.

## Run

    pip install -e .[test]
    uvicorn shelnews.app:app --reload
    pytest

`POST /classify {"headline": "..."}` → `{"categories": [...], "highlights": [{start, end, text, color}]}`
