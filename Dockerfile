FROM python:3.12

# .pycファイルを生成しないように設定
ENV PYTHONDONTWRITEBYTECODE 1

# 標準出力・標準エラーのストリームをバッファリングしないように設定
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを作成
RUN mkdir /code
WORKDIR /code

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y libpq-dev libheif-dev libjpeg-dev netcat-openbsd

# pipをアップグレードし、必要なライブラリをインストール
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# ソースコードをコンテナにコピー
COPY . /code/

# entrypointスクリプトの改行文字を修正し、実行可能に設定
COPY ./entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# エントリーポイントスクリプトを実行
ENTRYPOINT ["/code/entrypoint.sh"]
