# -*-coding:utf-8-*-
def template(name, value):

	if type(value)==str :
		return f'{name}=\'{value}\'\n'
	else:
		return f'{name}={value}\n'
	
def save_config(config_path,**kwargs):
	with open(config_path, 'w+') as f :
		for k, v in kwargs.items() :
			if k == "topo_object" :
				continue
			f.write(template(name = k, value = v))
