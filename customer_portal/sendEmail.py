
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self, sendFrom, sendTo, subject, text):
        self.sendFrom = sendFrom
        self.sendTo = sendTo
        self.subject = subject
        self.text = text

    
    def send(self):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.sendFrom
        msgRoot['To'] = self.sendTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'


        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        text = self.text
        msgText = MIMEText(text)
        msgAlternative.attach(msgText)

        connection = smtplib.SMTP(host='smtp-relay.corp.cableone.net', port=25)
        connection.starttls()
        connection.send_message(msgRoot)
        connection.quit()