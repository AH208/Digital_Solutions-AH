import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("road_crashes.csv")

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect("crashes.db")

# Write DataFrame to table "crashes"
df.to_sql("crashes", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("CSV imported into crashes.db")