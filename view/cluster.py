# -*-coding:utf-8-*-
import streamlit as st
from aiohttp import ClientSession
import asyncio
from typing import Dict,List
from streamlit_autorefresh import st_autorefresh
def template(name, value):

	if type(value)==str :
		return f'{name}=\'{value}\'\n'
	else:
		return f'{name}={value}\n'
	
bar=st.sidebar #图面编辑背景

settings_path=''
class Cluster(object) :
	def __init__ (self, **kwargs) :
		self.name = kwargs['name']
		
		self.MsgBarrier='/' #写死
		self.IP=None
		self.PORT=None
		self.QUEUE_LEN=500
		self.WAIT_CONNECT=10
		self.SERVER_RECV_BUFSIZE=204800000
		self.CLIENT_RECV_BUFSIZE=204800000
		
		self.ECHO=None
		self.CONTROLLER_IP=None
		self.OFP_VERSION='OpenFlow13'
		self.ECHO_DELAY=None
		self.PERFORMANCE_STATISTIC_ECHO=None
		self.SW_TO_SW_PRIORITY = 30
		self.IPV6_PRIORITY = 65534
		self.SW_TO_HOST_PRIORITY = 50
		self.TABLEMISS_PRIORITY = 0
		self.CROSSREQUIRE_PRIORITY = 30
		self.IDLE_TIME_OUT = 0
		self.HARD_TIME_OUT = 0
		
		self.TOPO=None
		self.CONTROLLERS=None
		self.CONTROLLER_PORTS=None
		self.EDGE_LINK=None
		self.SW_LINK =None
		self.SW_HOST=None
		self.SWS=None
		self.HOSTS=None
		self.ADJACENCY_CONTROLLER=None
		self.CONTROLLERS_EDGE_SWITCHES_AREA =None
		self.CONTROLLER_EDGE_SWITCHES=None
		
		self.UNKNOWN_MAC='00:00:00:00:00:00'
		self.BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'
		
		self.IF_ARP=None
		
		self.CONTROLLER_PKT_THRESHOLD=None
		
		self.show_options()
	def set_title(self):
		st.title(self.name)
	
	def show_options(self):
		server,  controller, = bar.tabs(
			["Server参数", "控制器"])
		with server:
			st.subheader("服务器配置")
			
			self.IP = st.selectbox('Server监听IP地址', ('192.168.10.3', '127.0.0.1'))
			
			self.PORT = st.number_input("Server监听端口", value = 8888)
		with controller:
			st.subheader("控制器配置")
	
	@staticmethod
	def get_map(LINKS:Dict):
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
		SW_LIST = [[] for _ in range(5)]  # 5个控制器
		HOST_LIST = [[] for _ in range(5)]
		
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