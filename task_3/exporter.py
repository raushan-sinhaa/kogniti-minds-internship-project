# 3.Export reports to Excel & PDF format.

from fpdf import FPDF

def export_to_pdf(total_revenue, monthly_df, top_customers_df, output_file='sales_report.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="📊 Sales Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Total Revenue: ₹{total_revenue:,.2f}", ln=True)

    pdf.cell(200, 10, txt="Monthly Revenue Trend:", ln=True)
    for _, row in monthly_df.iterrows():
        pdf.cell(200, 10, txt=f"{row['month']}: ₹{row['amount']:,.2f}", ln=True)

    pdf.cell(200, 10, txt="Top 5 Customers:", ln=True)
    for _, row in top_customers_df.iterrows():
        pdf.cell(200, 10, txt=f"{row['customer']}: ₹{row['amount']:,.2f}", ln=True)

    pdf.output(output_file)
    print(f"📄 PDF report saved as '{output_file}'")
