
import subprocess
import sys

ip = '10.10.10.3'


ping_reply = subprocess.call(['ping','-c','2',ip],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

if ping_reply == 0:
    print("\n{} is reachable :)".format(ip))
else:
    print("\n{} is not reachable :(".format(ip))
    sys.exit()

###Running the python using intermediary server Windows-->ubuntu-->cisko_switch

from jumpssh import SSHSession

server_session = SSHSession("10.10.10.100",'chetu',password='9535').open()
switch_session = server_session.get_remote_session('10.10.103', 'admin', password='admin1')
print(switch_session.get_cmd_output('show ip int brief'))
server_session.close()

#Instructions
###########Example for running local script on remote server
#more filepath\file_name.py | ssh user@ip password

###########Example for running remote script via local machine
#ssh user@ip "python3 /path/file_name.py"