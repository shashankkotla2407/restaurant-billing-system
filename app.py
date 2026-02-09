import streamlit as st
import pandas as pd
import os

from src.menu import Menu
from src.order import Order
from src.bill import Bill

# ---------------- Page Settings ----------------
st.set_page_config(page_title="Flavours of India", page_icon="🍽️", layout="wide")
st.title("🍽️ Flavours of India – Self Billing System")

# ---------------- Load Menu CSV ----------------
menu_df = pd.read_csv("data/menu.csv")

# ---------------- Create OOPS Objects ----------------
menu = Menu(menu_df)

if "order" not in st.session_state:
    st.session_state.order = Order()
order = st.session_state.order

bill = Bill(tax_rate=0.05)

# ---- Bill display state ----
if "show_bill" not in st.session_state:
    st.session_state.show_bill = False
if "bill_text" not in st.session_state:
    st.session_state.bill_text = ""
if "confirm_order" not in st.session_state:
    st.session_state.confirm_order = False

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔎 Filters")

categories = menu.get_categories()
selected_cat = st.sidebar.selectbox("Category", categories)

sort_by = st.sidebar.selectbox(
    "Sort By",
    ["Item Name (A-Z)", "Price Low → High", "Price High → Low"]
)

show_images = st.sidebar.checkbox("Show Images", value=True)

# ---------------- Filter + Sort Menu ----------------
filtered_df = menu.filter_by_category(selected_cat)

if sort_by == "Item Name (A-Z)":
    filtered_df = filtered_df.sort_values("item_name")
elif sort_by == "Price Low → High":
    filtered_df = filtered_df.sort_values("price")
else:
    filtered_df = filtered_df.sort_values("price", ascending=False)

# ---------------- Display Menu ----------------
st.subheader("🍽️ Menu Items")

cols = st.columns(3)

for i, row in enumerate(filtered_df.itertuples(index=False)):
    with cols[i % 3]:
        # Image (optional)
        if show_images and "image" in filtered_df.columns:
            img_path = os.path.join("assets", str(row.image))
            if os.path.exists(img_path):
                st.image(img_path, width=220)
            else:
                st.image(os.path.join("assets", "default.jpg"), width=220)

        # Item details
        st.markdown(f"**{row.item_name}**")
        st.write(f"₹ {row.price}")
        st.caption(row.category)

        # Add to cart
        if st.button("Add", key=f"add_{row.item_id}"):
            order.add_item(int(row.item_id), row.item_name, float(row.price))
            st.success(f"{row.item_name} added to cart")

        st.divider()

# ---------------- Cart Section ----------------
st.markdown("---")
st.subheader("🛒 Cart")

if order.is_empty():
    st.info("Cart is empty. Add items from the menu.")
else:
    cart_items = order.get_cart_items()

    st.write("Change quantity (auto updates). Set Qty = 0 to remove an item.")

    # ---- Quantity controls (auto update) ----
    for item in cart_items:
        c1, c2, c3, c4 = st.columns([4, 2, 2, 2])

        with c1:
            st.write(item["item_name"])

        with c2:
            st.write(f"₹ {item['price']}")

        with c3:
            new_qty = st.number_input(
                "Qty",
                min_value=0,
                step=1,
                value=int(item["quantity"]),
                key=f"qty_{item['item_id']}",
                label_visibility="collapsed"
            )
            order.set_quantity(item["item_id"], int(new_qty))

        with c4:
            st.write(f"₹ {item['price'] * int(new_qty):.2f}")

    # ---- Remove single item (dropdown) ----
    st.subheader("🗑️ Remove an Item")
    cart_items_after = order.get_cart_items()

    if len(cart_items_after) == 0:
        st.info("No items to remove.")
    else:
        item_options = [f"{x['item_name']} (ID: {x['item_id']})" for x in cart_items_after]
        selected_option = st.selectbox("Select item to remove", item_options)

        if st.button("Remove Selected Item"):
            selected_id = int(selected_option.split("ID: ")[1].replace(")", ""))
            order.remove_item(selected_id)
            st.success("Item removed ✅")
            st.rerun()

    # ---- Final Total with Tax ----
    subtotal = order.get_subtotal()
    tax = bill.calculate_tax(subtotal)
    final_total = bill.calculate_total(subtotal)

    st.subheader(f"💰 Final Total: ₹ {final_total:.2f}")
    st.caption(f"Includes Tax (5%): ₹ {tax:.2f}")

    # ---- Place Order + Confirmation ----
    st.subheader("✅ Place Order")

    if st.button("Place Order"):
        st.session_state.confirm_order = True

    if st.session_state.confirm_order:
        st.warning("Are you sure you want to place this order?")
        c_yes, c_no = st.columns(2)

        with c_yes:
            if st.button("Yes, Confirm Order"):
                # Build bill text
                final_cart = order.get_cart_items()

                lines = []
                lines.append("🍽️ Flavours of India - BILL")
                lines.append("----------------------------------")

                for x in final_cart:
                    lines.append(f"{x['item_name']}  x{x['quantity']}  = ₹{x['total']:.2f}")

                lines.append("----------------------------------")
                lines.append(f"Subtotal: ₹{subtotal:.2f}")
                lines.append(f"Tax (5%): ₹{tax:.2f}")
                lines.append(f"Final Total: ₹{final_total:.2f}")
                lines.append("----------------------------------")

                st.session_state.bill_text = "\n".join(lines)
                st.session_state.show_bill = True
                st.session_state.confirm_order = False

                # Clear cart after order confirm (kiosk style)
                order.clear_cart()

                st.success("✅ Order placed! Bill generated below.")
                st.rerun()

        with c_no:
            if st.button("No, Cancel"):
                st.session_state.confirm_order = False
                st.info("Order cancelled.")

    # ---- Clear full cart ----
    if st.button("Clear Cart"):
        order.clear_cart()
        st.success("Cart cleared successfully")
        st.rerun()

# ---------------- Bill Display (Below on same page) ----------------
if st.session_state.show_bill:
    st.markdown("---")
    st.subheader("🧾 Final Bill")
    st.code(st.session_state.bill_text)

    if st.button("New Order"):
        st.session_state.show_bill = False
        st.session_state.bill_text = ""
        st.success("Ready for new order ✅")
        st.rerun()
