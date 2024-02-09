import PyPDF2
import re
import os
import datetime
import sys
import phoenixdb
from datetime import datetime


# Database configuration

database_url = os.getenv('DATABASE_URL')
#table_name=os.getenv('TABLE_NAME')
table_name="INVOICES" 


# testing a new db... remove later in production
#database_url = 'https://cod-r0ie7klcltu-gateway0.se-sandb.a465-9q4k.cloudera.site/cod-r0ie7klcltu/cdp-proxy-api/avatica/'


opts = {
    'authentication': os.getenv('AUTHENTICATION'),  # Default to 'BASIC' if not set
    'serialization': os.getenv('SERIALIZATION'),  # Default to 'PROTOBUF' if not set
    'avatica_user': os.getenv('AVATICA_USER'),
    'avatica_password': os.getenv('AVATICA_PASSWORD')
}


def extract_and_insert_info_from_pdf(pdf_path, database_url, table_name,**opts):
    # Extract PDF information

    
    
    with open(pdf_path, 'rb') as file:
        # Read binary content of the PDF
        pdf_content = file.read()
        # Read text contents of the PDF
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + ' '

    # Define patterns for information extraction
    vendor_pattern = r"Vendor: (\w+)"
    date_pattern = r"Date: ([\d-]+)"
    total_cost_pattern = r"Total Cost: \$(\d+\.\d{2})"
    items_pattern = r"Items:"

    # Search for patterns
    vendor = re.search(vendor_pattern, text)
    date = re.search(date_pattern, text)
    total_cost = re.search(total_cost_pattern, text)
    items_list = text.split(items_pattern)[-1]
    number_of_items = len(items_list.split('\n')) - 1

    # Extracted values
    vendor_name = vendor.group(1) if vendor else "Unknown"
    invoice_date = date.group(1) if date else "Unknown"
    
    # convert to datetime
    invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d').date()

    
    total_cost_value = total_cost.group(1) if total_cost else "0.00"

    # File metadata
    file_stats = os.stat(pdf_path)
    file_size = file_stats.st_size
    creation_time = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    creation_time = datetime.strptime(creation_time, '%Y-%m-%d %H:%M:%S')
    
    # Connect to Phoenix and insert data
    conn = phoenixdb.connect(database_url, autocommit=True,**opts)
    cursor = conn.cursor()
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
#    cursor.execute(upsert_query, (os.path.basename(pdf_path), vendor_name, invoice_date, total_cost_value, number_of_items, pdf_path))

    cursor.execute(upsert_query, (os.path.basename(pdf_path),vendor_name,                
      invoice_date, total_cost_value, number_of_items,file_size,  
      creation_time,pdf_content))

    print(f"Data inserted for file: {pdf_path}")


    # Test pdf read capability
#    print(f"File Size: {file_size} bytes")
#    print(f"Date Created: {creation_time}")
#
#
#    print(f"Vendor: {vendor_name}")
#    print(f"Date: {invoice_date}")
#    print(f"Total Cost: {total_cost_value}")
#    print(f"Number of Items: {number_of_items}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python read_invoice.py <path_to_pdf_file>")
        sys.exit(1)

    pdf_path = sys.argv[1]
#    database_url = 'your_phoenix_query_server_url'
#    table_name = 'your_table_name'

    extract_and_insert_info_from_pdf(pdf_path, database_url, table_name,**opts)

    cursor.close()
    conn.close()