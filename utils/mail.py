import smtplib

def send_mail(subject:str, message:str, recipient:str):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("email", "password")
    server.sendmail("email", recipient, message)
    server.quit()
