import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from datetime import datetime, timedelta

# Introduction:
# This script generates random invoices in PDF format and stores them in a specified folder.
# Each invoice includes a vendor name, items with costs, and a date.
# TODO: Implement functionality to upload generated PDF files to an S3 or ADLS bucket.

def create_invoice(filename, vendor_name, items, date):
    """
    Creates a PDF invoice with given vendor name, items, and date.
    :param filename: The path to save the PDF file.
    :param vendor_name: Name of the vendor for the invoice.
    :param items: Dictionary of items with their costs.
    :param date: The date of the invoice.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"Vendor: {vendor_name}")
    c.drawString(100, 735, f"Date: {date.isoformat()}")
    y = 720
    c.drawString(100, y, "Items:")
    total_cost = 0
    for item, cost in items.items():
        y -= 15
        c.drawString(110, y, f"{item}: ${cost:.2f}")
        total_cost += cost
    c.drawString(100, y - 30, f"Total Cost: ${total_cost:.2f}")
    c.save()

def empty_folder(folder):
    """
    Empties the specified folder, deleting all its contents.
    :param folder: The folder to be emptied.
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def generate_invoice_data(date_offset_list=[]):
    """
    Generates random data for an invoice, including vendor number, item count, and invoice date.
    Ensures that the invoice date is chosen without replacement from the given range.
    :param date_offset_list: List of already chosen date offsets to avoid repetition.
    :return: Tuple containing vendor name, items, invoice date, and the chosen date offset.
    """
    vendor_num = random.randint(1, 10)
    item_count = random.randint(1, 10)
    items = {f"Item{item}": round(random.uniform(5.0, 50.0), 2) for item in range(1, item_count + 1)}
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    while random_number_of_days in date_offset_list:  # Avoiding date repetition
        random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    return f"Vendor_{vendor_num:02}", items, random_date, random_number_of_days

# Setup and invoice generation
invoices_folder = 'invoices'
if not os.path.exists(invoices_folder):
    os.makedirs(invoices_folder)
elif os.listdir(invoices_folder):
    proceed = input("The 'invoices' folder is not empty. To continue, it will be emptied. Proceed? (y/n): ")
    if proceed.lower() == 'y':
        empty_folder(invoices_folder)
    else:
        print("Operation cancelled.")
        exit()

num_invoices = int(input("How many invoices do you need? "))

date_offset_list = []
for i in range(num_invoices):
    vendor_name, items, invoice_date, random_number_of_days = generate_invoice_data(date_offset_list)
    invoice_date = invoice_date.date()
    date_offset_list.append(random_number_of_days)
    filename = os.path.join(invoices_folder, f"{vendor_name}_{invoice_date}.pdf")
    create_invoice(filename, vendor_name, items, invoice_date)
    print(f"Invoice {i+1} created.")

print("Invoices generated successfully.")
