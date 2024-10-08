#Creating a package for pip install using this app4 created earlier in course:
#-Rename main.py to somehitng more meaningful because this is what users will import - invoices.py
#-convert all code to classes and functions
#-Test the function: Create a main.py and import invoices.py. Then call it to test.
#-build the package
#  -Create new package folder "invoicing" and drag invoice.py into it
#  -create __init.py__ in this new folder and add the code you see in it.
#  -move everything except invoicing and venv folders out of this dir in prep for upload to pypi.
#  -Register your new username and pw in pypi  (userid: jjjcmar  pw: R....eee..!)
#  -Create a setup.py file in this dir, and update it with your upload info. (Search pypi for the name you want
#   to use to make sure its not already used. invoicing is already used, so name it invoicing-new.)
#  -in root dir terminal: >python setup.py sdist        This will create a dist dir which we will upload to pypi.
#  ->pip install twine
#  ->twine upload --skip-existing dist/*   (Give the userid and pw you created for pypi)

import os



import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

def generate(invoices_path, pdfs_path):
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add a header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
            pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        # Add total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image("pythonhow.png", w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)

        pdf.output(f"{pdfs_path}/{filename}.pdf")
