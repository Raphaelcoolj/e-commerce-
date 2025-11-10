import os
import psycopg2

# Use your Render DATABASE_URL if set as env variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://walletdb_83ld_user:s9ug22NICX3FbBlyoM90tVjZSX6IFuOc@dpg-d473jsbipnbc73cj356g-a.oregon-postgres.render.com/walletdb_83ld")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("✅ Database connection successful!")
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Database connection failed:", e)
