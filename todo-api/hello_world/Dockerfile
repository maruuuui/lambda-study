FROM public.ecr.aws/lambda/python:3.9

COPY app.py poetry.lock pyproject.toml ./

# poetry用環境変数
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \ 
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -





# --no-rootをつけないとインストールに失敗するらしい
# https://github.com/python-poetry/poetry/issues/1227
RUN poetry install --no-root

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
