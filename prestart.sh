python ./app/backend_pre_start.py
alembic upgrade head
python -m ./app/initial_data.py
poetry run python app/main.py
