import streamlit as st
import sqlalchemy

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
                    sqlalchemy.text("SELECT location, phone, client_email, price, qty, details,created_at,image_url FROM orders WHERE hostname = :host"),
                    {"host": hostname}
                ).fetchall()

            if rows:
                st.markdown("### Orders")

                for location, phone, client_email, price,qty,details, created_at, image_url in rows:
                    # Make location clickable
                    maps_url = f"https://www.google.com/maps?q={location}"
                    
                    st.write(f"**Location:** [{location}]({maps_url})")
                    st.write(f"**Phone:** {phone}")
                    st.write(f"**client_email:** {client_email}")
                    st.write(f"**Confirmed:** {price}")
                    st.write(f"**qty:** {qty}")
                    st.write(f"**details:** {details}")
                    st.write(f"**Created:** {created_at}")

                    # Display image if available
                    if image_url:
                        st.image(image_url, caption="Order Image", use_column_width=True)

                    st.markdown("---")  # separator between orders
            else:
                st.info("No orders found for this shop.")
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
    else:
        st.error("❌ Invalid shop name or password")
