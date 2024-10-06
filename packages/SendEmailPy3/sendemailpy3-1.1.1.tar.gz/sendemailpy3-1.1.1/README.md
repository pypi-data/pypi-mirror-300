# Email Sender Module
## Abstracted module for sending emails
### This module was made so that you don't have to worry about writing the code for sending emails yourself. This module can be used with multiple different email clients, and can be used to send multiple emails.

##### License must be followed while using this package.

## Documentation

### Parameters (required for all functions and methods)

Subject, content, receiver, username (sender's), password (sender's)

### Recommended import statement
```py
import sendemailpy3 as smpy
```

### Mail Commands
#### Gmail
```py
smpy.send_gmail(...)
```

#### Outlook
```py
smpy.send_outlook_email(...)
```

#### Yahoo Mail
```py
smpy.send_yahoo_email(...)
```

#### Proton Mail
```py
smpy.send_proton_email(...)
```

### Sending an email using procedural syntax
```py
import sendemailpy3 as smpy

smpy.send_gmail(...)
```

### Sending an email using object-oriented syntax
```py
import sendemailpy3 as smpy

email_sender = smpy.EmailSender()
email.send_gmail(...)
```