#!/bin/bash
# v1.0.0
echo=echo
for cmd in echo /bin/echo; do
    $cmd >/dev/null 2>&1 || continue

    if ! $cmd -e "" | grep -qE '^-e'; then
        echo=$cmd
        break
    fi
done

CSI=$($echo -e "\033[")
CEND="${CSI}0m"
CDGREEN="${CSI}32m"
CRED="${CSI}1;31m"
CGREEN="${CSI}1;32m"
CYELLOW="${CSI}1;33m"
CBLUE="${CSI}1;34m"
CMAGENTA="${CSI}1;35m"
CCYAN="${CSI}1;36m"

OUT_ALERT() {
    echo -e "${CYELLOW}$1${CEND}"
}

OUT_ERROR() {
    echo -e "${CRED}$1${CEND}"
}

OUT_INFO() {
    echo -e "${CCYAN}$1${CEND}"
}

if [[ -f /etc/redhat-release ]]; then
    release="centos"
elif cat /etc/issue | grep -q -E -i "debian"; then
    release="debian"
elif cat /etc/issue | grep -q -E -i "ubuntu"; then
    release="ubuntu"
elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
    release="centos"
elif cat /proc/version | grep -q -E -i "raspbian|debian"; then
    release="debian"
elif cat /proc/version | grep -q -E -i "ubuntu"; then
    release="ubuntu"
elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
    release="centos"
elif cat /proc/version | grep -q -E -i "deepin"; then
    release="deepin"
else
    OUT_ERROR "[错误] 不支持的操作系统！"
    exit 1
fi
OUT_ALERT "[信息] 操作系统检查完成！"
OUT_ALERT "[信息] 更新系统中！"
if [[ ${release} == "centos" ]]; then
    yum makecache
    yum install epel-release -y

    yum update -y
else
    apt update
    apt dist-upgrade -y
    apt autoremove --purge -y
fi

OUT_ALERT "[信息] 依赖软件安装"
if [[ ${release} == "centos" ]]; then
    yum install wget gcc python3 python3-pip mariadb-devel python3-devel expect -y
else
    apt install wget python3 python3-pip expect -y
fi

OUT_ALERT "[信息] Py依赖包安装"
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

OUT_ALERT "[信息] 核心组件安装"
set -e
if [ ! -e /root/.ipfs/config ]; then
    OUT_ALERT "[信息] IPFS不存在，正在安装"
    wget --no-check-certificate "https://gateway.ipns.tech/ipns/install-sh.ipns.network/ipfs-autoinstall.sh" -O ipfs-autoinstall.sh && bash ipfs-autoinstall.sh
fi
OUT_ALERT "[信息] lotus-lite安装"
if [ -e /tmp/lotuslite_install ]; then
    rm -rf /tmp/lotuslite_install
fi
mkdir /tmp/lotuslite_install
cd /tmp/lotuslite_install
if [ -e /usr/local/bin/lotus ]; then
    rm -rf /usr/local/bin/lotus
fi
wget --no-check-certificate "https://gateway.ipns.tech/ipfs/QmUKKCBBYtSax2diUDhDJHnXMsW7wWoR2fa3RdqfLTAqDw" -O lotus.tar.gz
tar zxvf lotus.tar.gz
cp -f lotus /usr/local/bin/
chmod +x /usr/local/bin/lotus
rm -rf /tmp/lotuslite_install
cd ~
echo "Install Done"

# Set Service File
cat >/etc/systemd/system/lotus-lite.service <<EOF
[Unit]
Description=Lotus Lite Daemon
After=network-online.target
Requires=network-online.target

[Service]
User=root
Group=root
LimitCPU=infinity
LimitFSIZE=infinity
LimitDATA=infinity
LimitSTACK=infinity
LimitCORE=infinity
LimitRSS=infinity
LimitNOFILE=infinity
LimitAS=infinity
LimitNPROC=infinity
LimitMEMLOCK=infinity
LimitLOCKS=infinity
LimitSIGPENDING=infinity
LimitMSGQUEUE=infinity
LimitRTPRIO=infinity
LimitRTTIME=infinity
Environment=GOLOG_FILE=/var/log/lotus-lite-daemon.log
Environment=GOLOG_LOG_FMT=json
Environment=GOPROXY=https://goproxy.cn
Environment=FULLNODE_API_INFO=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBbGxvdyI6WyJyZWFkIiwid3JpdGUiLCJzaWduIl19.GF9HWsMl2maRvU2ra2JeEL7DrEK4LnGNIaOi9Ld91GY:/dns4/lotus-api.ipns.tech/tcp/80/http
ExecStart=/usr/local/bin/lotus daemon --lite
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
echo "Set service Done"
systemctl restart lotus-lite
systemctl stop lotus-lite
wget --no-check-certificate "https://gateway.ipns.tech/ipfs/QmYdZ6tg3vxtmG3ADzjKi4i8uxzPHqihJfGFT6XfFT4768" -O /root/.lotus/config.toml
systemctl enable --now lotus-lite

exit 0
