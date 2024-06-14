import csv

# 指定生成的用户数量
num_users = 100

# 打开一个新的CSV文件用于写入
with open('user_credentials.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # 写入头部
    writer.writerow(['username', 'password'])

    # 生成并写入用户数据
    for i in range(1, num_users + 1):
        username = f"test-{i}"
        password = "123456"
        writer.writerow([username, password])

print("CSV文件已生成，包含用户名和密码。")
