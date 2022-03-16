#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import shutil
import random
import requests
import subprocess

def get_config(config_path):
    if os.path.isfile(config_path):
        f = open(config_path)
        config = json.load(f)
        f.close()
    else:
        print("Config文件不存在！请检查文件路径或使用其他模式")
        exit()
    return config["mode"],config["file_path"],config["deal_duration"],config["if_gc"],config["minerid"],config["deal_times"],config["max_budget"],config["config_path"],config["encrypt_mode"],config["encrypt_key"]

def get_opt():
    #在这里设定参数默认值
    mode = "1"
    file_path = None
    deal_duration = 190
    if_gc = "n"
    minerid = None
    deal_times = 3
    max_budget = 0.5
    config_path = None
    encrypt_mode = None
    encrypt_key = "VshareCloud"
    #===============#
    args = sys.argv
    del args[0]
    for arg in args:
        arg = arg.split("=")
        opt_name = arg[0]
        opt_content = arg[1]
        if opt_name in ("--mode","-m"):
            mode = str(opt_content)
        elif opt_name in ("--imputfile","-in"):
            file_path = str(opt_content)
        elif opt_name in ("--duration","-d"):
            deal_duration = int(opt_content)
        elif opt_name in ("--gcmode","-gc"):
            if_gc = str(opt_content)
        elif opt_name in ("--minerid","-mid"):
            minerid = str(opt_content)
        elif opt_name in ("--dealtimes","-n"):
            deal_times = int(opt_content)
        elif opt_name in ("--maxbudget"):
            max_budget = float(opt_content)
        elif opt_name in ("--config"):
            config_path = str(opt_content)
        elif opt_name in ("--encryptmode"):
            encrypt_mode = str(opt_content)
        elif opt_name in ("--encryptkey","-k"):
            encrypt_key = str(opt_content)
        else :
            pass
    if config_path != None:
        return get_config(config_path)
    else:
        return mode,file_path,deal_duration,if_gc,minerid,deal_times,max_budget,config_path,encrypt_mode,encrypt_key


def get_cid(file_path,encrypt_mode,encrypt_key):
    while os.path.exists(file_path) == False:
        print("该路径文件不存在，请检查")
        exit()
    else:
        if encrypt_mode == "keyword":
            if os.path.exists("/mnt/vsahre_tmp/"):
                shutil.rmtree("/mnt/vsahre_tmp/", ignore_errors=True)
            else:
                pass
            os.makedirs("/mnt/vsahre_tmp/")
            print("加密模式为：KeyWord，开始加密")
            enc_cmd = """tar -czvf - %s | openssl enc -aes-256-cbc -salt -k %s -out /mnt/vsahre_tmp/encryped-files.tar.gz""" % (file_path,str(encrypt_key))
            subprocess.run(enc_cmd, shell=True)
            ipfs_add_cmd = """ipfs add -r /mnt/vsahre_tmp/"""
            ipfs_cli_output = str(subprocess.check_output(ipfs_add_cmd.split()), "utf-8")
            cid = ipfs_cli_output.split()[-2]
            shutil.rmtree("/mnt/vsahre_tmp/", ignore_errors=True)
        elif encrypt_mode == "rsa":
            if os.path.exists("/mnt/vsahre_tmp/"):
                shutil.rmtree("/mnt/vsahre_tmp/", ignore_errors=True)
            else:
                pass
            os.makedirs("/mnt/vsahre_tmp/")
            print("加密模式为：公私钥，开始加密")
            keygen_cmd = """openssl rand -base64 64 > /mnt/vsahre_tmp/file.rand"""
            subprocess.run(keygen_cmd, shell=True)
            enc_cmd = """tar -czvf - %s | openssl enc -aes-256-cbc -salt -k file:/mnt/vsahre_tmp/file.rand -out /mnt/vsahre_tmp/encryped-files.tar.gz""" % file_path
            subprocess.run(enc_cmd, shell=True)
            enc_rand = """openssl rsautl -encrypt -inkey %s -pubin -in /mnt/vsahre_tmp/file.rand -out /mnt/vsahre_tmp/file.rand.enc""" % encrypt_key
            subprocess.run(enc_rand, shell=True)
            rm_rand = """rm -rf /mnt/vsahre_tmp/file.rand"""
            subprocess.run(rm_rand, shell=True)
            if os.path.exists("/mnt/vsahre_tmp/file.rand") == False:
                ipfs_add_cmd = """ipfs add -r /mnt/vsahre_tmp/"""
                ipfs_cli_output = str(subprocess.check_output(ipfs_add_cmd.split()), "utf-8")
                cid = ipfs_cli_output.split()[-2]
            else:
                print("数据脱敏异常！请检查工具代码或者提交Issue")
                exit()
            shutil.rmtree("/mnt/vsahre_tmp/", ignore_errors=True)
        elif encrypt_mode == None:
            print("文件没有选择加密模式，开始处理")
            if os.path.isfile(file_path):
                ipfs_add_cmd = """ipfs add %s""" % file_path
                ipfs_cli_output = str(subprocess.check_output(ipfs_add_cmd.split()), "utf-8")
                cid = ipfs_cli_output.split()[-2]
            elif os.path.isdir(file_path):
                ipfs_add_cmd = """ipfs add -r %s""" % file_path
                ipfs_cli_output = str(subprocess.check_output(ipfs_add_cmd.split()), "utf-8")
                cid = ipfs_cli_output.split()[-2]
            else:
                pass
        else:
            pass
    print("已获取到CID：%s" % cid)
    return cid

def get_vshare_nodeid():
    minerid_list = json.loads(requests.get('https://fil-api.ipns.tech/filtools/miner_list.php').text)
    minerid_list = minerid_list["data"]
    minerid = random.choice(minerid_list)
    print("已选取到节点：%s" % minerid)
    return minerid

def ipfs_gc(cid):
    print("开始垃圾清理")
    subprocess.run("ipfs pin rm %s" % cid, shell=True)
    print("垃圾清理已完成")
    pass

#Main
opt = get_opt()
mode = opt[0]
cid = get_cid(opt[1],opt[8],opt[9])
deal_duration = opt[2]
if_gc = opt[3]
minerid = opt[4]
deal_times = opt[5]
max_budget = opt[6]
config_path = opt[7]
# encrypt_mode = opt[8]
# encrypt_key = opt[9]
if mode == "1":
    minerid = get_vshare_nodeid()
    cmd = "expect /opt/vsharecloud-tools/scripts/single_deal.sh %s %s %s" % (cid, deal_duration, minerid)
    subprocess.run(cmd, shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("无需清理垃圾")
    exit()
elif mode == "2":
    cmd = "expect /opt/vsharecloud-tools/scripts/single_deal.sh %s %s %s" % (cid, deal_duration, minerid)
    subprocess.run(cmd, shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("无需清理垃圾")
    exit()
elif mode == "3":
    cmd = "expect /opt/vsharecloud-tools/scripts/global_deal.sh %s %s %s %s" % (cid, deal_duration, max_budget, deal_times)
    subprocess.run(cmd, shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("无需清理垃圾")
    exit()
else:
    print("模式参数无效，退出程序")
    exit()