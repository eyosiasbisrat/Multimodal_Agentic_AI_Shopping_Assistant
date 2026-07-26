# 10_project_shopping_agent

AI Shopping Assistant — Streamlit app with a LangChain agent to search, compare, and order grocery products via text or image.

## Features
- Keyword and filter-based product search (price, organic, rating).
- Visual product search via uploaded images.
- Retrieves product ratings and supports a checkout flow.
- Streamlit chat-style UI.

## Requirements
- Python 3.10+
- See `requirements.txt`

## Setup (Windows)
1. Create & activate venv (PowerShell):
    ```
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
2. Install dependencies:
    ```
    python -m pip install -r requirements.txt
    ```
3. Add credentials to `.env` (example):
    ```
    ANTHROPIC_API_KEY=your_anthropic_key
    ```

## Run
From project folder:
```
python -m streamlit run app.py
```

## Important files
- `app.py` — Streamlit frontend
- `shopping_agent.py` — Agent, tools, and LLM configuration
- `requirements.txt` — Python dependencies
- `store.db` — SQLite product database (placed next to `shopping_agent.py`)

## Troubleshooting
- `ModuleNotFoundError: No module named 'langchain_anthropic'`:
  - Install: `python -m pip install langchain-anthropic`
  - Or update import in `shopping_agent.py` to:
    ```py
    from langchain.chat_models import ChatAnthropic
    ```
- `streamlit: The term 'streamlit' is not recognized`:
  - Activate venv, then run `python -m streamlit run app.py`.
- If `app.py` raises syntax errors, remove duplicated imports/blocks — use the cleaned `app.py` in this repo.

## Usage notes
- Agent enforces flows: IMAGE SEARCH → BROWSING → ORDERING. Always confirm before checkout.
- Keep product IDs from agent messages for ordering.

## License
MIT