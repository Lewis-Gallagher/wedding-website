from app import app
import traceback
from werkzeug.exceptions import InternalServerError
import sendgrid
import os
sg = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])

# https://sendgrid.com/blog/custom-error-report-emails-for-python-flask-web-apps-with-twilio-sendgrid/
def create_message(email_text):
    return sendgrid.helpers.mail.Mail(
        from_email=app.config["ADMINS"][0],
        to_emails=app.config["ADMINS"],
        subject='[wedding-website] unhandled exception occurred!',
        plain_text_content=email_text,
    )

@app.errorhandler(InternalServerError)
def handle_500(error):
    error_tb = traceback.format_exc()
    try:
        resp = sg.send(create_message(error_tb))
    except Exception as exc:
        print(exc.message)
    return app.finalize_request(error, from_error_handler=True)