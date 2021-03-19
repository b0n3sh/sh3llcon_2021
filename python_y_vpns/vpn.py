import json
from time import sleep
import subprocess 
import random
import requests

def vpn_extract(): 
	servers_def = []
	web = requests.get('https://nordvpn.com/api/server')
	servers = json.loads(web.text)

	for server in servers:
		try:
			if server['categories'][0]['name']=='Standard VPN servers':
				servers_def.append(server['domain'].split('.')[0])
		except:
			pass
	return servers_def

def vpn_connect():
	result = subprocess.run(['nordvpn', 'c', random.choice(vpn_extract())], capture_output=True)

#while 1:
vpn_connect()
	#sleep(5)





	
