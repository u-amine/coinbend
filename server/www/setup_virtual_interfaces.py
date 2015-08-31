import re
import netifaces
import ipaddress

addr = netifaces.ifaddresses("eth1")[netifaces.AF_INET][0]
static_ip = addr["addr"]
netmask = addr["netmask"]
broadcast = addr["broadcast"]
broadcast2 = ".".join(static_ip.split(".")[0:2]) + ".255"
vif = ""
for i in range(1, 5 + 1):
    vip = str(ipaddress.IPv4Address(static_ip) + i)
    if i < 5:
        nl = "\n"
    else:
        nl = ""
    line = "    up ip addr add %s brd %s dev eth1 label eth1:%s%s" % (vip, broadcast, str(i), nl)
    vif += line

interfaces = """# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet dhcp
dns-nameservers 8.8.8.8 8.8.4.4

#VAGRANT-BEGIN
# The contents below are automatically generated by Vagrant. Do not modify.
auto eth1
iface eth1 inet static
    label eth1
    address %s
    netmask %s
    broadcast %s
    dns-servers 8.8.4.4 8.8.8.8
    dns-nameservers 8.8.4.4 8.8.8.8
%s
#VAGRANT-END
""" % (static_ip, netmask, broadcast2, vif)

with open("/etc/network/interfaces", 'w') as fp:
    fp.truncate()
    fp.write(interfaces)
    fp.close()
