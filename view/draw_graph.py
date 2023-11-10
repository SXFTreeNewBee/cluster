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

random=Random()

net=Network()

parent_html_dir='../static/'

path_to_notification='../static/notify/notification.html'

def generate_topo (**kwargs) :
	html_name=kwargs['name']
	controllers=kwargs["CONTROLLERS"]
	edge_link=kwargs['EDGE_LINK']
	sw_link=kwargs['SW_LINK']
	sw_host=kwargs['SW_HOST']
	sws=kwargs['SWS']
	hosts=kwargs['HOSTS']
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
	
	show(file=path_to_notification)
	
	show(path_to_file)


def show (file: str) :
	if not os.path.exists(file) :
		raise FileNotFoundError
	
	with open(file, 'r', encoding = 'utf-8') as f :
		content = f.read()
	
	with st.container() :
		html(content, width = 800, height = 600,scrolling = True)


	