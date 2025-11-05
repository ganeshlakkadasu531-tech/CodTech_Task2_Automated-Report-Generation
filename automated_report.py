
# automated_report.py
import os
import sys
from datetime import datetime

# -----------------------------
# Import required libraries
# -----------------------------
try:
    import pandas as pd
except ImportError:
    print("❌ Error: pandas not found. Install it using 'pip install pandas'")
    sys.exit(1)

try:
    from fpdf import FPDF
except ImportError:
    print("❌ Error: fpdf not found. Install it using 'pip install fpdf2'")
    sys.exit(1)


# -----------------------------
# Step 1: Read CSV Data
# -----------------------------
def read_data(path="data.csv"):
    """Read CSV file and validate the required columns."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Data file not found: {path}")

    df = pd.read_csv(path)

    # Validate columns
    required_cols = {"Name", "Marks"}
    if not required_cols.issubset(df.columns):
        raise ValueError("❌ CSV must contain 'Name' and 'Marks' columns.")

    # Convert Marks to numeric values
    df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")

    if df["Marks"].isnull().any():
        raise ValueError("❌ All 'Marks' values must be numeric.")

    return df


# -----------------------------
# Step 2: Create PDF Class
# -----------------------------
class SimpleReportPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "CODTECH - Automated Report", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


# -----------------------------
# Step 3: Generate PDF Report
# -----------------------------
def generate_pdf_report(df, out_path="report.pdf"):
    """Generate a PDF report from the DataFrame."""
    pdf = SimpleReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Metadata / Summary
    total = len(df)
    avg = round(df["Marks"].mean(), 2)
    highest = int(df["Marks"].max())
    lowest = int(df["Marks"].min())
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf.cell(0, 8, f"Generated: {date_str}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Summary", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 7, f"Total Students: {total}", ln=True)
    pdf.cell(0, 7, f"Average Marks: {avg}", ln=True)
    pdf.cell(0, 7, f"Highest Marks: {highest}", ln=True)
    pdf.cell(0, 7, f"Lowest Marks: {lowest}", ln=True)

    # Table header
    pdf.ln(8)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 8, "Name", border=1)
    pdf.cell(40, 8, "Marks", border=1, ln=True)

    # Table rows
    pdf.set_font("Arial", size=11)
    for _, row in df.iterrows():
        name = str(row["Name"])
        marks = str(int(row["Marks"]))
        if len(name) > 30:
            name = name[:27] + "..."
        pdf.cell(100, 8, name, border=1)
        pdf.cell(40, 8, marks, border=1, ln=True)

    # Analysis Section
    pdf.ln(8)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Analysis", ln=True)
    pdf.set_font("Arial", size=11)
    pass_count = (df["Marks"] >= 35).sum()
    pass_percent = round((pass_count / total) * 100, 2) if total > 0 else 0
    pdf.multi_cell(0, 6, f"Out of {total} students, {pass_count} passed ({pass_percent}%).")

    # Save PDF
    pdf.output(out_path)
    return out_path


# -----------------------------
# Step 4: Main Function
# -----------------------------
def main():
    csv_path = "data.csv"
    out_pdf = "report.pdf"

    try:
        df = read_data(csv_path)
    except Exception as e:
        print("❌ Error reading data:", e)
        sys.exit(1)

    try:
        result = generate_pdf_report(df, out_path=out_pdf)
        print(f"✅ Report successfully created: {result}")
    except Exception as e:
        print("❌ Error generating PDF:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()