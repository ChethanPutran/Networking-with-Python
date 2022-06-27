#Info about interfaces
import requests
import sys

#Allow self signed certs
requests.packages.urllib3.disable_warnings()

#Credentials
USER = 'developer'
PASS = 'Cisco12345'

#URL for GET requests
url = "https://sandboxdnac.cisco.com"

#Set yang+json as the data formats
headers = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}

#Run GET
response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)

print(response.text)