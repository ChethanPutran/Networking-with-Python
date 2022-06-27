import matplotlib
import networkx
from easysnmp import Session
from pprint import pprint

ip = input("\nEnter the 'root' device IP Address :")

ospf = []
authPass = "shapass1234"
privacyPass = "aespass1234"
uname = "chetu"

def ospfMaper():
    
    #creating empty lists for adding discovered devices
    nbridlist = []
    nbriplist = []
    ospfDevice = []
    
    #Opening SNMPv3 session to the device
    session = Session(hostname = ip, version = 3, security_level = "auth_with_privacy",security_username=uname,auth_protocol="SHA",auth_password=authPass,privacy_protocol="AES",privacy_password=privacyPass)
    
    #Getting device OSPF ID
    snmp_walk = session.walk('')