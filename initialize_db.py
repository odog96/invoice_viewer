import phoenixdb
import os

# Database configuration

database_url = os.getenv('DATABASE_URL')

# testing a new db... remove later in production
database_url = 'https://cod-r0ie7klcltu-gateway0.se-sandb.a465-9q4k.cloudera.site/cod-r0ie7klcltu/cdp-proxy-api/avatica/'


opts = {
    'authentication': os.getenv('AUTHENTICATION'),  # Default to 'BASIC' if not set
    'serialization': os.getenv('SERIALIZATION'),  # Default to 'PROTOBUF' if not set
    'avatica_user': os.getenv('AVATICA_USER'),
    'avatica_password': os.getenv('AVATICA_PASSWORD')
}

conn = phoenixdb.connect(database_url, autocommit=True,**opts)

# Create table with an additional column for the PDF binary data
create_table_sql = """
CREATE TABLE IF NOT EXISTS Invoices (
    InvoiceID VARCHAR PRIMARY KEY,
    "details"."VendorName" VARCHAR,
    "details"."InvoiceDate" DATE,
    "details"."TotalCost" DECIMAL,
    "details"."NumberOfItems" INTEGER,
    "metadata"."FileSize" BIGINT,
    "metadata"."CreationDate" TIMESTAMP,
    "file"."PdfContent" VARBINARY -- Use VARBINARY to store PDF binary data
)"""

# testing to see tables
#see_tbls="""SELECT DISTINCT TABLE_SCHEM, TABLE_NAME FROM SYSTEM.CATALOG"""
#cursor.execute(see_tbls)
#result = cursor.fetchone()
#print(result)


# Execute the create table statement
cursor = conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)

#cursor.execute(simple_create_table_sql)

cursor.execute(create_table_sql)


cursor.close()
conn.close()

print("Table 'Invoices' created successfully with PDF storage capability.")
