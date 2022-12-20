import mysql.connector


class DataBaseAdapter:
    def __init__(self):
        # データベースへの接続とカーソルの生成
        # TODO: 環境ごとに差し替える仕組み
        self.host = "lambda-study-db"
        self.port = ("3307",)
        self.user = ("root",)
        self.password = ("rootpass",)
        self.database = "sample_db"

    def connect_db(self):
        # データベースへの接続とカーソルの生成
        self.conn = mysql.connector.connect(
            host="lambda-study-db",
            port="3307",
            user="root",
            password="rootpass",
            database="sample_db",
        )
        print("connected!")
        self.cur = self.conn.cursor(dictionary=True)

    def disconnect_db(self):
        # 接続を閉じる
        self.cur.close()
        self.conn.close()

    def create(self, to_do):
        self.connect_db()

        sql = "select * from to_dos;"
        self.cur.execute(sql)
        results = self.cur.fetchall()

        self.disconnect_db()
        return results

    def update(self, to_do):
        self.connect_db()

        sql = "select * from to_dos;"
        self.cur.execute(sql)
        results = self.cur.fetchall()

        self.disconnect_db()
        return results

    def get_all(self):
        print("get_all")
        self.connect_db()

        sql = "select * from to_dos;"
        self.cur.execute(sql)
        results = self.cur.fetchall()

        self.disconnect_db()
        return results

    def get(self, id):
        self.connect_db()

        sql = "select * from to_dos;"
        self.cur.execute(sql)
        results = self.cur.fetchall()

        self.disconnect_db()
        return results

    def delete(self, id):
        self.connect_db()

        sql = "select * from to_dos;"
        self.cur.execute(sql)
        results = self.cur.fetchall()

        self.disconnect_db()
        return results
