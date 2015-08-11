# Programa que obtiene el contenido de las 10 threads mas largas
# e imprime cada una en un archivo de texto separado para analizarlas
from __future__ import print_function
import json

def print_to_err(*objs):
    print(*objs, file=sys.stderr)

json_filename = 'threads_dated_2.json'
json_file = open(json_filename)
json_str = json_file.read()
json_data = json.loads(json_str)

max_size = 1000

output_basename = 'longest_thread_'
output_extension = '.txt'

for index in range(10):
	i = 0
	biggest_thread_index = 0
	biggest_thread_size = 0
	for thread in json_data:
		size = thread['size']
		if size > biggest_thread_size and size < max_size:
			biggest_thread_size = size
			biggest_thread_index = i
		i += 1

	max_size = biggest_thread_size
	print(str(max_size))
	biggest_thread = json_data[biggest_thread_index]

	out = open(output_basename + str(index) + output_extension, "w")

	out.write('Thread length: ' + str(biggest_thread_size) + '\n') 
	out.write('Thread subject: ' + biggest_thread['subject'] + '\n') 

	for mail in biggest_thread['mails']:
		text = mail['text']
		out.write(text)

	out.close()