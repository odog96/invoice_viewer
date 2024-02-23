import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from datetime import datetime, timedelta
import boto3

def create_invoice(filename, vendor_name, items, date):
    """
    Creates a PDF invoice with given vendor name, items, and date, then uploads it to S3.
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

    access_id = os.getenv('aws_access_key_id')
    access_key = os.getenv('aws_secret_access_key')
    
#    upload_to_s3(filename, f'ozarate/invoices/{os.path.basename(filename)}')
    upload_to_s3(filename, f'ozarate/invoices/{os.path.basename(filename)}', access_id, access_key)


#def upload_to_s3(file_name, s3_file_name, bucket_name='goes-se-sandbox01'):
#    """
#    Uploads a file to an S3 bucket.
#    """
#    s3 = boto3.client('s3')
#    s3.upload_file(file_name, bucket_name, s3_file_name)

def upload_to_s3(file_name, s3_file_name, aws_access_key_id, aws_secret_access_key):
    """
    Uploads a file to an S3 bucket using provided AWS credentials.
    :param file_name: File to upload.
    :param s3_file_name: S3 object name.
    :param aws_access_key_id: AWS access key ID.
    :param aws_secret_access_key: AWS secret access key.
    """
    bucket_name = 'goes-se-sandbox01'

    # Creating a boto3 session with credentials
    session = boto3.Session(
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key')
    )

    # Creating an S3 resource from the session
    s3 = session.resource('s3')

    # Uploading the file
    s3.Bucket(bucket_name).upload_file(file_name, s3_file_name)
    print(f'File uploaded to s3://{bucket_name}/{s3_file_name}')

def generate_invoice_data():
    """
    Generates random data for an invoice.
    """
    vendor_num = random.randint(1, 10)
    item_count = random.randint(1, 10)
    items = {f"Item{item}": round(random.uniform(5.0, 50.0), 2) for item in range(1, item_count + 1)}
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    days_between_dates = (end_date - start_date).days
    random_date = start_date + timedelta(days=random.randint(0, days_between_dates))
    return f"Vendor_{vendor_num:02}", items, random_date

def main():
    vendor_name, items, invoice_date = generate_invoice_data()
    invoice_date = invoice_date.date()
    filename = f"{vendor_name}_{invoice_date}.pdf"
    create_invoice(filename, vendor_name, items, invoice_date)

if __name__ == "__main__":
    main()
