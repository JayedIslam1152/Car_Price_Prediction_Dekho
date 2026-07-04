import streamlit as st
import pandas as pd
import joblib
from datetime import datetime


# Configuration
EXCHANGE_RATE = 1.42

st.set_page_config(
    page_title="Car Selling Price Prediction System",
    page_icon="🚗",
    layout="centered"
)


# Load Model
model = joblib.load("used_car_price_prediction_model.pkl")


# Load Dataset
df = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")

# Create Brand Column
df["brand"] = df["name"].str.split().str[0]


# Sidebar
st.sidebar.title("📋 Project Information")

st.sidebar.markdown("""
### 🚗 Used Car Price Prediction

**Model**
- LinearRegression

**Dataset**
- CarDekho Vehicle Dataset

**Framework**
- Streamlit

### Instructions

1. Select Car Model
2. Select Brand
3. Select Fuel Type
4. Select Seller Type
5. Select Transmission
6. Select Owner Type
7. Enter Car Age
8. Enter Kilometers Driven
9. Click Predict Price
""")


# Title
st.markdown(
    "<h1 style='text-align:center;'> Car Selling Price Prediction System</h1>",
    unsafe_allow_html=True
)

st.write("")


# Inputs

car_model = st.selectbox(
    "Car Model",
    sorted(df["name"].unique())
)

brand = st.selectbox(
    "Brand",
    sorted(df["brand"].dropna().unique())
)

fuel = st.selectbox(
    "Fuel Type",
    sorted(df["fuel"].dropna().unique())
)

seller_type = st.selectbox(
    "Seller Type",
    sorted(df["seller_type"].dropna().unique())
)

transmission = st.selectbox(
    "Transmission",
    sorted(df["transmission"].dropna().unique())
)

owner = st.selectbox(
    "Owner",
    sorted(df["owner"].dropna().unique())
)

car_age = st.number_input(
    "Car Age (Years)",
    min_value=0,
    max_value=30,
    value=5
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000,
    step=1000
)


# Prediction

if st.button("Predict Price"):

    try:

        actual_brand = df[df["name"] == car_model]["brand"].iloc[0]

        if brand != actual_brand:
            st.error("❌ Invalid Selection! The selected Brand does not match the selected Car Model.")
            st.stop()


        input_df = pd.DataFrame({

        "name": [car_model],
        "brand": [brand],
        "fuel": [fuel],
        "seller_type": [seller_type],
        "transmission": [transmission],
        "owner": [owner],
        "km_driven": [km_driven],
        "car_age": [car_age]

        })

        prediction = model.predict(input_df)[0]

        prediction_bdt = prediction * EXCHANGE_RATE

        st.success("Prediction Successful ✅")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Selling Price (INR)",
                f"₹ {prediction:,.0f}"
            )

        with col2:
            st.metric(
                "Selling Price (BDT)",
                f"৳ {prediction_bdt:,.0f}"
            )

    except Exception as e:
        st.error(f"Prediction Failed!\n\n{e}")