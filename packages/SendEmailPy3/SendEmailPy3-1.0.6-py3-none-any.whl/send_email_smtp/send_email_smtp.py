import smtplib
from email.message import EmailMessage
import os

def send_gmail(subject, content, receiver):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)

	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	gmail = smtplib.SMTP("smtp.gmail.com", 587)
	gmail.ehlo()
	gmail.starttls()
	gmail.login(username, password)
	gmail.sendmail(username, receiver, email_message.as_string())
	gmail.quit()
	print("Send email function ended")
