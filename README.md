# docker-golang-study

https://github.com/maruuuui/docker-golang-study
のバックエンドをAWS lambda + API Gatewayに置き換え、フロントはSPAに置き換える。
serverlessなバックエンドを構築する練習

フロントはこちら：https://github.com/maruuuui/react-todo-app

## やること

 + mysqlでToDoアプリを作成し、AWS上にデプロイする  

## ローカル起動コマンド

```sh
# dbを立ち上げる
docker-compose up -d
# ローカルでlambdaを立ち上げる
cd todo-api
./start-api-local.sh
```

## デプロイ手順

以下のコマンドを実行する
```
cd todo-api
sum build
sum deploy
```

デプロイ先のURL： <http://s3.maruuuui.tk/>