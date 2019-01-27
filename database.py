from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_account(first_name,last_name,username,password,age):
    if not check_user_exists(username):    
        add_account = Account(
            first_name= first_name,
            last_name = last_name,
            username = username,         
            password = password,
            age = age)
        session.add(add_account)
        session.commit()
    else:
    	raise Exception("try onther user")

def check_user_exists(username):

    account = session.query(Account).filter_by(username=username).first()
    if account==None:

        return False
    else:
        return True


def check_user_and_pass(username, password):
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Account).filter_by(username=username,password=password)
    print("check")
    result = query.first()
    if result is not None:
        return True
    else:
       print('wrong password!')
       return False



def add_info(name, quantity, submitted):
    info = Info(
        name = name,
        quantity = quantity, 
        submitted=submitted)
    session.add(info)
    session.commit()

def print_info():
    info = session.query(Info)
    return info

def get_one(identity):
    one = session.query(Info).filter_by(identity = identity).first()
    return one


# def check_login(username,password):



def get_user_info(username):
    info_us = session.query(Info).filter_by(submitted = username)
    return info_us


def decrease_quantity(identity):
    item = session.query(Info).filter_by(identity=identity).first()
    if item:
        item.quantity -= 1
    else:
        raise AssertionError("Item does not exist")
    session.commit()


def increase_quantity(identity):
    add = session.query(Info).filter_by(identity=identity).first()
    if add:
        add.quantity += 1
    else:
        raise AssertionError("Item does not exist")
    session.commit()


def delete_item(identity):
    delete = session.query(Info).filter_by(identity=identity).delete()
    session.commit()