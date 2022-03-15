# -*- coding: utf-8 -*-
import json
import MySQLdb
import os
import time
import requests
from datetime import datetime

config_path = "" #Input Config Abs Path here
#Import SQL Config
def get_db_config(sqlname):
    if os.path.isfile(config_path + "/"+ sqlname +".json"):
        f = open(config_path + "/"+ sqlname +".json")
        sqlpwd = json.load(f)
        f.close()
    else:
        print("SQL Config 文件不存在！")
        exit()
    return sqlpwd


#获取SQL游标
def get_db_cursor(sql_config):
    db = MySQLdb.connect(host=sql_config['host'], port=sql_config['port'], user=sql_config['username'], passwd=sql_config['password'], db=sql_config['db'], charset='utf8' )
    cursor = db.cursor()
    return db,cursor

def get_binance_pirce():
    b_data = json.loads(requests.get('https://api.binance.com/api/v3/ticker/price?symbol=FILUSDT').text)
    return float(b_data["price"])

def submit_to_sql(price1):
    sql_config = get_db_config("sql")
    sql = get_db_cursor(sql_config)
    db = sql[0]
    cursor = sql[1]
    get_c_cmd = """SELECT * FROM `fil_storage_price`"""
    cursor.execute(get_c_cmd)
    price_config = cursor.fetchone()
    usd_exchange_rate = price_config[2]
    current_storage_price = price_config[4]
    exchange_rate =  price1
    fil_stable_price = current_storage_price / (exchange_rate * usd_exchange_rate) / 86400
    log_price1 = """INSERT INTO `c2c_price` (`time`, `price1`) VALUES ('%s', '%s')""" % (int(time.time()), price1)
    update_price = """UPDATE `fil_storage_price` SET `exchange_rate` = '%s' WHERE `fil_storage_price`.`id` = '1'""" % exchange_rate
    update_stable_price = """UPDATE `fil_storage_price` SET `fil_stable_price` = '%s' WHERE `fil_storage_price`.`id` = '1'""" % fil_stable_price
    try:
        cursor.execute(log_price1)
        cursor.execute(update_price)
        cursor.execute(update_stable_price)
        db.commit()
    except:
        db.rollback()
        db.close()
        exit()
    db.close()

#Main
price1 = get_binance_pirce()
submit_to_sql(price1)