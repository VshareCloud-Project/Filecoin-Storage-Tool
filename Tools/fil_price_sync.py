# -*- coding: utf-8 -*-
import json
import os
import requests
import subprocess

def get_pirce_data():
    price_data = json.loads(requests.get('https://fil-api.ipns.tech/filtools/check_price.php').text)
    return price_data["data"]

#Main
price_data = get_pirce_data()
cmd = """/usr/local/bin/lotus-miner storage-deals set-ask --price %s --verified-price 0.000000000000000001 --min-piece-size 16MiB --max-piece-size 60GiB""" % price_data["fil_stable_price"]
subprocess.run(cmd, shell=True)
print("价格已更新至：" + str(price_data["fil_stable_price"]))