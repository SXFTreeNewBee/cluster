# -*-coding:utf-8-*-
# -*-this is a python script -*-
import re

import subprocess

import time
import pandas as pd
import numpy as np
import os
import streamlit as st
from selenium import webdriver
from PIL import Image
from streamlit_autorefresh import st_autorefresh


class SideBar(object):

    def __init__(self,name):
        self.name=st.sidebar.title(name)

        server,socket,controller,topo,experiment,pingall,file_storage,role,mac=st.sidebar.tabs(["服务器","Socket","控制器","拓扑",
                                                                      "实验","初始化","文件","角色","MAC",])

        with server:
            st.subheader("服务器配置")

            self.MsgBarrier=st.text_input(label="消息分隔符(避免Socket乱序)",value="/")

            self.IP = st.selectbox('Server监听IP地址',('192.168.10.3', '127.0.0.1'))

            self.PORT=st.number_input("Server监听端口",value=8888)

            self.QUEUE_LEN = st.number_input("队列长度",value=500,step=100)

            self.CONTROLLER_NUM = st.number_input("控制器数量",value=5)

            self.WAIT_CONNECT = st.number_input("最大等待连接数",value=10,min_value=10) # 最大等待连接数

            self.WRINTE_PKTIN_LOAD_MONITOR = st.number_input("获取pktin负载的周期",value=5,min_value=2,max_value=10,step=1)  # 获取pktin负载的周期




if __name__ == '__main__':
    SideBar("集群基础信息配置")