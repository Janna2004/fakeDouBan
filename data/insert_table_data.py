import json
import psycopg2
from openpyxl import load_workbook

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_table(cursor, column_names):
    try:
        cursor.execute("DROP TABLE IF EXISTS movies;")
        cursor.execute("CREATE TABLE movies (id SERIAL PRIMARY KEY);")
        for column_name in column_names:
            cursor.execute(f"ALTER TABLE movies ADD COLUMN {column_name} VARCHAR;")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_data(cursor, data):
    try:
        for row in data:
            cursor.execute("INSERT INTO movies VALUES (DEFAULT, %s, %s, %s, %s, %s)", row)
    except Exception as e:
        print(f"Error inserting data: {e}")


if __name__ == "__main__":
    config = load_config('../config.json')
    db_config = config['database']

    conn = psycopg2.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host']
    )
    cursor = conn.cursor()

    # 从 Excel 文件中读取数据
    wb = load_workbook(filename='data_movie.xlsx')
    ws = wb.active
    column_names = [cell.value for cell in ws[1]]
    data = [[cell.value for cell in row] for row in ws.iter_rows(min_row=2)]

    # 创建表格并插入数据
    create_table(cursor, column_names)
    insert_data(cursor, data)

    # 提交并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

    print("Data inserted successfully!")
