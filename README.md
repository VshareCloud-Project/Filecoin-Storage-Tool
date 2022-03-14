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
wget --no-check-certificate https://gateway.ipns.tech/ipns/vsharecloud-tools-install.ipns.network/install.sh -O install.sh && bash install.sh
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
- 我们采用了动态稳定定价机制，确保所有节点的交易储存价格始终稳定在 0.01CNY/GiB/月 附近（后续根据全网资源，可能会有所微调）
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
#### 社区：
- 频道：https://t.me/vsharebetter
- 群组：https://t.me/ipns_tech