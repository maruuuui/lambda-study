FROM mysql:8.0

# 設定ファイルのコピー
COPY ./my.cnf /etc/mysql/conf.d/my.cnf
# 権限設定
RUN chmod 644 /etc/mysql/conf.d/my.cnf