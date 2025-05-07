import smtplib
from email.mime.text import MIMEText
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .app_passwords import EMAIL_APP_CODE




def send_email(receiver_email:str, data:str, subject:str) -> None:
    print(f"SENDING EMAIL TO: {receiver_email} \nMESSAGE BEING SENT: {data}")
    sender_email = "uodmessengerapp@gmail.com"
    password = EMAIL_APP_CODE
    msg = MIMEText(data, "plain")
    msg["Subject"] = subject

    host_name = "smtp.gmail.com"
    with smtplib.SMTP_SSL(host_name) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()


if __name__ == "__main__":
    
    #print(sys.path)
    send_email("100715281@unimail.derby.ac.uk", "Test", "this is a test")


    # SEDerby100715281