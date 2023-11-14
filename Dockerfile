# Use the official Ubuntu base image with tag "jammy"
FROM ubuntu:jammy

# Set the maintainer label
LABEL maintainer="Nisuga Jayawardana <nisuga.rockwell@gmail.com>"

# Set environment variables for configuration
ENV PYTHON_VERSION=3.10 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Update the package lists and install Python3.11 with pip
RUN apt-get update && apt-get install -y  python${PYTHON_VERSION} python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1
RUN python --version
RUN python${PYTHON_VERSION} -m pip install --upgrade pip
RUN pip --version

# installing dependencies to run browsers.
RUN pip install poetry==1.7.0 scrapy==2.11.0 scrapy-playwright==0.0.33
RUN playwright install
RUN playwright install-deps

WORKDIR /scraper

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN poetry install

RUN touch README.md

ENTRYPOINT ["poetry", "run", "python", "-m", "app.main"]

EXPOSE 5842
