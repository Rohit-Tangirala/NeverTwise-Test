install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

lint:
	ruff check app tests scripts

format-check:
	ruff format --check app tests scripts

manifest:
	python scripts/run_scenario.py --list

run:
	uvicorn app.main:app --reload
