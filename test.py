import sqlalchemy

db_url = "mysql+pymysql://root:nkNHIzniNHOqHrTpOrwuHFQbdOWhedHn@kodama.proxy.rlwy.net:45112/railway"
engine = sqlalchemy.create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 1"))
        print("✅ Connected:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
