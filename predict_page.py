import streamlit as st
import numpy as np
import pickle


def load_model():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    countries = (
        'United Kingdom of Great Britain and Northern Ireland',
        'Netherlands',
        'United States of America',
        'Italy',
        'Canada',
        'Germany',
        'Poland',
        'France',
        'Brazil',
        'Sweden',
        'Spain',
        'India',
        'Switzerland',
        'Australia',
        'Russian Federation'
)

    education = (
    "Master's degree",
    "Bachelor's degree",
    'Less than a Bachelors',
    'Post grad'
)

    country = st.selectbox("Country", countries)
    education = st.selectbox("Level of Education", education)

    experience = st.slider("Years of Experience", 0, 50, 3)

    calculate_btn = st.button("Calculate Salary")
    if calculate_btn:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)

        st.subheader(f"The estimated salary is ${salary[0]:.2f}")