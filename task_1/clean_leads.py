#   1. Write a Python script to read company leads (CSV format) and:
#      Validate emails
#      Remove duplicate entries
#      Save clean data into clean_customers.csv

import pandas as pd
import re

#  format for checking if mail is valid or not from company_leads.csv
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))

# cleaning the data of customers from company_leads.csv file then store the output file in the clean_customers.csv
def clean_leads(input_file='company_leads.csv', output_file='clean_customers.csv'):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"❌ File '{input_file}' not found.")
        return

    df.columns = df.columns.str.strip().str.lower()

    if 'email' not in df.columns:
        print("❌ 'email' column not found in the dataset.")
        print("📌 Available columns:", df.columns.tolist())
        return

# counting valid email from company_leads.csv list
    initial_count = len(df)
    df['valid_email'] = df['email'].apply(is_valid_email)
    df = df[df['valid_email']].drop(columns='valid_email')
    valid_count = len(df)

# Deleting invalid and duplicated email from company_leads.csv list
    df_clean = df.drop_duplicates(subset='email')
    final_count = len(df_clean)

# Storing valid customer list to clean_customers.csv
    df_clean.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to '{output_file}'")
    print(f"📊 Initial: {initial_count}, Valid: {valid_count}, Final: {final_count}")

if __name__ == "__main__":
    clean_leads()
