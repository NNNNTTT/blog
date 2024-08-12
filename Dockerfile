FROM python:3.12
# .pycの不要なファイルを生成しないよう設定
ENV PYTHONDONTWRITEBYTECODE 1
# 標準出力・標準エラーのストリームのバッファリングを行わないよう設定
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && \
    apt-get install -y libpq-dev netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# pipをアップグレードし、ライブラリをインストール
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/
COPY ./entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]


