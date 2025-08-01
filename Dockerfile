FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

RUN apt update
RUN apt install -y ffmpeg
RUN pip install -U poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /src/

RUN poetry install --no-interaction --no-ansi

COPY src/ /src/

ENTRYPOINT [ "python", "main.py" ]