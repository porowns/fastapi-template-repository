FROM python:3.10.6

ENV PYTHONPATH "${PYTHONPATH}:/"
# Required to bind to port 8000
ENV PORT=8000

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /api/
COPY pyproject.toml .

RUN poetry install --no-root --no-dev

COPY ./api api
COPY ./estimation estimation

CMD ["poetry", "run", "prod"]
# CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]
