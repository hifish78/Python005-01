'''
2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

    用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
    将 ORM、插入、查询语句作为作业内容提交

mysql> select * from userorm;
+----+-------+------+------------+------+--------+---------------------+---------------------+
| id | name  | age  | birthday   | sex  | degree | created_on          | updated_on          |
+----+-------+------+------------+------+--------+---------------------+---------------------+
|  1 | Terry |   25 | 1995-05-01 | M    | Master | 2020-12-11 20:27:26 | 2020-12-11 20:27:26 |
|  2 | Tony  |   35 | 1985-10-10 | M    | Master | 2020-12-11 20:27:26 | 2020-12-11 20:27:26 |
|  3 | Mary  |   20 | 2000-04-01 | F    | Master | 2020-12-11 20:27:26 | 2020-12-11 20:27:26 |
+----+-------+------+------------+------+--------+---------------------+---------------------+
3 rows in set (0.00 sec)
'''

from datetime import datetime, date

from sqlalchemy import Column, Integer, String, DateTime, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class User_table(Base):
    __tablename__ = 'userorm'
    id = Column(Integer(),primary_key=True)
    name = Column(String(50))
    age = Column(Integer())
    birthday = Column(Date())
    sex = Column(String(1))
    degree = Column(String(20))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"User_table(id= {self.id}, name={self.name})"

# 实例一个引擎
dburl = "mysql+pymysql://testuser:testpass@localhost:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")

# create table
Base.metadata.create_all(engine)

# create session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# insert 3 records
user1 = User_table(name='Terry', age=25, birthday=date(1995, 5, 1), sex='M',degree='Master')
user2 = User_table(name='Tony', age=35, birthday=date(1985, 10, 10), sex='M',degree='Master')
user3 = User_table(name='Mary', age=20, birthday=date(2000, 4, 1), sex='F',degree='Master')
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

#Query
query = session.query(User_table)
for item in query:
    print(item)
session.commit()

