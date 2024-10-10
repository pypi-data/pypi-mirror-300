from dhcpy import Server, send_dhcp6_config_to_server, save_config
from dhcpy.subnet import SubnetType
# from dhcpy.sendToServer import get_config
import json

# Create a server object
kea_server = Server(
    mgmt_ip4="198.19.249.59",
    hostname="kea0",
    interfaces=["prod"])
print("getting config")
# kea_server.get_config(ssl=False)
#
# print(f"v4_socket: {kea_server.v4_socket}")
# print(f"v6_socket: {kea_server.v6_socket}")

kea_server.get_v6_config(ssl=False)
two = send_dhcp6_config_to_server(kea_server, kea_server.dhcp_v6_service.__dict__(), ssl=False)
print(two)
three = save_config(kea_server, ssl=False)
print(three)
