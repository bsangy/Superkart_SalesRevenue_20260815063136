import streamlit as st
import pandas as pd
import requests

BACKEND_URL="http://backend:7860"
# Streamlit UI for Boston Housing Price Prediction
st.title("BWelcome to the Superkart Sales Revenue prediction  App")
st.write("This app predicts Product  Store sales for each prodcut and store based on Superkart dataset features.")
st.write("Move the sliders below to adjust values and get a prediction.")

# Collect user input using Super kart
Product_Weight = st.slider(" Weight of each product", 4.00, 22.00, 4.00,0.01)
Product_Sugar_Content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Allocated Area of each product")
Product_Type = st.selectbox("Type of product", ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene',
 'Snack Foods', 'Meat', 'Household', 'Hard Drinks', 'Fruits and Vegetables',
 'Breads', 'Soft Drinks' ,'Breakfast', 'Others', 'Starchy Foods', 'Seafood'])
#PRODUCT_MRP = st.text_input("MRP of each product", 31.00, 266.00, 31.00, 0.01)
Product_MRP = st.number_input("MRP of each product", 31.00, 266.00, 31.00, 0.01)
Store_Id = st.selectbox("Unique identifier of each store", ['OUT004', 'OUT003' ,'OUT001' ,'OUT002'])
Store_Size= st.selectbox("Size of the store, depending on sq. feet, ", ['High', 'Medium' ,'Small'])
Store_Location_City_Type = st.selectbox("Type of city in which the store is located", ['Tier 2', 'Tier 1' ,'Tier 3'])
Store_Type = st.selectbox("Type of store depending on the products ", ['Supermarket Type2' ,'Departmental Store', 'Supermarket Type1', 'Food Mart'])
Product_ID_Tag = st.text_input("Unique identifier of each product")
Product_Store_Age = st.slider("age of storeestablished", 0, 50, 9, 1)




# Create input DataFrame
input_data = {

        'Product_Weight': Product_Weight,
        'Product_Sugar_Content': Product_Sugar_Content,
        'Product_Allocated_Area': Product_Allocated_Area,
        'Product_Type': Product_Type,
        'Product_MRP': Product_MRP,
        'Store_Id': Store_Id,
        'Store_Size':Store_Size,
        'Store_Location_City_Type': Store_Location_City_Type,
        'Store_Type': Store_Type,
        'Product_ID_Tag': Product_ID_Tag,
        'Product_Store_Age': Product_Store_Age
}

if st.button("Predict", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/Product_Storesales", json=input_data)    # this will be online and instant output
    if response.status_code == 200:
        result = response.json()
        predicted_price = result["' Predicted_ProductStoresSales"]
        st.success(f"Predicted Prodcut Store sale Value: **${predicted_price * 1:.2f}**")
    else:
        st.error("Error in API request")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post("f{BACKEND_URL}/v1/Product_Storesales_batch", files={"file": file})
        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
