#!pip install --progress-bar off -r requirements.txt

from flask import Flask, render_template, send_file
import phoenixdb
import io
import json
import os

app = Flask(__name__)

# Phoenix Database Configuration

#opts = {}
#opts['authentication'] = 'BASIC'
#opts['serialization'] = 'PROTOBUF'
#opts['avatica_user'] = 'ozarate'
#opts['avatica_password'] = 'Oreoiscute1!'



#database_url = "https://cod-r0-LoadB-xFwbyEBxikob-d2fa90f06839727b.elb.us-east-2.amazonaws.com/cod-r0ie7klcltu/cdp-proxy-api/avatica/"
database_url = 'https://cod-r0ie7klcltu-gateway0.se-sandb.a465-9q4k.cloudera.site/cod-r0ie7klcltu/cdp-proxy-api/avatica/'
#database_url = 'https://cod-1umd4u6yvemjl-gateway0.se-sandb.a465-9q4k.cloudera.site/cod-1umd4u6yvemjl/cdp-proxy-api/avatica/'
opts = {
    'authentication': os.getenv('AUTHENTICATION'),  # Default to 'BASIC' if not set
    'serialization': os.getenv('SERIALIZATION'),  # Default to 'PROTOBUF' if not set
    'avatica_user': os.getenv('AVATICA_USER'),
    'avatica_password': os.getenv('AVATICA_PASSWORD')
}

phoenix_conn = phoenixdb.connect(database_url, autocommit=True,**opts) 

# Phoenix Connection
phoenix_cursor = phoenix_conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)

query = """select count(*) from INVOICES"""

#query = """select * from INVOICES"""

#query = """select rowid,rawbytes,FILE_NAME,FILESIZE,EXTRAATTR1,HASH_VALUE from ARCHIVES.INVOICE2"""

#query = """select rowid,rawbytes,FILE_NAME,FILESIZE from ARCHIVES.INVOICE2"""

#query = """select rowid,rawbytes,  from ARCHIVES.INVOICE2"""

phoenix_cursor.execute(query)
result = phoenix_cursor.fetchone()
print(result)


columns = [column[1] for column in phoenix_cursor.description]
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

phoenix_cursor.close()
phoenix_conn.close()

print(phoenix_cursor.fetchall())

