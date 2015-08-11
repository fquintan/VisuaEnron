# Programa que filtra los correos con al menos una respuesta
# y escribe su contenido en un archivo
from __future__ import print_function
import json

def print_to_err(*objs):
    print(*objs, file=sys.stderr)

json_filename = 'threads_dated_2.json'
json_file = open(json_filename)
json_str = json_file.read()
json_data = json.loads(json_str)

max_size = 20

output_filename = 'filtered_emails.txt'
out = open(output_filename, "w")

for thread in json_data:
	size = thread['size']
	if size < 2 or size > max_size:
		continue
		
	for mail in thread['mails']:
		text = mail['text']
		out.write(text)

out.close()