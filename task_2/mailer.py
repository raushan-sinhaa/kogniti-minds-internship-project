#  1.Develop an Email Automation System:
#     Store ready-made templates (Welcome, Thank You mails)
#     Read email IDs from clean_customers.csv
#     Send bulk emails via SMTP
#     Maintain an email_log.txt file with details of sent mails

import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

def load_template(template_path):
    with open(template_path, 'r') as f:
        return f.read()

def send_bulk_emails(template_file, csv_file='clean_customers.csv', log_file='email_log.txt'):
    template = load_template(template_file)
    df = pd.read_csv(csv_file)

    # SMTP setup
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_app_password'  # Use app password for Gmail

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create log file with header if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write("Timestamp\tRecipient\tStatus\tError\tTemplate\n")

    with open(log_file, 'a') as log:
        for _, row in df.iterrows():
            name = row.get('name', 'Customer')
            recipient = row['email']
            content = template.format(name=name)

            msg = EmailMessage()
            msg.set_content(content.split('\n\n', 1)[-1])
            msg['Subject'] = content.split('\n')[0].replace('Subject: ', '')
            msg['From'] = sender_email
            msg['To'] = recipient

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                server.send_message(msg)
                log.write(f"{timestamp}\t{recipient}\tSENT\t-\t{template_file}\n")
                print(f"✅ Sent to {recipient}")
            except Exception as e:
                log.write(f"{timestamp}\t{recipient}\tFAILED\t{e}\t{template_file}\n")
                print(f"❌ Failed to send to {recipient}: {e}")

    server.quit()

