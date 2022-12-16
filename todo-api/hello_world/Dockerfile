FROM public.ecr.aws/lambda/python:3.9

COPY app.py poetry.lock pyproject.toml ./

# poetryのインストール
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false 

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_NO_INTERACTION=1

RUN poetry install --no-root

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
