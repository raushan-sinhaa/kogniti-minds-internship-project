#                            Tasks 3
#                  Data Analysis & Visualization
#  Goal: Analyze sales and customer data for better insights.
#  Tasks:
#  1.Build a Sales Analyzer Script that reads sales_data.csv and generates:
#    Total revenue
#    Monthly revenue trend
#    Top 5 customers
#  2.Use Matplotlib to visualize sales trends (bar chart & line graph).
#  3.Export reports to Excel & PDF format

from sales_analyzer import analyze_sales
from visualizer import plot_monthly_trend, plot_top_customers
from exporter import export_to_excel, export_to_pdf

def main():
    total, monthly, top, raw = analyze_sales()
    plot_monthly_trend(monthly)
    plot_top_customers(top)
    export_to_excel(monthly, top, raw)
    export_to_pdf(total, monthly, top)

if __name__ == "__main__":
    main()
