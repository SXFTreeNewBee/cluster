# -*-coding:utf-8-*-
import streamlit as st
from aiohttp import ClientSession
import asyncio
import aiofile
from typing import Dict,List
from default import OS3E
from draw_graph import generate_topo
from streamlit_autorefresh import st_autorefresh
from utils.view import get_map
import os
from streamlit.components.v1 import html
def template(name, value):

	if type(value)==str :
		return f'{name}=\'{value}\'\n'
	else:
		return f'{name}={value}\n'
	
bar=st.sidebar #图面编辑背景,侧面栏

settings_path=''
class Cluster(object) :
	def __init__ (self, **kwargs) :
		self.name = kwargs['name']
		#凡是为None的，代表是可设置变量
		#Server
		self.MsgBarrier='/' #写死
		self.IP=None
		self.PORT=None
		self.QUEUE_LEN=500
		self.WAIT_CONNECT=10
		self.SERVER_RECV_BUFSIZE=204800000
		self.CLIENT_RECV_BUFSIZE=204800000
		#Controller
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
		#Topo
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
		#MAC
		self.UNKNOWN_MAC='00:00:00:00:00:00'
		self.BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'
		#是否开启集群通信
		self.IF_ARP=None
		#控制器过载阈值
		self.CONTROLLER_PKT_THRESHOLD=None
		#拓扑文件
		self.topo_html_dir=None
		
		self.show_options()
		
		self.main_page()
	def set_title(self):
		st.title(self.name)
	
	def show_options(self):
		server,  controller, topo,other= bar.tabs(
			["Server参数", "控制器","拓扑","其他选项"])
		self.server(server)
		self.controller(controller)
		self.topo(topo)
		self.other(other)
	def main_page(self):
		pass
	def server(self,server):
		with server :
			st.subheader("服务器配置")
			
			self.IP = st.selectbox('Server监听IP地址', ('192.168.10.3', '127.0.0.1'))
			
			self.PORT = st.number_input("Server监听端口", value = 8888)
			
	def controller(self,controller):
		with controller:
			st.subheader("控制器配置")
			
			self.ECHO = st.number_input("控制器监控周期",value=5)  # 单位秒
			
			self.CONTROLLER_IP = st.selectbox('控制器IP', ('127.0.0.1', '192.168.10.3'))  # 控制器的IP
			
			self.ECHO_DELAY = st.number_input("几个周期后开始request", value = 1, min_value = 1)  # 几个周期后开始request
			
			self.PERFORMANCE_STATISTIC_ECHO = st.number_input("获取交换机性能的间隔", value = 5)  # 打印交换机平均响应时延的间隔
			
	def topo(self,topo):
		
		with topo:
			st.subheader("拓扑配置选项(不显示主机)")
			self.TOPO = st.selectbox('拓扑样式', ("OS3E","自定义拓扑"))
			if self.TOPO=="OS3E":
				os3e=OS3E()
				
			else:
				#TODO 自定义拓扑显示
				pass
			st.button(label = "生成拓扑",on_click = generate_topo,kwargs = os3e.__dict__,key='topo_button')
			
	def other(self,other):
		
		with other:
			st.subheader("其他配置选项")
			self.IF_ARP=self.TOPO = st.selectbox('是否开启通信', ("1","0"))
			
			self.CONTROLLER_PKT_THRESHOLD=st.number_input("控制器阈值",value=1600)
	
	
