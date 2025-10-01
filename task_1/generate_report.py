#  2. Create an Excel Report Generator that:
#     Counts daily/weekly leads
#     Maintains a record of unique customers
#     Generates output as leads_report.xlsx

import pandas as pd
import os

def generate_report(input_file='clean_customers.csv', output_file='leads_reports.xlsx'):
    # Check if file exists and this is not empty
    if not os.path.exists(input_file):
        print(f"❌ File '{input_file}' not found.")
        return
    if os.path.getsize(input_file) == 0:
        print(f"⚠️ File '{input_file}' is empty. Cannot generate report.")
        return

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Failed to read '{input_file}': {e}")
        return

    df.columns = df.columns.str.strip().str.lower()

    if 'date' not in df.columns or 'email' not in df.columns:
        print("❌ Required columns 'date' and/or 'email' not found.")
        print("📌 Available columns:", df.columns.tolist())
        return

    # Convert 'date' column to datetime so that it can be tracked
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    if df.empty:
        print("⚠️ No valid date entries found. Report generation skipped.")
        return

    # Daily lead count of customers
    daily_counts = df.groupby(df['date'].dt.date).size().reset_index(name='Daily Leads')

    # Weekly lead count of customers
    df['week'] = df['date'].dt.strftime('%Y-W%U')
    weekly_counts = df.groupby('week').size().reset_index(name='Weekly Leads')

    # Unique customers by email list
    unique_customers = df.drop_duplicates(subset='email')

    # Write to Excel file by email list
    with pd.ExcelWriter(output_file) as writer:
        daily_counts.to_excel(writer, sheet_name='Daily Leads', index=False)
        weekly_counts.to_excel(writer, sheet_name='Weekly Leads', index=False)
        unique_customers.to_excel(writer, sheet_name='Unique Customers', index=False)

    print(f"✅ Report generated and saved as '{output_file}'")
    print(f"📊 Daily: {len(daily_counts)}, Weekly: {len(weekly_counts)}, Unique Customers: {len(unique_customers)}")

if __name__ == "__main__":
    generate_report()