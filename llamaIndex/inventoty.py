import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "inventory_data.csv"

# Load or initialize the inventory data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Item ID", "Item Name", "Category", "Quantity", "Unit Price", "Last Updated"])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_item(df, item_id, name, category, quantity, price):
    if item_id in df["Item ID"].values:
        st.warning("Item ID already exists.")
        return df
    new_item = pd.DataFrame([[item_id, name, category, quantity, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                            columns=df.columns)
    return pd.concat([df, new_item], ignore_index=True)

def update_item(df, item_id, quantity=None, price=None):
    if item_id not in df["Item ID"].values:
        st.error("Item ID not found.")
        return df
    idx = df[df["Item ID"] == item_id].index[0]
    if quantity is not None:
        df.at[idx, "Quantity"] = quantity
    if price is not None:
        df.at[idx, "Unit Price"] = price
    df.at[idx, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df

def delete_item(df, item_id):
    if item_id not in df["Item ID"].values:
        st.error("Item ID not found.")
        return df
    df = df[df["Item ID"] != item_id]
    return df

def main():
    st.set_page_config(page_title="Inventory Management App", layout="wide")
    st.title("📦 Inventory Management App")

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Inventory", "➕ Add Item", "✏️ Update/Delete", "📊 Analytics"])

    with tab1:
        st.subheader("Current Inventory")
        search = st.text_input("Search by Item Name or Category")
        filtered_df = df[df["Item Name"].str.contains(search, case=False, na=False) | df["Category"].str.contains(search, case=False, na=False)]
        st.dataframe(filtered_df.sort_values("Item Name"))

    with tab2:
        st.subheader("Add New Item")
        with st.form("add_form"):
            item_id = st.text_input("Item ID")
            name = st.text_input("Item Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Unit Price", min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Add Item")
            if submitted:
                df = add_item(df, item_id, name, category, quantity, price)
                save_data(df)
                st.success("Item added successfully!")

    with tab3:
        st.subheader("Update or Delete Item")
        item_id = st.selectbox("Select Item ID to Update/Delete", options=df["Item ID"].unique())
        selected = df[df["Item ID"] == item_id].iloc[0]
        new_quantity = st.number_input("New Quantity", min_value=0, value=int(selected["Quantity"]))
        new_price = st.number_input("New Unit Price", min_value=0.0, value=float(selected["Unit Price"]))
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Item"):
                df = update_item(df, item_id, new_quantity, new_price)
                save_data(df)
                st.success("Item updated successfully!")
        with col2:
            if st.button("Delete Item"):
                df = delete_item(df, item_id)
                save_data(df)
                st.success("Item deleted successfully!")

    with tab4:
        st.subheader("Inventory Analytics")
        if df.empty:
            st.info("No data to show.")
        else:
            total_items = df["Item ID"].nunique()
            total_quantity = df["Quantity"].sum()
            total_value = (df["Quantity"] * df["Unit Price"]).sum()

            st.metric("Total Unique Items", total_items)
            st.metric("Total Quantity in Stock", total_quantity)
            st.metric("Total Inventory Value ($)", f"{total_value:,.2f}")

            st.bar_chart(df.groupby("Category")["Quantity"].sum())

if __name__ == "__main__":
    main()
