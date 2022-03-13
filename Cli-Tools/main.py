# -*- coding: utf-8 -*-
import json
import os
import random
import requests
import subprocess

def get_cid():
    cid = "localfile"
    cid = input("请输入CID（直接回车导入本地文件）：")
    if cid == "localfile":
        file_path = input("请输入文件绝对路径：")
        while os.path.exists(file_path) == False:
            print("该路径文件不存在，请重新输入")
        else:
            if os.path.isfile(file_path):
                ipfs_add_cmd = """ipfs add %s"""
            elif os.path.isfile(file_path):
                ipfs_add_cmd = """ipfs add -r %s"""
            else:
                pass
    else:
        pass
    ipfs_cli_output = str(subprocess.check_output(ipfs_add_cmd.split()), "utf-8")
    cid = ipfs_cli_output.split()[-2]
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
mode = input("请选择交易类型（输入纯数字）：\n 1.托管数据至VshareCloud\n 2.托管数据到自定义FileCoin节点\n 3.托管数据到全球FileCoin节点（性价比最高，但是交易成功率与数据可靠性未知）")
deal_duration = input("请输入交易天数（纯数字）：")
cid = get_cid()
if mode == "1":
    minerid = get_vshare_nodeid()
    subprocess.run("expect /opt/vsharecloud-tools/scripts/single_deal.sh %s %s %s" % (cid, deal_duration, minerid), shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if_gc = input("是否清理刚刚导入的文件缓存？(y/n)")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("程序退出")
    exit()
elif mode == "2":
    minerid = input("请输入FileCoin节点ID（格式：f0xxxxx）：")
    subprocess.run("expect /opt/vsharecloud-tools/scripts/single_deal.sh %s %s %s" % (cid, deal_duration, minerid), shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if_gc = input("是否清理刚刚导入的文件缓存？(y/n)")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("程序退出")
    exit()
elif mode == "3":
    deal_times = input("请输入本次发起的交易次数（纯数字）：")
    max_budget = input("请输入最大的价格预算（纯数字）")
    subprocess.run("expect /opt/vsharecloud-tools/scripts/global_deal.sh %s %s %s %s" % (cid, deal_duration, max_budget, deal_times), shell=True)
    print("交易已发起，请通过命令 lotus client list-deals 查询交易状态")
    if_gc = input("是否清理刚刚导入的文件缓存？(y/n)")
    if if_gc == "y":
        ipfs_gc(cid)
    else:
        print("程序退出")
    exit()
else:
    print("输入无效，退出程序")
    exit()