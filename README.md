# Contract Registry
### How to run?
1. To work with project as intended use `pip install poetry`
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. Run the DB migrations via poetry `poetry run python app/prestart.py` (only required once)
4. Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
5. Open `http://localhost:8001/` docs to see service documentation