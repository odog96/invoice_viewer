from flask import Flask, render_template, request, flash, send_file, abort
import logging
import phoenixdb
import os
import io

# Setup logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Phoenix Database Configuration using environment variables
opts = {
    'authentication': os.getenv('AUTHENTICATION'),
    'serialization': os.getenv('SERIALIZATION'),
    'avatica_user': os.getenv('AVATICA_USER'),
    'avatica_password': os.getenv('AVATICA_PASSWORD')
}

database_url = os.getenv('DATABASE_URL')
tableName = os.getenv('TABLE_NAME')

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = phoenixdb.connect(database_url, autocommit=True, **opts)
    cursor = conn.cursor()

    # Query to get distinct VendorName values for the dropdown
    cursor.execute(f"SELECT DISTINCT \"VendorName\" FROM {tableName} ORDER BY \"VendorName\" ASC")
    vendors = [row[0] for row in cursor.fetchall()]

    records = []
    if request.method == 'POST' or request.args:
      # Starting base of the query
        base_query = f"SELECT INVOICEID, VendorName, InvoiceDate, TotalCost, NumberOfItems, FileSize, CreationDate FROM {tableName}"
        where_clauses = []
        params = []

      # Filter by VendorName
        vendor_name = request.args.get('vendorName')
        if vendor_name:
            where_clauses.append(f'VendorName = {vendor_name}')  # Changed from %s to ?
            params.append(vendor_name)
        # Filter by InvoiceDate
        invoice_date = request.args.get('invoiceDate')
        if invoice_date:
            where_clauses.append('"InvoiceDate" = %s')
            params.append(invoice_date)

      # Filter by TotalCost range
        min_total_cost = request.args.get('minTotalCost')
        max_total_cost = request.args.get('maxTotalCost')
        if min_total_cost:
            where_clauses.append('"TotalCost" >= %s')
            params.append(min_total_cost)
        if max_total_cost:
            where_clauses.append('"TotalCost" <= %s')
            params.append(max_total_cost)

      # Filter by NumberOfItems
      number_of_items = request.args.get('numberOfItems')
        if number_of_items:
            where_clauses.append('"NumberOfItems" = %s')
            params.append(number_of_items)

        # Filter by FileSize range
        min_file_size = request.args.get('minFileSize')
        max_file_size = request.args.get('maxFileSize')
        if min_file_size:
            where_clauses.append('"FileSize" >= %s')
            params.append(min_file_size)
        if max_file_size:
            where_clauses.append('"FileSize" <= %s')
            params.append(max_file_size)

        # Filter by CreationDate
        creation_date = request.args.get('creationDate')
        if creation_date:
            where_clauses.append('"CreationDate" = %s')
            params.append(creation_date)

        # Construct the final query
        if where_clauses:
            final_query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        else:
            final_query = base_querybase_query
    
  
    # Execute the query with parameters
    test_query = "SELECT INVOICEID, VendorName, InvoiceDate, TotalCost, NumberOfItems, FileSize, CreationDate FROM INVOICES"
    test_query = "SELECT * FROM INVOICES"
    #cursor.execute(final_query, params)
    #cursor.execute(test_query, params)
    cursor.execute(test_query)
    records = cursor.fetchall()

    print("Final Query:", final_query)
    print("test_query",test_query)
    print("Params:", params)
    print("Vendor:", vendor_name)
    
    # Render template with records (assumed you have a records.html template)
    return render_template('records.html', records=records)
        
        # For demonstration, let's use a simple query (adjust as needed)
        test_query = f"SELECT * FROM {tableName}"
        cursor.execute(test_query)
        records = cursor.fetchall()

    # Render the same template, but now pass both 'vendors' and 'records' to it
    return render_template('index.html', vendors=vendors, records=records)

@app.route('/download-pdf/<invoice_id>')
def download_pdf(invoice_id):
    # Ensure the connection is established here as well, similar to the index function
    conn = phoenixdb.connect(database_url, autocommit=True, **opts)
    cursor = conn.cursor()

    # Query Phoenix table to get PdfContent for the given INVOICEID
    query = f"SELECT PdfContent FROM {tableName} WHERE INVOICEID = ?"
    cursor.execute(query, [invoice_id])
    pdf_content = cursor.fetchone()

    if pdf_content:
        # Convert the binary data to a BytesIO object
        pdf_io = io.BytesIO(pdf_content[0])

        # Send the binary data as a downloadable file
        return send_file(pdf_io, as_attachment=True, download_name=f"{invoice_id}.pdf", mimetype='application/pdf')
    else:
        abort(404)  # Record not found

if __name__ == "__main__":
    app_port = int(os.getenv("CDSW_PUBLIC_PORT", 5000))  # Default to 5000 if not set
    app.run(host="127.0.0.1", port=app_port)
