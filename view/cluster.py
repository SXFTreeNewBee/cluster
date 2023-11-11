# -*-coding:utf-8-*-
import sys
sys.path.append('..')
from view.topo.default.OS3E import OS3E
from draw_graph import *


def template(name, value):

	if type(value)==str :
		return f'{name}=\'{value}\'\n'
	else:
		return f'{name}={value}\n'
	
bar=st.sidebar #图面编辑背景,侧面栏

custom_topo_dir='topo'

settings_path=''

config_path='../config.py'
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
		#MAC
		self.UNKNOWN_MAC='00:00:00:00:00:00'
		self.BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'
		#是否开启集群通信
		self.IF_ARP=None
		#控制器过载阈值
		self.CONTROLLER_PKT_THRESHOLD=None
		
		#开关
		
		#拓扑方法对象
		self.topo_object=None
		
		self.show_options()
		
		
	def set_title(self):
		st.title(self.name)
	
	def show_options(self):
		server,  controller, topo,other,run= bar.tabs(
			["Server", "控制器","拓扑","其他选项","生成网络"])

		self.server(server)
		self.controller(controller)
		self.topo(topo)
		self.other(other)
		self.run(run)
		
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
		
		def analyse_topo():
			st.write("按照OS3E拓扑形式，给出自定义拓扑的相关参数")
			st.write("拓扑地址：../view/dedfault")
			topo_file = st.file_uploader("自定义拓扑文件"
			                             , accept_multiple_files = False,
			                             )
			if topo_file:
				try:
					custom_topo_path = f'{custom_topo_dir}/custom/{topo_file.name}'
					with open(custom_topo_path,'wb') as f:
						
						f.write(topo_file.getvalue())
						
				except Exception as e:
					raise e
				topo_package_dir=custom_topo_path.strip('.py').split('/')

				package = __import__('.'.join(topo_package_dir), fromlist = [topo_package_dir[-1]])
				
				topo_class=getattr(package, topo_package_dir[-1])
				
				return topo_class()
		with topo:
			st.subheader("拓扑配置选项(不显示主机)")
			self.TOPO = st.selectbox('拓扑样式', ("OS3E","自定义拓扑"))
			if self.TOPO=="OS3E":
				self.topo_object=OS3E()
			
			else:
				self.topo_object=analyse_topo()
			
				
			
			
	def other(self,other):
		
		with other:
			st.subheader("其他配置选项")
			self.IF_ARP=self.TOPO = st.selectbox('是否开启通信', (1,0))
			
			self.CONTROLLER_PKT_THRESHOLD=st.number_input("控制器阈值",value=1600)
	
	def run(self,run):
		with run:
			st.subheader("先保存再生成")
			if self.topo_object:

				button_state={
					'save_button':False,
					'network_button':True
				}

				if 'button_state' not in st.session_state:
					st.session_state.button_state=button_state

				save_button=st.button(label="保存配置", on_click=self.save_config, kwargs=self.__dict__,
						  key='save_button', use_container_width=True,disabled=st.session_state.button_state.get('save_button'))

				if save_button:

					st.session_state.button_state['network_button']=False

				network_button=st.button(label="生成网络", on_click=generate_network, kwargs=self.topo_object.__dict__,
						  key='network_button', use_container_width=True,
						  disabled=st.session_state.button_state.get('network_button'))






	def save_config(self,**kwargs):

		with open(config_path,'w+') as f :
			for k,v in kwargs.items():
				if k=="topo_object":
					continue
				f.write(template(name=k,value=v))

		show_notify()


