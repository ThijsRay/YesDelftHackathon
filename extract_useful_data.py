import os
from mail import Mail
import email

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

mailList = list()

for subdir, dirs, files in os.walk("maildir"):
    for file in files:
        filepath = subdir + os.sep + file

        with open(filepath, encoding = "ISO-8859-1") as f:
            msg = EmailMessage()
            msg.set_content(f.read())

        mailList.append()

for mail in mailList:
    mail.print_mail()
