import boto3
from io import BytesIO
import os
import PyPDF2
import re
from datetime import datetime

def extract_and_insert_info_from_pdf(s3_bucket, s3_key, database_url, table_name, **opts):
    # Create a boto3 session and get the PDF content from S3
    session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    s3 = session.resource('s3')
    obj = s3.Object(s3_bucket, s3_key)
    response = obj.get()
    pdf_content = response['Body'].read()
    file_like_object = BytesIO(pdf_content)

    # Read and parse the PDF to extract information
    reader = PyPDF2.PdfReader(file_like_object)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + ' '

    # Extract information from the PDF text
    vendor_pattern = r"Vendor: (\w+)"
    date_pattern = r"Date: ([\d-]+)"
    total_cost_pattern = r"Total Cost: \$(\d+\.\d{2})"

    vendor = re.search(vendor_pattern, text)
    date = re.search(date_pattern, text)
    total_cost = re.search(total_cost_pattern, text)

    vendor_name = vendor.group(1) if vendor else "Unknown"
    invoice_date = datetime.strptime(date.group(1), '%Y-%m-%d').date() if date else "Unknown"
    total_cost_value = total_cost.group(1) if total_cost else "0.00"
    number_of_items = len(re.findall(r"Item\d+", text))  # Count 'Item' occurrences as number of items
    creation_time = datetime.now()  # Use current time as creation time

    # Connect to Phoenix and check for existing record
    conn = phoenixdb.connect(database_url, autocommit=True, **opts)
    cursor = conn.cursor()

    invoice_id = os.path.basename(s3_key)
    check_query = f"SELECT COUNT(*) FROM {table_name} WHERE InvoiceID = ?"
    cursor.execute(check_query, (invoice_id,))
    result = cursor.fetchone()

    if result[0] > 0:
        print(f"Record for file {invoice_id} already exists. Skipping upsert.")
    else:
        upsert_query = f"""
            UPSERT INTO {table_name} (
                InvoiceID, 
                "details"."VendorName", 
                "details"."InvoiceDate", 
                "details"."TotalCost", 
                "details"."NumberOfItems", 
                "metadata"."FileSize", 
                "metadata"."CreationDate", 
                "file"."PdfContent"
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(upsert_query, (invoice_id, vendor_name, invoice_date, total_cost_value, number_of_items, len(pdf_content), creation_time, pdf_content))
        print(f"Data upserted for file: {s3_key}")

    cursor.close()
    conn.close()
