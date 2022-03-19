# -*- coding: utf-8 -*-
import os,time,MySQLdb,json,sys,subprocess

def get_opt():
    #在这里设定参数默认值
    config_path = None
    packup_path = None
    #===============#
    args = sys.argv
    del args[0]
    for arg in args:
        arg = arg.split("=")
        opt_name = arg[0]
        opt_content = arg[1]
        if opt_name in ("--config"):
            config_path = str(opt_content)
        elif opt_name in ("--packup-path"):
            packup_path = str(opt_content)
        else :
            pass
    return config_path,packup_path

def get_db_config(config_path):
    if os.path.isfile(config_path):
        f = open(config_path)
        sqlpwd = json.load(f)
        f.close()
    else:
        print("SQL Config 文件不存在！")
        exit()
    return sqlpwd

def getDatabaseNames(sql_config):
    db = MySQLdb.connect(host=sql_config['host'], port=sql_config['port'], user=sql_config['username'], passwd=sql_config['password'], db=sql_config['db'], charset='utf8')
    cursor = db.cursor()
    cursor.execute('show databases;')
    dbs = cursor.fetchall()
    db.close()
    return dbs

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

#Main
config_path = get_opt()[0]
packup_path = get_opt()[1]
sql_config = get_db_config(config_path)
timestr = time.strftime("%Y%m%d-%H%M%S",time.localtime(time.time()))
if os.path.exists(packup_path) == False:
    os.makedirs(packup_path)
else:
    pass
dbs = getDatabaseNames(sql_config)
print(dbs)
for db in dbs:
    try:
        dbname = db[0]
        if dbname=="mysql" or dbname=="performance_schema" or dbname=="information_schema" or dbname=="sys":
            pass
        else:
            cmd = "mysqldump -u%s -p%s %s > %s/%s.sql" % (sql_config['username'], sql_config['password'], dbname, packup_path, (dbname+"_"+timestr))
            print(cmd)
            subprocess.run(cmd,shell=True)
    except Exception as error:
        print(error)