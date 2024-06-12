import psycopg2


class Database:
    def __init__(self, dbname, user, password, host):
        # 初始化数据库连接
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

    def fetch(self, sql, params=None):
        # Method to fetch data
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()  # Suitable for SELECT queries

    def execute(self, sql, params=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                self.conn.commit()  # 确保提交事务
                return True
        except psycopg2.DatabaseError as e:
            self.conn.rollback()  # 回滚事务
            print("Database error:", e)
            return False


    def close(self):
        # 关闭数据库连接
        self.conn.close()
