import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def code_gen():

    return int(time.time()) % 10000

def send_mail(_to):
    fromaddr = 'bitcapinc@gmail.com'
    toaddr = str(_to)

    #generating a random number
    code = code_gen()

    #credentials
    username = 'bitcapinc@gmail.com'
    password = 'pactibcni'

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Manipal Univerity Jaipur No Dues"

    mail_content = "Your code: " + str(code)

    body = str(mail_content)
    msg.attach(MIMEText(body, 'plain'))

    #connecting to the server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return code