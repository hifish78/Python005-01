'''
CREATE TABLE user_tb(
user_id INT AUTO_INCREMENT PRIMARY KEY,
user_name VARCHAR(100) NOT NULL
);

CREATE TABLE user_asset_tb(
user_id INT PRIMARY KEY,
asset_amount INT,
CONSTRAINT fk_user
FOREIGN KEY(user_id) REFERENCES user(user_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE audit_tb(
transaction_id INT AUTO_INCREMENT PRIMARY KEY,
from_id INT,
to_id INT,
transfer_amount INT,
transfer_time DATETIME
)
'''
from datetime import datetime

import pymysql
conn = pymysql.connect("localhost", "testuser", "testpass", "testdb")

def query_sql(sql):
    try:
        res = []
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"fetch error {e}")
        conn.close()
    finally:
        return res


def find_user(user_name):
    query = f"select user_id from user_tb where user_name = '{user_name}'"
    res = query_sql(query)
    if len(res) != 1:
        raise Exception("Can't find the user name or have the duplicated user name, please check!")
    return res[0][0]

def find_asset(user_name):
    query = f"select asset_amount from user_asset_tb a, user_tb b " \
            f"where a.user_id = b.user_id and b.user_name = '{user_name}'"
    res = query_sql(query)
    return res[0][0]

def transfer_asset(from_user_name, to_user_name, amount):
    from_user_id = find_user(from_user_name)
    to_user_id = find_user(to_user_name)
    from_user_asset = find_asset(from_user_name)
    to_user_asset = find_asset(to_user_name)

    try:
        updated_from_user_asset = from_user_asset - amount
        updated_to_user_asset = to_user_asset + amount
        # transfer_time = datetime.now()
        with conn.cursor() as cursor:
            sql1 = f"update user_asset_tb set asset_amount = {updated_from_user_asset} where user_id = {from_user_id}"
            sql2 = f"update user_asset_tb set asset_amount = {updated_to_user_asset} where user_id = {to_user_id}"
            sql3 = f"insert into audit_tb(from_id, to_id, transfer_amount, transfer_time) " \
                   f"values({from_user_id}, {to_user_id}, {amount}, now())"
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"failed to transfer asset due to {e}")
    finally:
        conn.close()

def prepare_data():
    with conn.cursor() as cursor:
        sql1 = "insert into user_tb values(%s, %s)"
        values1 = (
            (1, '张三'),
            (2, '李四')
        )
        cursor.executemany(sql1, values1)

        sql2 = "insert into user_asset_tb values(%s, %s)"
        values2 = (
            (1, 1500),
            (2, 2000)
        )
        cursor.executemany(sql2,values2)
    conn.commit()


if __name__ == '__main__':
    # prepare_data()
    transfer_asset("张三","李四",100)
