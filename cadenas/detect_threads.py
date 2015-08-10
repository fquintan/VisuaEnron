from __future__ import print_function
from email_util import EmailWalker
import sys
import string
import datetime
STOPWORDS = set(['thanks', 'forwarded', 'would', 'please', 'subject', 'want', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

def print_to_err(*objs):
    print(*objs, file=sys.stderr)
	
def jsonify(emails):
	json = '['
	punctuation_map = string.maketrans(string.punctuation+'\n\r\t', ' '*(len(string.punctuation)+3))
	for email in emails:
		json += '{'
		json += '\"text\":\"' + email['text'].translate(punctuation_map).strip() + '\",'
		json += '\"date\":\"' + str(email['date']) + '\"'
		if(email == emails[-1]):
			json += '}\n'
		else:
			json += '},\n'
			
	return json + ']'
	
def load_enron_emails(folder=''):
	# clear_subspace(db, ER_space)
	# reader = EmailWalker(localdir+folder)
	reader = EmailWalker(folder)
	count_mails = 0	
	punctuation_map = string.maketrans(string.punctuation+'\n\r\t', ' '*(len(string.punctuation)+3))
	res_strings = ['re:', 'fw:', 'fwd:']
	threads = {}
	for email in reader:
		subject = email['subject'].lower()
		for s in res_strings:
			subject = subject.replace(s, '')
		subject = subject.translate(punctuation_map).strip()
		if subject == '':
			continue
		if subject in threads:
			threads[subject].append(email)
		else:
			threads[subject] = [email]
		if (count_mails % 1000) == 0:
			print ("[%s] %s" % (datetime.datetime.utcnow(),count_mails))

		count_mails +=1
	print ("[%s] Finished processing mails, started writing" % datetime.datetime.utcnow())
	
	#import operator
	#sorted_dict = sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
	
	out = open("threads_dated_2.json", "w")
	out.write("[")
	for (k, v) in threads.iteritems():
		out.write("{\"subject\":\"%s\", \"mails\":%s, \"size\":%s},\n" % (k, jsonify(v), len(v)))
	out.write("]")
	out.close()

load_enron_emails('../enron_mail_20110402/maildir')

