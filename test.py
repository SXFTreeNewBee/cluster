# -*-coding:utf-8-*-
s='view/topo/custom/OS3E.py'

path_dir=s.strip('.py').split('/')

package=__import__('.'.join(path_dir),fromlist = [path_dir[-1]])
print(getattr(package,path_dir[-1])().__dict__)
