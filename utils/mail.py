import smtplib

def send_mail(subject:str, message:str, recipient:str):
    '''send mail to recipient with given data'''
    print("Sending")
    server = smtplib.SMTP('localhost', 1025)
    server.sendmail(subject, recipient, message)
    server.quit()
