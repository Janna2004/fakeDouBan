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

    def modify_name(self, data):
        id = data.get('id')
        newName = data.get('newName')
        if not id or not newName:
            self.response_handler.parse_error('id and newName are required')
            return
        sql_update = "UPDATE users SET username = %s WHERE id = %s"
        self.db.execute(sql_update, (newName, id))
        try:
            sql = "SELECT * FROM users WHERE id = %s"
            user = self.db.fetch(sql, (id,))[0]
            data = {
                "id": user[4],
                "isAdmin": user[3],
                "username": user[0],
                "phone": user[2]
            }
            self.response_handler.response_json(data)
        except:
            self.response_handler.server_error('Failed to update username')

    def modify_pwd(self, data):
        id = data.get('id')
        oldPwd = data.get('oldPwd')
        newPwd = data.get('newPwd')
        if not id or not oldPwd or not newPwd:
            self.response_handler.parse_error('id, oldPwd and newPwd are required')
            return

        sql_check = "SELECT * FROM users WHERE id = %s AND password = %s"
        if self.db.fetch(sql_check, (id, oldPwd)):
            sql_update = "UPDATE users SET password = %s WHERE id = %s"
            self.db.execute(sql_update, (newPwd, id))
            try:
                sql = "SELECT * FROM users WHERE id = %s"
                user = self.db.fetch(sql, (id,))[0]
                data = {
                    "id": user[4],
                    "isAdmin": user[3],
                    "username": user[0],
                    "phone": user[2]
                }
                self.response_handler.response_json(data)
            except:
                self.response_handler.server_error('Failed to update password')
        else:
            self.response_handler.parse_error('Incorrect old password')

    def user_info(self, query_params):
        id = query_params.get('id', [None])[0]
        if id:
            sql = "SELECT * FROM users WHERE id = %s"
            user = self.db.fetch(sql, (id,))[0]
            if user:
                data = {
                    "id": user[4],
                    "isAdmin": user[3],
                    "username": user[0],
                    "phone": user[2]
                }
                self.response_handler.response_json(data)
            else:
                self.response_handler.not_found('User not found')
        else:
            self.response_handler.parse_error('id is required')

    def all_user(self):
        sql = "SELECT * FROM users"
        users = self.db.fetch(sql)
        data = [{
            "id": user[4],
            "isAdmin": user[3],
            "username": user[0],
            "phone": user[2]
        } for user in users]
        self.response_handler.response_json(data)

    def delete_user(self, query_params):
        id = query_params.get('id', [None])[0]
        if id:
            sql = "DELETE FROM users WHERE id = %s"
            if self.db.execute(sql, (id,)):
                sql = "SELECT * FROM users"
                users = self.db.fetch(sql)
                data = [{
                    "id": user[4],
                    "isAdmin": user[3],
                    "username": user[0],
                    "phone": user[2]
                } for user in users]
                self.response_handler.response_json(data)
            else:
                self.response_handler.server_error('Failed to delete user')
        else:
            self.response_handler.parse_error('id is required')

    def add_admin(self, query_params):
        id = query_params.get('id', [None])[0]
        if id:
            sql = "UPDATE users SET is_admin = TRUE WHERE id = %s"
            if self.db.execute(sql, (id,)):
                sql = "SELECT * FROM users"
                users = self.db.fetch(sql)
                data = [{
                    "id": user[4],
                    "isAdmin": user[3],
                    "username": user[0],
                    "phone": user[2]
                } for user in users]
                self.response_handler.response_json(data)
            else:
                self.response_handler.server_error('Failed to add admin')
        else:
            self.response_handler.parse_error('id is required')
