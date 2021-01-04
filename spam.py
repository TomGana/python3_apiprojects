import smtplib

gmail_user = ''
gmail_password = ''

sent_from = gmail_user
to = ['']
subject = 'Super Important Message'
body = ''

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
i=0
while i<200:
    server.sendmail(sent_from, to, email_text)
    i+= 1
    print('emailed  '+ str(i))
server.close()
