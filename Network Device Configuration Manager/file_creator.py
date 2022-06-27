import datetime
path = "~./config_files/"

ip_file = open("ipaddres.text", 'r')
ip = ip_file.readlines()[0].lstrip('\n')

with open(path+ ip + '_' + datetime.date.today().isoformat()+".txt",'w') as fp:
    pass
