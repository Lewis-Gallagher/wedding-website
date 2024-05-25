from contextlib import closing
from dotenv import load_dotenv
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email
import sqlite3 as db

# Load environmental variables from file.
load_dotenv(os.path.join('.env'))

# Pull list of emails from the database.
with closing(db.connect('db/app.db')) as conn:
    # sq3 returns a tuple with an empty second value by default. Return only first value.
    conn.row_factory = lambda cursor, row: row[0]
    with closing(conn.cursor()) as cursor:
        to_emails = cursor.execute('SELECT email FROM Guest WHERE attending == 1').fetchall()

for i in to_emails:
    print(i)

# Get plain text content for email from file.
with open('text.txt', 'r') as fh:
    plain_content = fh.read()

# Get html content for email from file.
with open('text.html') as fh:
    html_content = fh.read()

# Construct mail.
from_email = Email("lewis@nplgwedding.com", 'Lewis and Niki')  # Change to your verified sender.
subject = "Getting ready for our Wedding in Kos!"

mail = Mail(from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=html_content,
            plain_text_content=plain_content,
            is_multiple=True)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

try:
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
