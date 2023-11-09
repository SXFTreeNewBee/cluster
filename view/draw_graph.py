# -*-coding:utf-8-*-
from pyvis.network import Network
import sys
sys.path.append('..')
import streamlit as st
import os
import aiofile

net=Network()
parent_html_dir='../static/topo'
def generate_topo (**kwargs) :
	html_name=kwargs['name']
	controllers=kwargs["CONTROLLERS"]
	edge_link=kwargs['EDGE_LINK']
	sw_link=kwargs['SW_LINK']
	sw_host=kwargs['SW_HOST']
	sws=['SWS']
	hosts=['HOSTS']

	controller_list=[controller for controller in controllers]
	net.add_nodes(controller_list,
	              title=[f'控制器{controller}' for controller  in controllers],
	              label=controller_list,
	              color=["#EE2C2C" for _ in range(len(controller_list))])
	net.save_graph(f'{parent_html_dir}/{html_name}.html')
	
	