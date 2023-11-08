# -*-coding:utf-8-*-
import streamlit as st
from aiohttp import ClientSession
import asyncio
from streamlit_autorefresh import st_autorefresh
def template(name, value):

	if type(value)==str :
		return f'{name}=\'{value}\'\n'
	else:
		return f'{name}={value}\n'
bar=st.sidebar #图面编辑背景
class Cluster(object) :
	def __init__ (self, **kwargs) :
		self.name = kwargs['name']

	def set_title(self):
		st.title(self.name)
	
	def show_options(self):
		pass
	