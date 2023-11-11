# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
# 默认拓扑选项OS3E
import sys

sys.path.append('../..')
import streamlit as st
from utils.view import get_map

class OS3E(object) :
	def __init__ (self) :
		self.name = 'OS3E'
		self.CONTROLLERS = st.multiselect(label = "控制器节点(OS3E默认配置)",
		                                  options = ['c' + str(num) for num in range(0, 10)],
		                                  default = ['c0', 'c1', 'c2', 'c3', 'c4'],
		                                  key = "CONTROLLERS")
		self.CONTROLLER_PORTS = st.multiselect(label = "控制器监听端口(OS3E默认配置)",
		                                       options = [port for port in range(6650, 6659)],
		                                       default = [6653, 6654, 6655, 6656, 6657],
		                                       key = "CONTROLLER_PORT")  # 控制器端口
		self.EDGE_LINK = { ("s13", "s33") : [3, 2], ("s15", "s31") : [5, 2], ("s16", "s21") : [4, 2]
			, ("s22", "s31") : [2, 4], ("s23", "s32") : [2, 2], ("s24", "s51") : [3, 2],
			               ("s26", "s55") : [3, 2], ("s33", "s43") : [3, 2], ("s34", "s52") : [3, 2],
			               ("s54", "s40") : [3, 2] }  # 边缘交换机的连接端口，用于Server对全局拓扑的初始化
		self.SW_LINK = { ("s10", "s11") : [2, 2], ("s10", "s13") : [5, 2], ("s10", "s15") : [4, 2],
		                 ("s10", "s12") : [3, 2],
		                 ("s12", "s14") : [3, 2], ("s14", "s15") : [3, 3], ("s14", "s16") : [4, 2],
		                 ("s16", "s15") : [3, 4],
		                 ("s21", "s20") : [3, 2], ("s20", "s22") : [3, 3], ("s31", "s32") : [3, 3],
		                 ("s20", "s25") : [4, 2],
		                 ("s23", "s25") : [3, 3], ("s32", "s30") : [4, 3], ("s30", "s33") : [2, 4],
		                 ("s25", "s24") : [4, 2],
		                 ("s25", "s26") : [5, 2], ("s30", "s34") : [4, 2], ("s52", "s53") : [3, 2],
		                 ("s51", "s53") : [3, 3],
		                 ("s53", "s50") : [4, 2], ("s50", "s55") : [4, 3], ("s55", "s56") : [4, 2],
		                 ("s50", "s54") : [3, 2],
		                 ("s40", "s41") : [3, 2], ("s41", "s42") : [3, 2], ("s42", "s43") : [3, 3],
		                 ("s43", "s44") : [4, 2],
		                 ("s44", "s45") : [3, 2], ("s45", "s46") : [3, 2], ("s46", "s47") : [3, 2],
		                 ("s47", "s40") : [3, 4] }
		
		self.SW_HOST, self.SWS, self.HOSTS = get_map(LINKS=self.SW_LINK,CONTROLLERS=self.CONTROLLERS)
		
		self.ADJACENCY_CONTROLLER = {
			"c1" : ["c2", "c3"],
			"c3" : ["c1", "c2", "c4", "c5"],
			"c2" : ["c1", "c5", "c3"],
			"c4" : ["c3", "c5"],
			"c5" : ["c2", "c3", "c4"]
		}
		self.CONTROLLERS_EDGE_SWITCHES_AREA = {
			"c1" : { ("s13", 3) : 2, ("s15", 5) : 2, ("s16", 4) : 1 },
			"c2" : { ("s22", 2) : 2, ("s21", 2) : 0, ("s23", 2) : 2, ("s24", 3) : 4, ("s26", 3) : 4 },
			"c3" : { ("s31", 2) : 0, ("s31", 4) : 1, ("s32", 2) : 1, ("s33", 2) : 0, ("s33", 3) : 3, ("s34", 3) : 4 },
			"c4" : { ("s43", 2) : 2, ("s40", 2) : 4 },
			"c5" : { ("s51", 2) : 1, ("s52", 2) : 2, ("s54", 3) : 3, ("s55", 2) : 1 }
		}
		self.CONTROLLER_EDGE_SWITCHES = {
			"c1" : ["s13", "s15", "s16"],
			"c2" : ["s22", "s21", "s23", "s24", "s26"],
			"c3" : ["s31", "s32", "s33", "s34"],
			"c4" : ["s43", "s40"],
			"c5" : ["s51", "s52", "s54", "s55"]
		}

