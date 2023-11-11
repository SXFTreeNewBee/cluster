# -*-coding:utf-8-*-
from typing import Dict,List
def get_map (LINKS: dict,CONTROLLERS:list) :
	PREPARE = ["s" + str(i) for i in range(10, 60)]
	ALL = PREPARE.copy()
	for k in LINKS.keys() :
		
		if k[0] in PREPARE :
			PREPARE.remove(k[0])
		if k[1] in PREPARE :
			PREPARE.remove(k[1])
	for h in PREPARE :
		ALL.remove(h)
	
	HOSTS = { }
	SW_LIST = [[] for _ in range(len(CONTROLLERS))]  # n个控制器
	HOST_LIST = [[] for _ in range(len(CONTROLLERS))]
	
	def h (x) :
		# 3 台主机
		return x, ["h" + x.split("s")[1] + '01', "h" + x.split("s")[1] + '02', "h" + x.split("s")[1] + '03']
	
	for host in map(h, ALL) :
		HOSTS[host[0]] = host[1]
	
	for c in ALL :
		SW_LIST[int(list(c)[1]) - 1].append(c)
		# 3 台主机
		HOST_LIST[int(list(c)[1]) - 1].append(
			["h" + c.split("s")[1] + '01', "h" + c.split("s")[1] + '02', "h" + c.split("s")[1] + '03'])
	
	return HOSTS, SW_LIST, HOST_LIST
