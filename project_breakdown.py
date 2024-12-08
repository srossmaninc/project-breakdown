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

dir_to_search = "/Users/sethrossman/Desktop/UNH Y4/GUPPS/gupps-control"

files_to_omit = [".DS_Store", ".gitignore"]
dir_to_omit = [".git", "__pycache__", ".vscode"]

def omitted(path, to_omit):
	for omit in to_omit:
		if path.find(omit) != -1: # directory not in omit list
			return True
	return False

def search_code():
	all_files = {}
	for dirpath, dirnames, filenames in os.walk(dir_to_search, topdown=True):
		# for f in filenames:
		# 	# list containing all connected nodes
		# 	all_files[f"{dirpath}/{f}"] = {
		# 		'num_of_instances': 0,
		# 		'connections': []
		# 	}
		if not omitted(dirpath, dir_to_omit):
			for f in filenames:
				# list containing all connected nodes (minus files_to_omit)
				if not omitted(f, files_to_omit):
					all_files[f"{dirpath}/{f}"] = {
						'num_of_instances': 0,
						'connections': []
					}
			# print(f"{dirpath}/{f}")

	# for entry in all_files:
	# 	print(type(entry))
	# 	pass

	for key in all_files.keys():
		# print(type(key))
		with open(key, 'r') as ff:
			try:
				file_read = ff.read()
				# if a file 'k' is referenced in another file, add to that files connections
				for k in all_files.keys():
					search_k = k.split("/")[-1]
					search_k_search = search_k.split(".")
					# print(f"search_k: {search_k}, search_k_search: {search_k_search}")
					# print(search_k_search)

					if len(search_k_search) == 1:
						if file_read.find(search_k_search[-1]) != -1:
							all_files[key]['num_of_instances'] += 1
							all_files[key]['connections'].append(k)
					else:
						# print(search_k_search[-2])
						if file_read.find(search_k_search[-2]) != -1:
							all_files[key]['num_of_instances'] += 1
							all_files[key]['connections'].append(k)
			except Exception as e:
				# trying to read an unreadable file
				print(f"Error ({e}): {key}")
				# print("---")
				pass

	return all_files

def print_res(connections_dict):
	for dirpath, dirnames, filenames in os.walk(dir_to_search, topdown=True):
		level = len(dirpath.split("/"))
		indentation = "".join([' ' for i in range(level)])

		aa = dirpath.split("/")[-1]

		# NOTE: possibly change so ONLY the root omitted folder is displayed
		if not omitted(dirpath, dir_to_omit):
			print(f"{indentation}{colors['root_f']}/{aa}{colors['white']}")

			for folder in dirnames:
				print(f"{indentation}{colors['folder']}  {folder}{colors['white']}")

			for f in filenames:
				if not omitted(f, files_to_omit):
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
					if (connected_instances['num_of_instances'] != 0):
						print(f"{colors['connection']} ({connected_instances['num_of_instances']}){colors['white']}")
						for connect in connected_instances['connections']:
							print(f"{indentation}  | {colors['connection']}{connect}{colors['white']}")
					else:
						print()

def main():
	connections_dict = search_code()
	print_res(connections_dict)

if __name__ == '__main__':
	main()