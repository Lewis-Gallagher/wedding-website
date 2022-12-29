# wedding-website
A Python Flask app for our wedding

## Pages
1. Home/Landing Page
2. RSVP Form
3. FAQ
4. Event Info
5. The Story So Far
6. Contact Us

## Home Page
Shows the digital invite card. All pages include a navigation bar with links to other areas of the site.

## RSVP Form
A form with numerous fields:
* Attending: yes/no
* Name (must be unique)
* Email address (must be unique and be an invited email address)
* Phone number
* Dietary requirements (if any)
* An optional message

## SQLAlchemy Database
The app uses an SQLAlchemy SQLite database as it is lightweight and traffic is expected to be very low, so there is no need to host a MySQL or PostgreSQL server.

### Structure
The database contains two tables: Invited and Guest. The Invited table contains the email addresses of all invitees and a unique ID which is a foreign key to the Guest table. The Guest table contains attendee information such as name, contact information, dietary requirements etc plus a unique ID. 

### Considerations
The flask forms are set up so an RSVP may only be submitted with an email address that exists in the Invited table. This is to ensure no uninvited guests may RSVP and also prevents me from having guests register with an email address and password. This is not the most secure option as one may easily RSVP with someone else's email address, however, I felt a user registration system would be quite unnecessary for an otherwise static and non-interactive website.

Database backups are important to not erroneously lose attendee information. This is achieved manually every time the database is manually accessed by running the `sq3backup.sh` script: 
```bash
. sq3backup.sh
``` 
This creates a backup file of the database, labelled with the date and time, within the `./bak` directory.

The database can be restored with:
 ```bash
 dbfile=bak/20221228-143151.app.db.sq3
 sqlite3 app.db ".restore $dbfile"
 ```

 Finally, the database can be exported to csv format with:
 ```bash
 sqlite3 -header -csv app.db "SELECT * from Guest;" > guests.csv
 ```
