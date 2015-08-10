from __future__ import print_function
from email_util import EmailWalker
import sys

def print_to_err(*objs):
    print(*objs, file=sys.stderr)

def load_enron_emails(folder=''):
	# clear_subspace(db, ER_space)
	# reader = EmailWalker(localdir+folder)
	reader = EmailWalker(folder)
	count_mails = 0

	max = 50000
	message_ids = {}
	for email in reader:
	# add_email(db, email)
		for recipient in email['to']:
			print(email['sender'] + '\t' + recipient)
			
		message_ids[email['mid']] = 1
		count_mails += 1
		if(count_mails % 10000 == 0):
			print_to_err("Processed", count_mails, "mails")
		# if(count_mails > max):
		# 	break


	print_to_err("Processed", count_mails, "mails")
	print_to_err("Distinct mids:", len(message_ids.keys()))

load_enron_emails('../enron_mail_20110402/maildir')

