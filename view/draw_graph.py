# -*-coding:utf-8-*-
import time
from pyvis.network import Network
import sys
from streamlit.components.v1 import html
sys.path.append('..')
import streamlit as st
import os
import aiofile
from typing import List,Dict
from jinja2 import Template
from style import controller_style,switch_style,host_style,edge_style,internal_style,controller_link_style
from random import Random
import pandas as pd
random=Random()

net=Network()

parent_html_dir='../static/'

path_to_notification='../static/notify/notification.html'

topo_html_dir=None
def generate_network (**kwargs) :
	global topo_html_dir,if_generate_topo
	html_name=kwargs['name']
	controllers=kwargs["CONTROLLERS"]
	edge_link=kwargs['EDGE_LINK']
	sw_link=kwargs['SW_LINK']
	sws=kwargs['SWS']

	#添加控制器

	for controller in controllers:
		net.add_node(controller,
		              title=f'控制器{controller}',
		              label=controller,

		              **controller_style)

	#添加交换机
	for index, sw_list in enumerate(sws) :
		for s in sw_list :
			net.add_node(
				s,title=f'交换机{s}',label = s,**switch_style,
						)

	time.sleep(0.5)

	#添加链路
	
	for edge in edge_link.keys():#边界链路
		net.add_edge(edge[0],edge[1],title=f'边界链路:{edge[0]} <=> {edge[1]}',**edge_style)
	
	for internal in sw_link.keys():#内部链路
		net.add_edge(internal[0],internal[1],title=f'内部链路:{internal[0]} <=> {internal[1]}',**internal_style)
	
	for index,controller in enumerate(controllers):#添加控制器与交换机的链路
		
		for sw in sws[index]:
			net.add_edge(controller,sw,**controller_link_style)

	path_to_file=f'{parent_html_dir}/topo/{html_name}.html'
	
	net.save_graph(path_to_file)

	show_notify()
	
	topo_html_dir=path_to_file
	
	show_main_page(kwargs)
def show_main_page (args:dict) :
	topo_image, cluster_info, cluster_status = st.tabs(['拓扑图', '网络配置信息', '网络状态'])
	
	with topo_image :
		show_topo()
	with cluster_info:
		show_info(args)
	with cluster_status:
		show_status()
def show_notify () :
	
	file=path_to_notification
	
	if not os.path.exists(file) :
		raise FileNotFoundError
	
	with open(file, 'r', encoding = 'utf-8') as f :
		content = f.read()
	
	html(content, width = 0, height = 0)#加载弹窗
def show_topo () :
	global topo_html_dir
	
	file=topo_html_dir
	
	if not os.path.exists(file) :
		raise FileNotFoundError
	
	with open(file, 'r', encoding = 'utf-8') as f :
		content = f.read()
	
	html(content, width = 1000, height = 600, scrolling = True)#加载拓扑图
def show_info(args:dict):
	df = pd.DataFrame({
		"controllers" : [controller for controller in args['CONTROLLERS']],
		"IP" : ['127.0.0.1' for _ in range(len(args['CONTROLLERS']))],
		"port" : [port for port in args['CONTROLLER_PORTS']],
		"switches" : [sws for sws in args['SWS']],
	})
	column_config = {
		"switches" : st.column_config.ListColumn(
			label = "交换机",
			help = "该控制下所掌管的交换机集合",
			width = "large"
		),
		"IP" : st.column_config.ListColumn(
			label = "IP",
			help = "控制器IP",
			width = "small"
		),
		"controllers" : st.column_config.ListColumn(
			label = "名称",
			help = "控制器名称",
			width = "small"
		), "port" : st.column_config.ListColumn(
			label = "端口",
			help = "控制器服务端口",
			width = "small"
		)
	}
	st.data_editor(df, column_config = column_config,
	               hide_index = True
	               )
def show_status():
	pass
	