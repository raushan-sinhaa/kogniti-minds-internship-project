#  1.Build a Sales Analyzer Script that reads sales_data.csv and generates:
#    Total revenue
#    Monthly revenue trend
#    Top 5 customers

import pandas as pd

def analyze_sales(csv_file='sales_data.csv'):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ File '{csv_file}' not found.")
        return None

    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # Total revenue
    total_revenue = df['amount'].sum()

    # Monthly revenue trend
    df['month'] = df['date'].dt.to_period('M')
    monthly_trend = df.groupby('month')['amount'].sum().reset_index()

    # Top 5 customers
    top_customers = df.groupby('customer')['amount'].sum().nlargest(5).reset_index()

    # Output results
    print(f"✅ Total Revenue: ₹{total_revenue:,.2f}\n")

    print("📈 Monthly Revenue Trend:")
    print(monthly_trend.to_string(index=False))

    print("\n🏆 Top 5 Customers:")
    print(top_customers.to_string(index=False))

    return total_revenue, monthly_trend, top_customers

if __name__ == "__main__":
    analyze_sales()
