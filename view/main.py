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
from cluster import Cluster

if __name__ == '__main__':
	cluster=Cluster(name = 'cluster')
	