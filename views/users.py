from utils.http_code import HTTPResponseHandler


class Users:
    def __init__(self, db, handler):
        self.db = db
        self.response_handler = HTTPResponseHandler(handler)

    def login(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if not phone or not password:
            self.response_handler.parse_error('phone and password are required')
            return

        sql = "SELECT * FROM users WHERE phone = %s"
        user = self.db.fetch(sql, (phone,))[0]
        if user and user[1] == password:
            data = {
                "id": user[4],
                "isAdmin": user[3],
                "username": user[0],
                "phone": user[2]
            }
            self.response_handler.response_json(data)
        else:
            self.response_handler.parse_error('Invalid credentials')

    def signup(self, data):
        username = data.get('username')
        phone = data.get('phone')
        password = data.get('password')
        if not username or not password:
            self.response_handler.parse_error('Username and password are required')
            return

        sql_check = "SELECT * FROM users WHERE username = %s and phone = %s"
        if self.db.fetch(sql_check, (username, phone)):
            self.response_handler.parse_error('用户名与手机号已注册')
        else:
            sql_insert = "INSERT INTO users (username, phone, password) VALUES (%s, %s, %s)"
            self.db.execute(sql_insert, (username, phone, password))
            try:
                sql = "SELECT * FROM users WHERE username = %s and phone = %s"
                user = self.db.fetch(sql, (username,phone))[0]
                print(user)
                data = {
                    "id": user[4],
                    "isAdmin": user[3],
                    "username": user[0],
                    "phone": user[2]
                }
                self.response_handler.response_json(data)
            except:
                self.response_handler.server_error('注册失败')
