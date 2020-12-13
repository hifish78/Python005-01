学习笔记
1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
1)修改字符集为 UTF8mb4 并验证
mysql> set global character_set_server='utf8mb4';
Query OK, 0 rows affected (0.00 sec)
mysql> set global character_set_database='utf8mb4';
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> set global character_set_connection='utf8mb4';
Query OK, 0 rows affected (0.00 sec)
mysql> set global character_set_client='utf8mb4';
Query OK, 0 rows affected (0.00 sec)
mysql> show variables like '%character%';
+--------------------------+--------------------------------------------------------+
| Variable_name            | Value                                                  |
+--------------------------+--------------------------------------------------------+
| character_set_client     | utf8mb4                                                |
| character_set_connection | utf8mb4                                                |
| character_set_database   | utf8mb4                                                |
| character_set_filesystem | binary                                                 |
| character_set_results    | utf8mb4                                                |
| character_set_server     | utf8mb4                                                |
| character_set_system     | utf8                                                   |
| character_sets_dir       | /usr/local/Cellar/mysql/8.0.22_1/share/mysql/charsets/ |
+--------------------------+--------------------------------------------------------+
8 rows in set (0.01 sec)

2)新建一个数据库 testdb，并为该数据库增加远程访问的用。
mysql> create database testdb;
Query OK, 1 row affected (0.00 sec)
mysql> set global variables validate_password.policy 0
mysql> create user 'testuser'@'%' IDENTIFIED BY 'testpass';
Query OK, 0 rows affected (0.01 sec)
mysql> GRANT ALL PRIVILEGES ON *.* TO  'testuser'@'%';
Query OK, 0 rows affected (0.00 sec) 

2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
    用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
    将 ORM、插入、查询语句作为作业内容提交
    (see user_info.py file)
    
3. 为以下 sql 语句标注执行顺序：
5# SELECT DISTINCT player_id, player_name, count(*) as num
1# FROM player JOIN team ON player.team_id = team.team_id     
2# WHERE height > 1.80
3# GROUP BY player.team_id 
4# HAVING num > 2 
6# ORDER BY num DESC 
7# LIMIT 2

4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?
Table1
id name
1 table1_table2
2 table1

Table2
id name
1 table1_table2
3 table2

Innner JOIN result:
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;
+------+---------------+------+---------------+
| id   | name          | id   | name          |
+------+---------------+------+---------------+
| 1    | table1_table2 | 1    | table1_table2 |
+------+---------------+------+---------------+

Left Join:
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
LEFT JOIN Table2
ON Table1.id = Table2.id;
+------+---------------+------+---------------+
| id   | name          | id   | name          |
+------+---------------+------+---------------+
| 1    | table1_table2 | 1    | table1_table2 |
| 2    | table1        | NULL | NULL          |
+------+---------------+------+---------------+

RIGHT JOIN:
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
RIGHT JOIN Table2
ON Table1.id = Table2.id;
+------+---------------+------+---------------+
| id   | name          | id   | name          |
+------+---------------+------+---------------+
| 1    | table1_table2 | 1    | table1_table2 |
| NULL | NULL          | 3    | table2        |
+------+---------------+------+---------------+
2 rows in set (0.00 sec)

5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。
mysql> create unique index table1_id on table1(id);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> desc table1
    -> ;
+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| id    | varchar(100) | YES  | UNI | NULL    |       |
| name  | varchar(100) | YES  |     | NULL    |       |
+-------+--------------+------+-----+---------+-------+
2 rows in set (0.00 sec)

当数据记录特别大的情况下，增加索引后能提高查询速度。但是如果记录特别少，增加索引未必能提高查询速度，因为有重建缩影的开销。

6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

    请合理设计三张表的字段类型和表结构；
    请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

See transaction.py file