import streamlit as st
import joblib
import pandas as pd

model_data = joblib.load('car_model_enhanced.pkl') 
model = model_data['model']  # Extract the actual model

st.title("🚗 Car Price Prediction")

brand_options = [col.replace('brand_', '') 
                for col in model_data['features'] 
                if col.startswith('brand_')]

col1, col2 = st.columns(2)
with col1:
    car_age = st.slider("Car Age (Years)", 1, 20, 5)
with col2:
    brand = st.selectbox("Brand", brand_options)

if st.button("Predict Price"):
    input_data = {col: 0 for col in model_data['features']}
    input_data['age'] = car_age
    input_data[f'brand_{brand}'] = 1
    
    prediction_input = pd.DataFrame([input_data], columns=model_data['features'])
    
    prediction = model.predict(prediction_input)[0]
    st.success(f"Predicted Price: Rp {prediction:,.0f}")