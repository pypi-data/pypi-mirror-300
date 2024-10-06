import smtplib
from email.message import EmailMessage
import os

class EmailSender():
	def __init__(self, subject, content, receiver, username, password):
		self.subject = subject
		self.content = content
		self.receiver = receiver
		self.username = username
		self.password = password
	
	def send_gmail(self):
		send_gmail(self.subject, self.content, self.receiver, self.username, self.password)
	
	def send_outlook_email(self):
		send_outlook_email(self.subject, self.content, self.receiver, self.username, self.password)
	
	def send_yahoo_email(self):
		send_yahoo_email(self.subject, self.content, self.receiver, self.username, self.password)
	
	def send_proton_mail(self):
		send_proton_email(self.subject, self.content, self.receiver, self.username, self.password)

def send_gmail(subject, content, receiver, username, password):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)

	gmail = smtplib.SMTP("smtp.gmail.com", 587)
	gmail.ehlo()
	gmail.starttls()
	gmail.login(username, password)
	gmail.sendmail(username, receiver, email_message.as_string())
	gmail.quit()
	print("Send email function ended")

def send_outlook_email(subject, content, receiver, username, password):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
	
	outlook = smtplib.SMTP("smtp-mail.outlook.com", 587)
	outlook.ehlo()
	outlook.starttls()
	outlook.login(username, password)
	outlook.sendmail(username, receiver, email_message.as_string())
	outlook.quit()
	print("Send email function ended")

def send_yahoo_email(subject, content, receiver, username, password):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
    
	yahoo = smtplib.SMTP("smtp.mail.yahoo.com", 465)
	yahoo.ehlo()
	yahoo.starttls()
	yahoo.login(username, password)
	yahoo.sendmail(username, receiver, email_message.as_string())
	yahoo.quit()
	print("Send email function ended")

def send_proton_email(subject, content, receiver, username, password):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
    
	proton = smtplib.SMTP("smtp.protonmail.ch", 587)
	proton.ehlo()
	proton.starttls()
	proton.login(username, password)
	proton.sendmail(username, receiver, email_message.as_string())
	proton.quit()
	print("Send email function ended")
