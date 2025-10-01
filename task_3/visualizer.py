# 2.Use Matplotlib to visualize sales trends (bar chart & line graph)

import matplotlib.pyplot as plt

def plot_monthly_trend(monthly_df):
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_df['month'].astype(str), monthly_df['amount'], marker='o')
    plt.title('Monthly Revenue Trend')
    plt.xlabel('Month')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_trend.png')
    plt.close()

def plot_top_customers(top_df):
    plt.figure(figsize=(8, 5))
    plt.bar(top_df['customer'], top_df['amount'], color='skyblue')
    plt.title('Top 5 Customers by Revenue')
    plt.xlabel('Customer')
    plt.ylabel('Revenue')
    plt.tight_layout()
    plt.savefig('top_customers.png')
    plt.close()

