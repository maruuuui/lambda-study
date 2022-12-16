FROM public.ecr.aws/lambda/python:3.9 as python-base


# poetry用環境変数
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \ 
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

ENV PATH="$POETRY_HOME/bin:$PATH"

FROM python-base as initial
# mysqlに必要なパッケージ
RUN yum install -y mysql-devel gcc python3-devel

# poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM initial as development-base
COPY poetry.lock pyproject.toml ./
# --no-rootをつけないとインストールに失敗するらしい
# https://github.com/python-poetry/poetry/issues/1227
RUN poetry install --no-root --only main

COPY app.py ./
COPY util/ ./util/

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
