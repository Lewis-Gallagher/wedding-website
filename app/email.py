import os
from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(subject, from_email, to_emails, text_body, html_body):
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

def send_email_rsvp(guest):
    subject = 'Wedding RSVP - Thank you for your RSVP!'
    sender = os.environ['MAIL_DEFAULT_SENDER']
    recipients = guest.email
    text_body = render_template('email/rsvp_response.txt', guest = guest)
    html_body = render_template('email/rsvp_response.html', guest = guest)

    send_email(subject = subject,
            from_email = sender,
            to_emails = recipients,
            text_body = text_body,
            html_body = html_body)
