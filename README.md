# Filecoin-Storage-Tool 
VshareCloud-CLI

>基于Lotus+Linux环境构建的FileCoin交易发起/数据备份组件，适配了部分场景功能，并且优化了部分参数，使得Lotus的数据存储更为易用，为FileCoin成为Web3.0数字世界基石打下基础。

### 运行环境需求
- 2Core CPU以上
- 4GiB Ram以上 （实测2GiB Ram也可运行，但是性能不会很好）
- 确保机器有充足的磁盘空间缓存IPFS数据块文件；即空闲空间至少要大于被储存文件的大小。
- 支持Systemd的Linux系统
### 安装
- 1.安装Rust 
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
- 2.主要组件安装
```
wget --no-check-certificate https://gateway.ipns.tech/ipns/vsharecloud-tools-install.ipns.network/install.sh -O install.sh && sudo bash install.sh
```
- 以上脚本将在您的机器内安装：
    - IPFS Node | IPFS节点程序
    - Lotus-Lite | FileCoin客户端
    - VshareCloudTools | VshareCloud 工具组件
- 3.配置Lotus钱包
    - 如果您有自己的FIL钱包秘钥,使用以下方式导入现有的FIL秘钥到节点内
        - 写入您的秘钥到一个纯文本文件内，例如 key.txt
        - 上传 key.txt 到服务器内
        - 执行 `lotus wallet import key.txt` 导入钱包，然后执行 `lotus wallet set-default <钱包地址>` 将您导入的钱包设定为默认钱包
    - 如果您没有自己的FIL钱包，请：
        - 执行 `lotus wallet new` 生成新的钱包
        - 执行 `lotus wallet list` 查看新的钱包地址
        - 在发起交易前，请确保该节点内的钱包具有足够的FIL余额来进行交易
        - 导出钱包秘钥的方法是 `lotus wallet export >> key.txt`
    - Tips | 小技巧
        - Filecoin的储存市场部分是使用单独的支付通道进行支付（以此来避免每次交易都要发起链上转账，从而导致过高的TPS消耗），所以还需要单独发起一笔储存市场“充值”转账，以确保自己的账户在储存市场已有足够资金来支付存储费用。否则会在每一次发起交易时，由lotus客户端单独发起一笔充值转账，这会导致不必要的链上Gas费消耗（往往可能是交易资金的好几倍）和占用公链资源。
        
        - 充值方法：
        ```
        lotus wallet market add --address <钱包地址> <充值金额>
        ```
        - 提取余额方法：
        ```
        lotus wallet market withdraw --address <钱包地址> <提取金额>
        ```
        - 查询自己在储存市场的余额：
        ```
        lotus state market balance <钱包地址>
        ```
- 4.开始储存交易
```
root@devmachine:~# vsharecloud-cli
 1.托管数据至VshareCloud  #托管数据到VshareCloud联盟的FileCoin节点[*]
 2.托管数据到自定义FileCoin节点 #自定义托管节点
 3.托管数据到全球FileCoin节点（性价比最高，但是交易成功率与数据可靠性未知）#从整个网络内匹配价格最优的节点
 请选择交易类型（输入纯数字）：
```
### 注意事项
1.所有的上链数据都是面向整个网络公开的，如果您用于储存重要的数据，请先将内容进行加密打包后再储存

2.储存交易对于数据大小有一定的要求，建议单笔数据存储交易的数据大小不小于16MiB且不大于60GiB，否则可能不会被接受

3.储存后请自己保存好文件的CID和订单号等信息，便于后续取回数据

#### *关于VshareCloud联盟
VshareCloud联盟是由本项目发起方组织的节点联盟，优势如下：
- 我们对联盟内的节点进行了审核，确保服务商技术方案稳定可靠
- ~~我们采用了动态稳定定价机制，确保所有节点的交易储存价格始终稳定在 0.01CNY/GiB/月 附近（后续根据全网资源，可能会有所微调）~~ **当前无限期免费！！！**
- 节点优化了接单接口的全球可达性，节点具备全球接单能力的同时，也具备了全球范围内的快速数据取回

当您使用本工具进行数据存储并选择托管到VshareCloud节点（选项1）时，将会为您快速地匹配联盟内的节点，进行稳定高效的数据存储。

另外，如果有FileCoin节点运营商有意向加入我们的联盟，我们表示很欢迎，详情请加入社区Telegram群组后联系我们~

### 数据取回
- 1.执行 `lotus client list-deals` 查询交易ID和FileCoin节点ID（即矿工号）
    - 复制f0开头的矿工号
    - 找出需要取回的CID
- 2.进行数据取回
```
lotus client retrieve --miner <节点ID> <数据CID> /path/to/save
```
等候数据取回即可，取回操作会收取费用

欢迎大家上手测试，有问题请提交Issue~

### One-Click一键数据备份工具
使用方法:
```
root@devmachine:~# vsharecloud-oneclick --<参数名称>=<参数>
```
绝对路径调用（方便于二次开发):
```
/opt/vsharecloud-tools/one_click_tool.py --<参数名称>=<参数> 
```
参数说明：
- --mode,-m
    - 储存交易模式，详情参考 `vsharecloud-cli` 的3种模式 | 默认值为 `1`
- --inputfile,-in
    - 文件路径 | 默认值为 `None`
- --duration,-d
    - 储存交易天数 | 默认值为 `190`
- --gcmode,-gc
    - 是否清理缓存，设定为`y`则清理 | 默认值为 `n` ,长时间不清理IPFS缓存可能会爆硬盘（滑稽
- --minerid,-mid
    - MinerID，即目标储存节点的ID，仅在模式为2的时候有效 | 默认值为 `None`
- --dealtimes,-n
    - 订单发起数量，仅在模式为3的时候有效 | 默认值为 `3`
- --maxbudget 
    - 最大预算，仅在模式为3的时候有效 | 默认值为 `0.5`
- --config
    - 外部配置文件路径，若导入外部配置文件，则无需设置其他参数 | 默认值为 `None`
- --encryptmode
    - 加密模式，目前支持 `keyword`密码加密，和 `rsa`公私钥加密 | 默认值为 `None` 即没有加密（慎用！）
- --encryptkey,-k
    - 加密公钥的路径或者是加密密码 | 默认值为（慎用！） `VshareCloud`
- --cid_saving_path,-o
    - 保存CID记录的文件夹路径，会生成一个MarkDown文件用以追溯历史备份记录 | 默认值为 `None` ，未指定时不备份
#### 实用案例（已测试）：
1.模拟，适配`宝塔面板`数据库备份场景，公私钥模式：
```
/opt/vsharecloud-tools/one_click_tool.py -gc=y --encryptmode=rsa -k=/www/wwwroot/pub.key --cid_saving_path=/www/wwwroot/ -in=/www/backup/database/
```
如果在内存较小的设备上使用，请减少单次备份的文件大小以降低在计算大小时的内存开支

如果不希望IPFS占用过多的内存和CPU资源，请执行：
```
ipfs config --json Routing.Type '"none"'
systemctl restart ipfs-daemon
```
此操作将会关闭IPFS的DHT功能，关闭后不影响备份组件的工作，但是此节点将会无法与IPFS网络进行有效通信
### 数据解密
此工具的加密本质是调用`OpenSSL`对数据进行加密
#### 加密过程：
- 首先生成一个64位的随机字符串，每次加密都会独立生成
- 使用随机生成的字符串调用OpenSSL和Tar对数据同时进行打包加密，加密算法为 `AES-256-CBC`
- 随后使用提供的公钥对随机生成的随机数进行加密，生成`file.rand.enc`，所以此文件会存在于每个使用本工具加密的文件CID路径中。
#### 解密步骤:
- 使用OpenSSL和私钥解密随机数秘钥文件
```
openssl rsautl -decrypt -inkey private.key -in file.rand.enc -out file.rand
```
- 使用解密后的随机数文件解密文件
```
openssl enc -d -aes-256-cbc -k file:file.rand -in encrypted-files.tar.gz | tar xzvf -
```
### 社区：
- 频道：https://t.me/vsharebetter
- 群组：https://t.me/ipns_tech
