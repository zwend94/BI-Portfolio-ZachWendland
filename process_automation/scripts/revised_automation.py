import imaplib
import email
from email.header import decode_header
import pandas as pd
import os

#Params
SERVER = "outlook.office365.com" 
EMAIL_ACCOUNT = "trigger-automation@zillow.com"
PASSWORD = "pwd"
PROCESS_FOLDER = "C:/PATH/TO/PROCESS_FOLDER/"
SCRIPT_FOLDER = "C:/PATH/TO/SCRIPT_FOLDER/" 

#Connect to the server
def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    return mail

#Get unread emails
def fetch_unread_emails(mail):
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    return email_ids

#Process email
def process_email(mail, email_id):
    res, msg = mail.fetch(email_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            from_ = msg.get("From")
            print(f"Processing email from: {from_}, Subject: {subject}")

            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = part.get("Content-Disposition")
                    if content_disposition and "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join(PROCESS_FOLDER, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Saved attachment: {filename}")
                            process_excel(filepath)
    mail.store(email_id, "+FLAGS", "\\Seen") 

#Process XLSX file
def process_excel(filepath):
    try:
        data = pd.ExcelFile(filepath)
        df = data.parse(data.sheet_names[0]) 
        print(f"Processing file: {filepath}")
        os.rename(filepath, os.path.join(SCRIPT_FOLDER, os.path.basename(filepath)))
    except Exception as e:
        print(f"Error processing Excel file: {e}")

#Main function
def main():
    try:
        mail = connect_to_email()
        email_ids = fetch_unread_emails(mail)
        for email_id in email_ids:
            process_email(mail, email_id)
        mail.logout()
    except Exception as e:
        print(f"Error in email processing: {e}")

if __name__ == "__main__":
    main()

