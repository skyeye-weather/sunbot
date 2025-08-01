FROM python:3.12

WORKDIR /code
COPY . /code

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

CMD python main.py
