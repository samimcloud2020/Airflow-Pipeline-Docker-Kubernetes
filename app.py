import streamlit as st
import joblib
import pandas as pd

# Load the model
MODEL_PATH = "/app/models/iris_logistic_model.pkl"
model = joblib.load(MODEL_PATH)
class_names = ['Setosa', 'Versicolor', 'Virginica']

# Streamlit UI
st.title("Iris Flower Classification")
st.write("Enter the Iris flower measurements to predict its class.")

# Input fields
sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, max_value=10.0, value=5.1)
sepal_width = st.number_input("Sepal Width (cm)", min_value=0.0, max_value=10.0, value=3.5)
petal_length = st.number_input("Petal Length (cm)", min_value=0.0, max_value=10.0, value=1.4)
petal_width = st.number_input("Petal Width (cm)", min_value=0.0, max_value=10.0, value=0.2)

# Predict button
if st.button("Predict"):
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(input_data)[0]
    predicted_class = class_names[prediction]
    st.success(f"Predicted Class: **{predicted_class}**")