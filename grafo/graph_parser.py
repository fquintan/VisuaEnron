#!/usr/bin/python
import operator
import sys
min_value = int(sys.argv[1])
nombre_json = ('grafo_ordenado_contado.json')
archivo = open('grafo_ordenado.txt', 'r')
out = open(nombre_json, 'w')

def get_group(email):
	if email.endswith("enron.com"):
		return 1
	else: 
		return 2
# count = 0
# name_id = {}
# for line in archivo:
# 	nombres = line.split()
# 	if(not nombres[0] in name_id):
# 		name_id[nombres[0]] = count
# 		count += 1
# 	if(not nombres[1] in name_id):
# 		name_id[nombres[1]] = count
# 		count += 1


# archivo.close()
# sorted_names = sorted(name_id.items(), key=operator.itemgetter(1))

# out.write('{\n"nodes":[\n')
# for (name, n) in sorted_names:
# 	w = '{"name":"' + name + '","group":1},\n'
# 	out.write(w)

# out.write('],\n')	

# archivo = open('grafo_ordenado.txt', 'r')

count = 1
# out.write('"links":[\n')
last_line = archivo.readline()
conections = {}
for line in archivo:
	if (line == last_line):
		count += 1
	else:
		nombres = last_line.split()
		# w = '{"source":' + str(name_id[nombres[0]]) + ',"target":' + str(name_id[nombres[1]]) + ',"value":' + str(count) + '},\n'
		# out.write(w)
		n0 = ''
		n1 = ''
		if (nombres[0] > nombres[1]):
			n1 = nombres[0]
			n0 = nombres[1]
		else:
			n0 = nombres[0]
			n1 = nombres[1]
		if ((n0, n1) in conections):
			conections[(n0, n1)] += count
		else:
			conections[(n0, n1)] = count
		last_line = line
		count = 1

# out.write(']\n}')

sorted_conections = sorted(conections.items(), key=operator.itemgetter(1), reverse=True)
name_id = {}


count = 0
out.write('var graph = {"links":[\n')
for ((n1, n2), v) in sorted_conections:
	if(v < min_value):
		break
	if(not n1 in name_id):
		name_id[n1] = count
		count += 1
	if(not n2 in name_id):
		name_id[n2] = count
		count += 1
	w = '{"source":' + str(name_id[n1]) + ',"target":' + str(name_id[n2]) + ',"value":' + str(v) + '},\n'
	out.write(w)
out.write('],\n')

sorted_names = sorted(name_id.items(), key=operator.itemgetter(1))

out.write('"nodes":[\n')
for (name, n) in sorted_names:
	w = '{"name":"' + name + '","group":' + str(get_group(name)) + '},\n'
	out.write(w)

out.write(']\n}')	

