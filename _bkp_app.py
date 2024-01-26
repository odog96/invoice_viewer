!pip install phoenixdb

from flask import Flask, render_template, send_file, send_from_directory, request
import logging
import phoenixdb
import io
import json
import os

# This reduces the the output to the
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path="")

# Phoenix Database Configuration
opts = {}
opts['authentication'] = 'BASIC'
opts['serialization'] = 'PROTOBUF'
opts['avatica_user'] = 'mmattson'
opts['avatica_password'] = '5Alamander!'
database_url = 'https://cod--9guffabsj4p0-gateway0.se-sandb.a465-9q4k.cloudera.site/cod--9guffabsj4p0/cdp-proxy-api/avatica/'
tableName = "archives.invoice2"
phoenix_conn = phoenixdb.connect(database_url, autocommit=True,**opts) 

# Phoenix Connection
# phoenix_conn = phoenixdb.connect(phoenix_config)
phoenix_cursor = phoenix_conn.cursor()

@app.route('/')
def home():
    return "<script> window.location.href = '/templates/index.html'</script>"
  
def index():
    # Example query to fetch binary data (PDF) from Phoenix table 'invoice2' with column 'rawbytes'
    query = 'SELECT rawbytes FROM archives.invoice2'
    phoenix_cursor.execute(query)
    result = phoenix_cursor.fetchone()

    if result:
        # Get the binary data from the result
        pdf_binary_data = result['RAWBYTES']

        # Render the PDF file
        return render_pdf(pdf_binary_data)
    else:
        return "No data found."

def render_pdf(binary_data):
    # Create an in-memory buffer for the PDF content
    buffer = io.BytesIO(binary_data)

    # Return the PDF file as a response
    return send_file(buffer, download_name='invoice.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host="127.0.0.1",
           port=int(os.environ['CDSW_APP_PORT']))