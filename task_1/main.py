#                     Task 1
#       Data Handling (Lead Management Basics)
#  Goal: Learn to clean and organize company data.
#  Tasks:
#  1. Write a Python script to read company leads (CSV format) and:
#     Validate emails
#     Remove duplicate entries
#     Save clean data into clean_customers.csv
#  2. Create an Excel Report Generator that:
#     Counts daily/weekly leads
#     Maintains a record of unique customers
#     Generates output as leads_report.xlsx

import argparse
from clean_leads import clean_leads
from generate_report import generate_report

def main():
    parser = argparse.ArgumentParser(description="Lead Cleaning and Reporting Tool")
    parser.add_argument('--clean', action='store_true', help="Run lead cleaning")
    parser.add_argument('--report', action='store_true', help="Generate lead report")
    parser.add_argument('--input', type=str, default='company_leads.csv', help="Input file path")
    parser.add_argument('--output', type=str, help="Output file path")

    args = parser.parse_args()

    if args.clean:
        output_file = args.output if args.output else 'clean_customers.csv'
        clean_leads(input_file=args.input, output_file=output_file)

    if args.report:
        input_file = args.input if args.input else 'clean_customers.csv'
        output_file = args.output if args.output else 'leads_reports.xlsx'
        generate_report(input_file=input_file, output_file=output_file)

    if not args.clean and not args.report:
        print("⚠️ Please specify at least one action: --clean or --report")

if __name__ == "__main__":
    main()