import smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders


class EmailSender():
	def __init__(self, subject, content, receiver, username, password, filepath=None):
		self.subject = subject
		self.content = content
		self.receiver = receiver
		self.username = username
		self.password = password
		self.filepath = filepath
	
	def send_gmail(self):
		send_gmail(self.subject, self.content, self.receiver, self.username, self.password, self.filepath)
	
	def send_outlook_email(self):
		send_outlook_email(self.subject, self.content, self.receiver, self.username, self.password, self.filepath)
	
	def send_yahoo_email(self):
		send_yahoo_email(self.subject, self.content, self.receiver, self.username, self.password, self.filepath)
	
	def send_proton_mail(self):
		send_proton_email(self.subject, self.content, self.receiver, self.username, self.password, self.filepath)


def send_gmail(subject, content, receiver, username, password, filepath=None):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
	if filepath is not None:
		try:
			with open(filepath, 'rb') as file:
				mime_base = MIMEBase('application', 'octet-stream')
				mime_base.set_payload(file.read())
				
			encoders.encode_base64(mime_base)
			
			mime_base.add_header('Content-Disposition', f'attachment; filename={filepath.split("/")[-1]}')
			
			email_message.add_attachment(mime_base.get_payload(decode=True), maintype='application', subtype='octet-stream', filename=filepath.split("/")[-1])

		except Exception as e:
			print(f"Failed to attach the file: {e}")

	gmail = smtplib.SMTP("smtp.gmail.com", 587)
	gmail.ehlo()
	gmail.starttls()
	gmail.login(username, password)
	gmail.sendmail(username, receiver, email_message.as_string())
	gmail.quit()
	print("Send email function ended")


def send_outlook_email(subject, content, receiver, username, password, filepath=None):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
	if filepath is not None:
		try:
			with open(filepath, 'rb') as file:
				mime_base = MIMEBase('application', 'octet-stream')
				mime_base.set_payload(file.read())
				
			encoders.encode_base64(mime_base)
			
			mime_base.add_header('Content-Disposition', f'attachment; filename={filepath.split("/")[-1]}')
			
			email_message.add_attachment(mime_base.get_payload(decode=True), maintype='application', subtype='octet-stream', filename=filepath.split("/")[-1])

		except Exception as e:
			print(f"Failed to attach the file: {e}")
	
	outlook = smtplib.SMTP("smtp-mail.outlook.com", 587)
	outlook.ehlo()
	outlook.starttls()
	outlook.login(username, password)
	outlook.sendmail(username, receiver, email_message.as_string())
	outlook.quit()
	print("Send email function ended")


def send_yahoo_email(subject, content, receiver, username, password, filepath=None):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
	if filepath is not None:
		try:
			with open(filepath, 'rb') as file:
				mime_base = MIMEBase('application', 'octet-stream')
				mime_base.set_payload(file.read())
				
			encoders.encode_base64(mime_base)
			
			mime_base.add_header('Content-Disposition', f'attachment; filename={filepath.split("/")[-1]}')
			
			email_message.add_attachment(mime_base.get_payload(decode=True), maintype='application', subtype='octet-stream', filename=filepath.split("/")[-1])

		except Exception as e:
			print(f"Failed to attach the file: {e}")
    
	yahoo = smtplib.SMTP("smtp.mail.yahoo.com", 465)
	yahoo.ehlo()
	yahoo.starttls()
	yahoo.login(username, password)
	yahoo.sendmail(username, receiver, email_message.as_string())
	yahoo.quit()
	print("Send email function ended")


def send_proton_email(subject, content, receiver, username, password, filepath=None):
	print("Send email function started")
	email_message = EmailMessage()
	email_message["Subject"] = subject
	email_message.set_content(content)
	if filepath is not None:
		try:
			with open(filepath, 'rb') as file:
				mime_base = MIMEBase('application', 'octet-stream')
				mime_base.set_payload(file.read())
				
			encoders.encode_base64(mime_base)
			
			mime_base.add_header('Content-Disposition', f'attachment; filename={filepath.split("/")[-1]}')
			
			email_message.add_attachment(mime_base.get_payload(decode=True), maintype='application', subtype='octet-stream', filename=filepath.split("/")[-1])

		except Exception as e:
			print(f"Failed to attach the file: {e}")
    
	proton = smtplib.SMTP("smtp.protonmail.ch", 587)
	proton.ehlo()
	proton.starttls()
	proton.login(username, password)
	proton.sendmail(username, receiver, email_message.as_string())
	proton.quit()
	print("Send email function ended")
