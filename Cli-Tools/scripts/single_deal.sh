#!/usr/bin/expect
set timeout -1
set cid [lindex $argv 0]
set duration [lindex $argv 1]
set minerid [lindex $argv 2]
#基础检查
if {$duration < 180} {
    send_user "交易时长设定必须大于180天"
    exit 1
}
#发起交易，导入CID
spawn /usr/local/bin/lotus client deal
expect "Data CID "
send "${cid}\r"
#设定交易时间
expect "Deal duration "
send "${duration}\r"
#搜索矿工
expect "Miner Addresses"
send "${minerid}\r"
#确认交易
expect "Accept "
send "yes\r"
#结束
expect eof
exit