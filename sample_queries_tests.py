!pip install --progress-bar off -r requirements.txt

from flask import Flask, render_template, send_file
import phoenixdb
import io
import json
import os

app = Flask(__name__)

# Phoenix Database Configuration
opts = {}
opts['authentication'] = 'BASIC'
opts['serialization'] = 'PROTOBUF'
opts['avatica_user'] = '*******'
opts['avatica_password'] = '*****!'
database_url = 'https://cod--9guffabsj4p0-gateway0.se-sandb.a465-9q4k.cloudera.site/cod--9guffabsj4p0/cdp-proxy-api/avatica/'
TABLENAME = "archive.invoice"
phoenix_conn = phoenixdb.connect(database_url, autocommit=True,**opts) 

# Phoenix Connection
phoenix_cursor = phoenix_conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)

query = """select rowid,rawbytes,FILE_NAME,FILESIZE,EXTRAATTR1,HASH_VALUE from ARCHIVES.INVOICE2"""

#query = """select rowid,rawbytes,FILE_NAME,FILESIZE from ARCHIVES.INVOICE2"""

#query = """select rowid,rawbytes,  from ARCHIVES.INVOICE2"""

phoenix_cursor.execute(query)
result = phoenix_cursor.fetchone()
print(result)


columns = [column[0] for column in phoenix_cursor.description]
print(columns)

for cols in phoenix_cursor.description:
  print(cols)

pdf_binary_data = result['RAWBYTES']

def render_pdf(pdf_binary_data):
    buffer = io.BytesIO(pdf_binary_data)
    return send_file(buffer, download_name='invoice.pdf', mimetype='application/pdf')

print(pdf_binary_data)

  
## use index.html to present the results
#app = Flask(__name__)
#result = phoenix_cursor.fetchall()
#render_template('templates/index.html', data=result)
#

print(phoenix_cursor.fetchall())

