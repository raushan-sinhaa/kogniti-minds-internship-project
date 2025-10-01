#            Task 2
#  Automation (Marketing + Communication)
#  Goal: Automate communication tasks.
#  Tasks:
#  1.Develop an Email Automation System:
#    Store ready-made templates (Welcome, Thank You mails)
#    Read email IDs from clean_customers.csv
#    Send bulk emails via SMTP
#    Maintain an email_log.txt file with details of sent mails
#  2.(Optional) WhatsApp Automation:
#     Use pywhatkit library to send fixed template messages to
#     customers.

from mailer import send_bulk_emails
from whatsapp_sender import send_whatsapp_messages

def main():
    print("📤 Choose communication channel:")
    print("1. Send Bulk Emails")
    print("2. Send WhatsApp Messages")
    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        print("📨 Choose email template:")
        print("1. Welcome")
        print("2. Thank You")
        email_choice = input("Enter choice (1/2): ").strip()

        template_map = {
            '1': 'templates/welcome.txt',
            '2': 'templates/thank_you.txt'
        }

        template_file = template_map.get(email_choice)
        if not template_file:
            print("❌ Invalid email template choice.")
            return

        send_bulk_emails(template_file)

    elif choice == '2':
        template = (
            "Hi {name},\n\n"
            "Thanks for connecting with us! We're excited to have you on board.\n\n"
            "— Team LeadManager"
        )
        send_whatsapp_messages(template)

    else:
        print("❌ Invalid channel choice.")

if __name__ == "__main__":
    main()
