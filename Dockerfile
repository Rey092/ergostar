FROM python:3.12-slim-bullseye

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

# where the code lives
WORKDIR $PYTHONPATH

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl \
  # translations
  gettext

# install dependencies
RUN pip install --upgrade pip
RUN pip install setuptools

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# copy python dependencies
COPY pyproject.toml poetry.lock ./
# disable virtualenv creation
RUN poetry config virtualenvs.create false
# install python dependencies
RUN poetry install --only main --no-interaction

# copy entrypoint.sh
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# install app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]
