from __future__ import print_function
from email_util import EmailWalker
import sys
import string
import datetime
STOPWORDS = set(['thanks', 'forwarded', 'would', 'please', 'subject', 'want', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

def print_to_err(*objs):
    print(*objs, file=sys.stderr)

def load_enron_emails(folder=''):
	# clear_subspace(db, ER_space)
	# reader = EmailWalker(localdir+folder)
	reader = EmailWalker(folder)
	count_mails = 0	
	punctuation_map = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	max = 10000
	hist = {}
	for email in reader:
		text = email['subject'].strip().lower().translate(punctuation_map)
		#print text
		words = [x.strip() for x in text.split() if x.strip() != ""]
		for word in [x for x in words if x not in STOPWORDS and not x.isdigit() and len(x)>3]:
			if word in hist:
				hist[word] += 1
			else:
				hist[word] = 1
		count_mails +=1
		if (count_mails % 1000) == 0:
			print ("[%s] %s" % (datetime.datetime.utcnow(),count_mails))
		#if count_mails > max:
		#	break
	print ("[%s] Finished processing mails, started writing" % datetime.datetime.utcnow())
	
	import operator
	sorted_dict = sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
	
	out = open("wordcount_subject.json", "w")
	out.write("data=[")
	for (k, v) in sorted_dict[0:200]:
		out.write("{\"text\":\"%s\", \"size\":%s},\n" % (k, v))
	out.write("];")
	out.close()

load_enron_emails('../enron_mail_20110402 (1)/enron_mail_20110402/maildir')

