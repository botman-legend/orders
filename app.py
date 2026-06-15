import streamlit as st
import sqlalchemy
import pandas as pd

# Database connection string stored in secrets
db_url = st.secrets["DATABASE_URL"]
engine = sqlalchemy.create_engine(db_url)

# Shop passwords stored in secrets
shop_passwords = st.secrets["SHOP_PASSWORDS"]

st.title("🛒 Shop Orders Dashboard")

# --- Login form ---
shop_name = st.text_input("Shop name (e.g. admin)")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if shop_name in shop_passwords and password == shop_passwords[shop_name]:
        st.success(f"✅ Login successful for {shop_name}")

        # Build hostname from shop name
        hostname = f"{shop_name}.botsmen.com"

        try:
            with engine.connect() as conn:
                rows = conn.execute(
                    sqlalchemy.text(
                        "SELECT location, phone, client_email, price, qty, details, created_at, link "
                        "FROM orders WHERE hostname = :host"
                    ),
                    {"host": hostname}
                ).fetchall()

            if rows:
                # Convert rows into a DataFrame with clickable links + thumbnails
                data = []
                for location, phone, client_email, price, qty, details, created_at, link in rows:
                    maps_url = f"https://www.google.com/maps?q={location}"
                    data.append({
                        "Location": f"[{location}]({maps_url})",
                        "Phone": phone,
                        "Client Email": client_email,
                        "Price": price,
                        "Qty": qty,
                        "Details": details,
                        "Created": created_at,
                        # Render image as small thumbnail
                        "Image": f'<img src="{link}" width="100">'
                    })

                df = pd.DataFrame(data)

                # Display table with clickable links and thumbnails
                st.write(df.to_html(escape=False), unsafe_allow_html=True)

            else:
                st.info("No orders found for this shop.")
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
    else:
        st.error("❌ Invalid shop name or password")
