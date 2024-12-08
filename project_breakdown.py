# project overview utility...

import os

# first, take the specificed directory and walk down it.
# each 'level' is indented more and more

"""
color coding:
  folder -> white
  python file -> light green
  arduino file -> blue
  header file -> dark blue
  connection -> red preceded by (1:x) in parentheses
"""

colors = {
	'python': '\033[0;32m',
	'arduino': '\033[0;34m', # or C++ (might switch to light blue for C++)
	'header_f': '\033[0;34m',
	'connection': '\033[1;31m',
	'white': '\033[0;37m',
	'png': '\033[0;36m',
	'root_f': '\033[1;35m',
	'folder': '\033[0;35m'
}

dir_to_search = "/Users/sethrossman/Desktop/UNH Y4/ASV/mantaray-ground-control/"

def search_code():
	all_files = {}
	for dirpath, dirnames, filenames in os.walk(dir_to_search, topdown=True):
		for f in filenames:
			# list containing all connected nodes
			all_files[f"{dirpath}/{f}"] = 0
			# print(f"{dirpath}/{f}")

	for key in all_files.keys():
		# print(key)
		with open(key, 'r') as ff:
			try:
				file_read = ff.read()
				# print(file_read)
				for k in all_files.keys():
					# print(k)
					search_k = k.split("/")[-1]
					# print(search_k)
					search_k_search = search_k.split(".")
					if len(search_k_search) == 1:
						if file_read.find(search_k_search) != -1:
							all_files[key] += 1
					else:
						if file_read.find(search_k_search[-2]) != -1:
							all_files[key] += 1
			except:
				# trying to read an unreadable file
				# print("---")
				pass

	return all_files

def print_res(connections_dict):
	for dirpath, dirnames, filenames in os.walk(dir_to_search, topdown=True):
		level = len(dirpath.split("/"))
		indentation = "".join([' ' for i in range(level)])

		aa = dirpath.split("/")[-1]
		print(f"{indentation}{colors['root_f']}/{aa}{colors['white']}")
		for folder in dirnames:
			print(f"{indentation}{colors['folder']}  {folder}{colors['white']}")
		# print(filenames)
		for f in filenames:
			f_split = f.split(".")
			if (len(f_split) == 2):
				if f_split[1] == "py":
					print(f"{indentation}  {colors['python']}{f}{colors['white']}", end='')
				elif f_split[1] == "ino":
					print(f"{indentation}  {colors['arduino']}{f}{colors['white']}", end='')
				elif f_split[1] == "png":
					print(f"{indentation}  {colors['png']}{f}{colors['white']}", end='')
				else:
					print(f"{indentation}  {f}", end='')
			else:
				print(f"{indentation}  {f}", end='')
			connected_instances = connections_dict[f"{dirpath}/{f}"]
			if (connected_instances != 0):
				print(f"{colors['connection']} ({connected_instances}){colors['white']}")
			else:
				print()

def main():
	connections_dict = search_code()
	print_res(connections_dict)

if __name__ == '__main__':
	main()