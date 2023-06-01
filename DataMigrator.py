# Import modules
import pyodbc

# Connect to the database using Windows authentication
server = 'tcp:YONATAN-PC.customerData.windows.net'
database = 'customerData'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cur = cnxn.cursor()

# Create a table if not exists
cur.execute("CREATE TABLE IF NOT EXISTS geo_data (id INTEGER PRIMARY KEY, latitude REAL, longitude REAL, name TEXT)")

# Open the csv file
with open("geo_data.csv", "r") as f:
    # Skip the header row
    next(f)
    # Insert each row into the table using executemany
    cur.executemany("INSERT INTO geo_data (latitude, longitude, name) VALUES (?, ?, ?)", f)

# Commit the changes and close the connection
cnxn.commit()
cnxn.close()