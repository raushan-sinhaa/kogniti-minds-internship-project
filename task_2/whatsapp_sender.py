#  2.(Optional) WhatsApp Automation:
#    Use pywhatkit library to send fixed template messages to
#    customers


import pandas as pd
import pywhatkit as kit
import time

def send_whatsapp_messages(template_text, csv_file='clean_customers.csv'):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        phone = row.get('phone')  # Ensure 'phone' column exists with country code
        name = row.get('name', 'Customer')
        message = template_text.format(name=name)

        if pd.isna(phone) or not str(phone).startswith('+'):
            print(f"❌ Skipping invalid phone: {phone}")
            continue

        try:
            print(f"📲 Sending to {name} ({phone})...")
            kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
            time.sleep(15)  # Delay between messages
        except Exception as e:
            print(f"❌ Failed to send to {phone}: {e}")
