import streamlit as st
import joblib
import pandas as pd

# Load model PROPERLY
model_data = joblib.load('car_model_enhanced.pkl')  # This is a dictionary
model = model_data['model']  # Extract the actual model

st.title("🚗 Car Price Prediction")

# Get brand options from model features
brand_options = [col.replace('brand_', '') 
                for col in model_data['features'] 
                if col.startswith('brand_')]

# User inputs
col1, col2 = st.columns(2)
with col1:
    car_age = st.slider("Car Age (Years)", 1, 20, 5)
with col2:
    brand = st.selectbox("Brand", brand_options)

if st.button("Predict Price"):
    # Prepare input with ALL features
    input_data = {col: 0 for col in model_data['features']}
    input_data['age'] = car_age
    input_data[f'brand_{brand}'] = 1
    
    # Convert to DataFrame with correct column order
    prediction_input = pd.DataFrame([input_data], columns=model_data['features'])
    
    prediction = model.predict(prediction_input)[0]
    st.success(f"Predicted Price: Rp {prediction:,.0f}")