from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=True)

class UserAsset(Base):
    __tablename__ = 'user_asset'

    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    asset_amount = Column(Integer)

class Audit(Base):
    __tablename__ = 'audit'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    transfer_amount = Column(Integer)
    transfer_time = Column(DateTime)

# implement an engine
dburl = "mysql+pymysql://testuser:testpass@localhost:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")

# create table
Base.metadata.create_all(engine)

# create session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

def find_user(user_name):
    user_id = session.query(User.user_id).filter(User.user_name == user_name).one()
    return user_id[0]

def find_asset(user_name):
    user_id = find_user(user_name)
    asset_amount = session.query(UserAsset.asset_amount).filter(UserAsset.user_id == user_id).one()
    return asset_amount[0]

def transfer_asset(from_name, to_name, amount):
    try:
        from_user_id = find_user(from_name)
        to_user_id = find_user(to_name)
        from_user_asset = find_asset(from_name)
        if from_user_asset < amount:
            return f"The remaining amount is not enough."

        # update the asset for from person
        query_from = session.query(UserAsset.asset_amount).filter(UserAsset.user_id == from_user_id)
        query_from.update({UserAsset.asset_amount: UserAsset.asset_amount - amount})

        # update the asset for the to person
        query_to = session.query(UserAsset.asset_amount).filter(UserAsset.user_id == to_user_id)
        query_to.update({UserAsset.asset_amount: UserAsset.asset_amount + amount})

        # update audit info
        transfer_item = Audit(from_id=from_user_id,
                              to_id=to_user_id,
                              transfer_amount=amount,
                              transfer_time=datetime.now()
                              )
        session.add(transfer_item)
        session.flush()
        session.commit()
    except Exception as e:
        print(f"failed due to {e}")
        session.rollback()
    finally:
        session.close()

def prepare_data():
    session1 = SessionClass()
    user1 = User(user_id=1, user_name='张三')
    user2 = User(user_id=2, user_name='李四')
    session1.add(user1)
    session1.add(user2)
    session1.flush()
    session1.commit()

    session2 = SessionClass()
    asset1 = UserAsset(user_id=1, asset_amount=500)
    asset2 = UserAsset(user_id=2, asset_amount=1000)
    session2.add(asset1)
    session2.add(asset2)
    session2.flush()
    session2.commit()

def test1():
    prepare_data()
    transfer_asset('张三', "李四", 100)

if __name__ == '__main__':
    test1()


