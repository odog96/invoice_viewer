!pip install --progress-bar off -r requirements.txt

from flask import Flask, render_template, send_file, send_from_directory, request
import logging
import phoenixdb
import io
import json
import subprocess
import os

# This reduces the the output to the
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Phoenix Database Configuration
opts = {}
opts['authentication'] = 'BASIC'
opts['serialization'] = 'PROTOBUF'
opts['avatica_user'] = 
opts['avatica_password'] = '***********'
database_url = 'https://cod--9guffabsj4p0-gateway0.se-sandb.a465-9q4k.cloudera.site/cod--9guffabsj4p0/cdp-proxy-api/avatica/'
tableName = "archives.invoice2"
phoenix_conn = phoenixdb.connect(database_url, autocommit=True,**opts) 

# Phoenix Connection
phoenix_cursor = phoenix_conn.cursor()

#@app.route('/')
#def home():
#    # Example query to fetch binary data (PDF) from Phoenix table 'invoice2' with column 'rawbytes'
#    query = """select rowid,rawbytes from ARCHIVES.INVOICE2"""
#    phoenix_cursor.execute(query)
#    result = phoenix_cursor.fetchall()
#    return render_template('index.html', data=result)

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        phoenix_conn = phoenixdb.connect(database_url, autocommit=True, **opts) 
        phoenix_cursor = phoenix_conn.cursor()
        if request.method == 'POST':
            # Use request.form to access submitted data
            query = """select rowid,rawbytes ,FILE_NAME,FILESIZE,EXTRAATTR1,HASH_VALUE from ARCHIVES.INVOICE2"""
        else:
            query = """select rowid,rawbytes ,FILE_NAME,FILESIZE,EXTRAATTR1,HASH_VALUE from ARCHIVES.INVOICE2"""
        
        phoenix_cursor.execute(query)
        result = phoenix_cursor.fetchall()
        print(result)
        return render_template('index.html', data=result)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return render_template('index.html', data=[])



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_PUBLIC_PORT"]))
  
