from flask import Flask, render_template, request, flash
import logging
import phoenixdb
import os

# Setup logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Phoenix Database Configuration using environment variables
opts = {
    'authentication': os.getenv('AUTHENTICATION'),  # Default to 'BASIC' if not set
    'serialization': os.getenv('SERIALIZATION'),  # Default to 'PROTOBUF' if not set
    'avatica_user': os.getenv('AVATICA_USER'),
    'avatica_password': os.getenv('AVATICA_PASSWORD')
}

database_url = os.getenv('DATABASE_URL')
tableName = os.getenv('TABLE_NAME')

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        phoenix_conn = phoenixdb.connect(database_url, autocommit=True, **opts)
        phoenix_cursor = phoenix_conn.cursor()
        query = f"SELECT rowid, rawbytes, FILE_NAME, FILESIZE, EXTRAATTR1, HASH_VALUE FROM {tableName}"
        phoenix_cursor.execute(query)
        result = phoenix_cursor.fetchall()
        return render_template('index.html', data=result)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return render_template('index.html', data=[])

if __name__ == "__main__":
    app_port = int(os.getenv("CDSW_PUBLIC_PORT", 5000))  # Default to 5000 if not set
    app.run(host="127.0.0.1", port=app_port)