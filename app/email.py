import os
from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import app
from config import Config

def send_email(subject='NP LG Wedding', from_email=app.config['ADMINS'][0], to_emails=None, text_body=None, html_body=None):
    """
    Creates an email to send via SendGrid Mail API.
    All emails will be sent to an admin so the to_emails variable needs to be extended.
    """

    admins = app.config['ADMINS']
    to_emails = [to_emails]
    to_emails.extend(admins)

    msg = Mail(from_email = from_email,
               to_emails = to_emails,
               subject = subject,
               plain_text_content = text_body,
               html_content = html_body
               )

    sg = SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
    response = sg.send(msg)
    print(response.status_code)
    print(response.body)
    print(response.headers)