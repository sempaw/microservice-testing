FROM python:3.10

ENV STAGE=development \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /usr/app
COPY poetry.lock pyproject.toml /usr/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "STAGE" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /usr/app

RUN #poetry run python ./prestart.py

CMD poetry run ./prestart.sh