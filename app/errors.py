import os
from app import app
import traceback
from werkzeug.exceptions import InternalServerError
import sendgrid
from app.email import send_email

sg = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])

# https://sendgrid.com/blog/custom-error-report-emails-for-python-flask-web-apps-with-twilio-sendgrid/


@app.errorhandler(InternalServerError)
def handle_500(error):
    error_tb = traceback.format_exc()
    try:
        resp = send_email(
            subject="[wedding-website] An unexpected error has occurred.",
            from_email=app.config['ADMINS'][0],
            to_emails=app.config['ADMINS'][0],
            text_body = error_tb,
            html_body=None)
    except Exception as exc:
        print(exc)
    return app.finalize_request(error, from_error_handler=True)