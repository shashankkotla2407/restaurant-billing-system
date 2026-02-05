import streamlit as st
import pandas as pd
import os

# 1) Page settings
st.set_page_config(page_title="Flavours of India", page_icon="🍽️", layout="wide")
st.title("🍽️ Flavours of India – Self Billing System")

# 2) Load CSV
menu_df = pd.read_csv("data/menu.csv")

# 3) Sidebar filters
st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(menu_df["category"].dropna().unique().tolist())
selected_cat = st.sidebar.selectbox("Category", categories)

sort_by = st.sidebar.selectbox("Sort By", ["Item Name (A-Z)", "Price Low → High", "Price High → Low"])

show_images = st.sidebar.checkbox("Show Images", value=True)

# 4) Filter by category
if selected_cat != "All":
    menu_df = menu_df[menu_df["category"] == selected_cat]

# 5) Sort
if sort_by == "Item Name (A-Z)":
    menu_df = menu_df.sort_values("item_name")
elif sort_by == "Price Low → High":
    menu_df = menu_df.sort_values("price")
else:
    menu_df = menu_df.sort_values("price", ascending=False)

st.subheader("🍽️ Menu Items")

# 6) Show items in a grid (3 per row)
cols = st.columns(3)

for i, row in enumerate(menu_df.itertuples(index=False)):
    with cols[i % 3]:
        # --- Image (optional) ---
        if show_images and "image" in menu_df.columns:
            img_path = os.path.join("assets", str(row.image))
            if os.path.exists(img_path):
                st.image(img_path, width=220, caption=None)
            else:
                # fallback if file not found
                default_path = os.path.join("assets", "default.jpg")
                if os.path.exists(default_path):
                    st.image(default_path, width=220, caption=None)

        # --- Item text ---
        st.markdown(f"**{row.item_name}**")
        st.write(f"₹ {row.price}")
        st.caption(f"{row.category}")

        # Placeholder button (we’ll connect cart tomorrow)
        st.button("Add", key=f"add_{row.item_id}")

        st.divider()
