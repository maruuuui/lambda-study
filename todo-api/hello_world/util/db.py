import os
import mysql.connector


MYSQL_HOST_NAME = os.environ.get('MYSQLHOSTNAME') if os.environ.get('MYSQLHOSTNAME') else "lambda-study-db"
MYSQL_PORT_NO = os.environ.get('MYSQLPORTNO') if os.environ.get('MYSQLPORTNO') else  "3307"
MYSQL_USER  = os.environ.get('MYSQLUSER') if os.environ.get('MYSQLUSER') else  "root"
MYSQL_PASSWORD  = os.environ.get('MYSQLPASSWORD') if os.environ.get('MYSQLPASSWORD') else  "rootpass"

class DataBaseAdapter:
    def __init__(self):
        # データベースへの接続情報
        self.host = MYSQL_HOST_NAME
        self.port = MYSQL_PORT_NO
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.database = "sample_db"

    def connect_db(self):
        # データベースへの接続とカーソルの生成
        connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        print("connected!")
        return connection

    def create(self, to_do):
        connection = self.connect_db()
        with connection:
            with connection.cursor(dictionary=True) as cur:
                # レコードを挿入
                sql = "INSERT INTO `to_dos` (`id`, `title`, `memo`, `deadline`) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (to_do["id"], to_do["title"], to_do["memo"], to_do["deadline"]))

                result_sql = "select * from to_dos where `id`=%s;"
                cur.execute(result_sql, (to_do["id"],))

                result = cur.fetchone()
            # コミットしてトランザクション実行
            connection.commit()
        # 終了処理
        cur.close()
        return result

    def update(self, to_do):
        pass

    def get_all(self):
        print("get_all")
        connection = self.connect_db()

        with connection.cursor(dictionary=True) as cur:
            sql = "select * from to_dos order by deadline;"
            cur.execute(sql)
            results = cur.fetchall()

        # 終了処理
        cur.close()
        return results

    def get(self, id):
        pass

    def delete(self, todo_id):
        print("delete", todo_id)
        connection = self.connect_db()
        with connection:
            with connection.cursor(dictionary=True) as cur:

                sql = "delete from to_dos where `id`=%s;"
                cur.execute(sql, (todo_id,))
                result = {"deleted_rowcount": cur.rowcount}
            # コミットしてトランザクション実行
            connection.commit()

        # 終了処理
        cur.close()
        return result
