from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Bcc, Email
from app import app

def send_email(subject='NP LG Wedding', from_email=app.config['ADMINS'][0], to_emails=None, text_body=None, html_body=None):
    """
    Creates an email to send via SendGrid Mail API.
    All emails will be sent to admins so the to_emails variable needs to be extended.
    """

    to_emails = [to_emails]
    # to_emails.extend(app.config['ADMINS'])

    msg = Mail(from_email = from_email,
               to_emails = to_emails,
               subject = subject,
               plain_text_content = text_body,
               html_content = html_body
               )
    
    personalisation = Personalization()
    personalisation.add_to(Email(to_emails))
    personalisation.add_bcc(Bcc(app.config['ADMINS']))

    msg.add_personalization(personalisation)        

    sg = SendGridAPIClient(api_key=app.config['SENDGRID_API_KEY'])
    response = sg.send(msg)
    app.logger.info(f'Attempting to connect SendGridAPIClient - {response.status_code} - {response.body} - {response.headers}')
