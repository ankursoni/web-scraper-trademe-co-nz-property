FROM python:3.9.13-slim-buster

WORKDIR /src
COPY search search
COPY requirements.txt .

RUN pip install -r /src/requirements.txt

ENV FLASK_ENV=development
# ENV FLASK_APP=/src/search/app.py
# CMD ["flask", "run"]

ENTRYPOINT [ "python3" ]
CMD ["-m", "search.app"]
