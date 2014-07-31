# 1. 清除规则
iptables -F
iptables -X
iptables -Z

iptables -t nat -F
iptables -t nat -X
iptables -t nat -Z

# 2. 设定默认策略
iptables -P   INPUT DROP
iptables -P  OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# 3~5. 规则制定
# filter
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -i eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -s 172.16.0.0/16 -j ACCEPT
iptables -A INPUT -p tcp  --dport 10001 -j ACCEPT
iptables -A INPUT -p tcp  --dport 10002 -j ACCEPT

# nat

#iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 10001  -j DNAT --to-destination 172.16.18.32:25101

# 6. 保存
/etc/init.d/iptables save
