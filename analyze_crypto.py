import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# File paths
DATA_FILE = "crypto_data.xlsx"
EXCEL_FILE = "crypto_analysis.xlsx"
PDF_FILE = "crypto_analysis.pdf"

def save_to_pdf(df_analysis, df_top5, filename):
    """Save analysis and top 5 cryptocurrencies to a PDF file."""
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("📊 Cryptocurrency Market Analysis", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))  # Spacer for better formatting

    # Convert DataFrames to table format
    def dataframe_to_table(df):
        table_data = [df.columns.to_list()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        return table

    # Add Analysis Table
    elements.append(Paragraph("📌 Market Insights", styles["Heading2"]))
    elements.append(dataframe_to_table(df_analysis))
    elements.append(Spacer(1, 20))

    # Add Top 5 Cryptocurrencies Table
    elements.append(Paragraph("🏆 Top 5 Cryptocurrencies by Market Capitalization", styles["Heading2"]))
    elements.append(dataframe_to_table(df_top5))

    # Build PDF
    pdf.build(elements)
    print(f"✅ Crypto analysis saved to: {filename}")

def analyze_crypto_data():
    """Perform analysis on cryptocurrency data."""
    try:
        # Load the latest data from the Excel file
        df = pd.read_excel(DATA_FILE, sheet_name="Live Data")

        # Ensure required columns exist
        required_columns = ["Cryptocurrency", "Symbol", "Current Price (USD)", "Market Capitalization", "24h Change (%)"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column in data: {col}")

        # 1️⃣ Identify the top 5 cryptocurrencies by market capitalization
        top_5_by_market_cap = df.nlargest(5, "Market Capitalization")[["Cryptocurrency", "Symbol", "Market Capitalization"]]

        # 2️⃣ Calculate the average price of the top 50 cryptocurrencies
        average_price = df["Current Price (USD)"].mean()

        # 3️⃣ Find the highest and lowest 24-hour percentage price change
        highest_24h_change = df.loc[df["24h Change (%)"].idxmax()]
        lowest_24h_change = df.loc[df["24h Change (%)"].idxmin()]

        # Prepare analysis summary
        analysis_data = {
            "Metric": [
                "Average Price of Top 50",
                "Highest 24h % Change",
                "Lowest 24h % Change"
            ],
            "Value": [
                average_price,
                highest_24h_change["24h Change (%)"],
                lowest_24h_change["24h Change (%)"]
            ],
            "Cryptocurrency": [
                "All",
                highest_24h_change["Cryptocurrency"],
                lowest_24h_change["Cryptocurrency"]
            ],
            "Symbol": [
                "-",
                highest_24h_change["Symbol"],
                lowest_24h_change["Symbol"]
            ]
        }
        df_analysis = pd.DataFrame(analysis_data)

        # Save data to Excel
        with pd.ExcelWriter(EXCEL_FILE, mode="w", engine="openpyxl") as writer:
            df_analysis.to_excel(writer, index=False, sheet_name="Analysis")
            top_5_by_market_cap.to_excel(writer, index=False, sheet_name="Top 5 Market Cap")

        print(f"✅ Crypto analysis saved to: {EXCEL_FILE}")

        # Save data to PDF
        save_to_pdf(df_analysis, top_5_by_market_cap, PDF_FILE)

    except Exception as e:
        print("⚠️ Error analyzing data:", str(e))

# Run the analysis
if __name__ == "__main__":
    analyze_crypto_data()
