#!/usr/bin/env python3
"""
Kogniti Minds CRM Lite - Integrated CLI Application
Task 4: Final Project Integration

Combines functionality from:
- Task 1: Lead Management & Data Cleaning
- Task 2: Communication & Email Automation
- Task 3: Sales Analysis & Reporting

Features:
a. Add new lead (name, email, phone, source)
b. List existing leads
c. Record sales data
d. Generate weekly reports (Excel + Graphs + PDF)
e. Send bulk emails to stored customers
"""

# Kogniti Minds CRM Lite - Unified CLI Main File

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage
import pywhatkit as kit
from datetime import datetime
from fpdf import FPDF
import time
import os
import re

DB_NAME = 'crm_lite.db'

# -------- clean_leads.py integration --------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))

def import_clean_leads():
    filename = input("CSV filename (default company_leads.csv): ").strip() or "company_leads.csv"
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found")
        return
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip().str.lower()
    if "email" not in df.columns or "name" not in df.columns:
        print("Missing required columns")
        return
    df['valid_email'] = df['email'].apply(is_valid_email)
    df = df[df['valid_email']].drop_duplicates(subset='email')
    conn = sqlite3.connect(DB_NAME)
    imported, skipped = 0, 0
    for _, row in df.iterrows():
        try:
            conn.execute('INSERT INTO leads (name, email, phone, source) VALUES (?, ?, ?, ?)', (
                row['name'], row['email'].lower(), str(row.get('phone')), row.get('source', 'CSV')))
            imported += 1
        except sqlite3.IntegrityError:
            skipped += 1
    conn.commit()
    conn.close()
    print(f"Imported: {imported}, Duplicates skipped: {skipped}")

# -------- mailer.py integration --------
def load_template(template_file):
    with open(template_file, 'r') as f:
        return f.read()

def send_bulk_emails():
    conn = sqlite3.connect(DB_NAME)
    leads = conn.execute('SELECT name, email FROM leads').fetchall()
    conn.close()
    sender = input("Sender email: ")
    password = input("App password: ")
    print("Template: 1=welcome.txt, 2=thank_you.txt")
    choice = input("Select: ")
    template_file = "welcome.txt" if choice=="1" else "thank_you.txt"
    if not os.path.exists(template_file):
        print("Template missing")
        return
    template = load_template(template_file)
    subject = input("Email subject: ")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        for name, email in leads:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = email
            msg.set_content(template.replace("{name}", name))
            server.send_message(msg)
            print(f"Sent: {name} ({email})")
        server.quit()
    except Exception as e:
        print("Email error:", e)

# -------- whatsapp_sender.py integration --------
def send_whatsapp_messages():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query('SELECT name, phone FROM leads', conn)
    conn.close()
    template_file = "welcome.txt"
    if not os.path.exists(template_file): print("Template missing"); return
    template = load_template(template_file)
    for _, row in df.iterrows():
        phone = str(row['phone'])
        name = row['name']
        if not phone or not phone.startswith('+'):
            print(f"Skipping phone: {phone}")
            continue
        try:
            print(f"Sending WhatsApp to {name} ({phone})...")
            kit.sendwhatmsg_instantly(phone_no=phone, message=template.format(name=name), wait_time=10, tab_close=True)
            time.sleep(15)
        except Exception as e:
            print(f"WhatsApp fail for {phone}: {e}")

# -------- Sales + Analytics + Reporting (sales_analyzer.py, visualizer.py, exporter.py) --------
def record_sales_data():
    list_leads()
    lead_id = input("Lead ID: ").strip()
    amount = input("Sale Amount: ").strip()
    try:
        conn = sqlite3.connect(DB_NAME)
        name = conn.execute('SELECT name FROM leads WHERE id=?', (lead_id,)).fetchone()
        if not name:
            print("Invalid Lead ID")
            conn.close()
            return
        conn.execute('INSERT INTO sales (lead_id, customer_name, amount, date) VALUES (?, ?, ?, ?)', (
            lead_id, name[0], float(amount), datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        print(f"Recorded sale for {name[0]}: ₹{amount}")
    except Exception as e:
        print("Error:", e)

def analyze_sales():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query('SELECT customer_name, amount, date FROM sales', conn)
    conn.close()
    if df.empty:
        print("No sales")
        return None, None, None, df
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    total = df['amount'].sum()
    monthly = df.groupby('month')['amount'].sum().reset_index()
    top = df.groupby('customer_name')['amount'].sum().nlargest(5).reset_index()
    print(f"Revenue: ₹{total}")
    print("Trend:\n", monthly)
    print("Top Customers:\n", top)
    return total, monthly, top, df

def plot_monthly_trend(monthly):
    plt.figure(figsize=(8,4))
    plt.plot(monthly['month'].astype(str), monthly['amount'], marker='o')
    plt.title('Monthly Revenue')
    plt.savefig('monthly_trend.png')
    plt.close()
    print("Saved plot: monthly_trend.png")

def plot_top_customers(top):
    plt.figure(figsize=(6,4))
    plt.bar(top['customer_name'], top['amount'], color='sky blue')
    plt.title('Top 5 Customers')
    plt.savefig('top_customers.png')
    plt.close()
    print("Saved plot: top_customers.png")

def export_to_pdf(total, monthly, top):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,txt="Sales Report",ln=True,align='C')
    pdf.cell(200,10,txt=f"Total Revenue: ₹{total:,.2f}",ln=True)
    pdf.cell(200,10,txt="Monthly Revenue",ln=True)
    for _, r in monthly.iterrows():
        pdf.cell(200,10,txt=f"{r['month']}: ₹{r['amount']:,.2f}",ln=True)
    pdf.cell(200,10,txt="Top Customers",ln=True)
    for _, r in top.iterrows():
        pdf.cell(200,10,txt=f"{r['customer_name']}: ₹{r['amount']:,.2f}",ln=True)
    pdf.output('sales_report.pdf')
    print("PDF saved: sales_report.pdf")

def export_to_excel(monthly, top, df):
    with pd.ExcelWriter('sales_report.xlsx') as writer:
        monthly.to_excel(writer, sheet_name='MonthlyTrend', index=False)
        top.to_excel(writer, sheet_name='TopCustomers', index=False)
        df.to_excel(writer, sheet_name='AllSales', index=False)
    print("Excel saved: sales_report.xlsx")

def generate_report():
    total, monthly, top, df = analyze_sales()
    if monthly is not None: plot_monthly_trend(monthly)
    if top is not None: plot_top_customers(top)
    export_to_excel(monthly, top, df)
    export_to_pdf(total, monthly, top)

# -------- Basic DB/CLI --------
def init_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            source TEXT,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            customer_name TEXT,
            amount REAL NOT NULL,
            date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    ''')
    conn.commit()
    conn.close()

def add_new_lead():
    name = input("Name: ")
    email = input("Email: ").strip().lower()
    phone = input("Phone with +countrycode: ")
    source = input("Source: ")
    if not name or not email: print("Name and Email required"); return
    if not is_valid_email(email): print("Invalid Email"); return
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute('INSERT INTO leads (name, email, phone, source) VALUES (?, ?, ?, ?)', (name, email, phone, source))
        conn.commit()
        conn.close()
        print(f"Lead '{name}' added.")
    except sqlite3.IntegrityError:
        print("Duplicate email.")
    except Exception as e:
        print("Error:", e)

def list_leads():
    conn = sqlite3.connect(DB_NAME)
    leads = conn.execute('SELECT id, name, email, phone, source, date_added FROM leads').fetchall()
    conn.close()
    print(f"{'ID':<4}{'Name':<18}{'Email':<24}{'Phone':<15}{'Source':<13}{'Date'}")
    print("-"*88)
    for l in leads:
        print(f"{l[0]:<4}{l[1]:<18}{l[2]:<24}{l[3]:<15}{l[4]:<13}{l[5][:10]}")
    print(f"Total leads: {len(leads)}")

def main_menu():
    init_database()
    while True:
        print("\n== KOGNITI MINDS CRM LITE ==")
        print("1. Add New Lead\n2. List Leads\n3. Import & Clean CSV\n4. Record Sale\n5. Analytics\n6. Generate Reports\n7. Bulk Emails\n8. WhatsApp Messages\n9. Exit")
        ch = input("Choice: ").strip()
        if ch == "1": add_new_lead()
        elif ch == "2": list_leads()
        elif ch == "3": import_clean_leads()
        elif ch == "4": record_sales_data()
        elif ch == "5": analyze_sales()
        elif ch == "6": generate_report()
        elif ch == "7": send_bulk_emails()
        elif ch == "8": send_whatsapp_messages()
        elif ch == "9": print("Bye!"); break
        else: print("Invalid choice")

if __name__ == "__main__":
    main_menu()
