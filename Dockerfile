FROM python:3.13-slim-trixie

WORKDIR /src
COPY search search
COPY pyproject.toml uv.lock .

RUN pip install --upgrade pip && pip install uv && \
    uv sync --frozen && uv add newrelic

ENV FLASK_ENV=development

ENTRYPOINT [ "python3" ]
CMD ["-m", "search.app"]
