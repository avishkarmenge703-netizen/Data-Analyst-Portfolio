import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import datetime

df = pd.read_csv('sample_data.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Profit Margin'] = df['Profit'] / df['Sales']

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
avg_margin = df['Profit Margin'].mean()
num_orders = df['Order ID'].nunique()
num_customers = df['Customer ID'].nunique()

top_customers = df.groupby('Customer Name')['Sales'].sum().nlargest(10).reset_index()

df['YearMonth'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['Sales'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)

plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales, x='YearMonth', y='Sales', marker='o')
plt.xticks(rotation=45)
plt.title('Monthly Sales Trend')
plt.tight_layout()
plt.savefig('monthly_trend.png')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Automated Sales Report', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Executive Summary', 0, 1)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, f"Total Sales: ${total_sales:,.2f}\nTotal Profit: ${total_profit:,.2f}\nAvg Profit Margin: {avg_margin:.2%}\nNumber of Orders: {num_orders}\nNumber of Customers: {num_customers}")
pdf.ln(5)

pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Top 10 Customers by Sales', 0, 1)
pdf.set_font('Arial', '', 10)
for idx, row in top_customers.iterrows():
    pdf.cell(0, 8, f"{row['Customer Name']}: ${row['Sales']:,.2f}", 0, 1)
pdf.ln(5)

pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Seasonal Trend', 0, 1)
pdf.image('monthly_trend.png', x=10, w=190)

pdf.output('sales_report.pdf')
print("✅ PDF report generated: sales_report.pdf")
