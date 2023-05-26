import streamlit as st
import squarify
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor" in x:
        return "Bachelor's degree"
    elif "Master" in x:
        return "Master's degree"
    elif "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    else:
        return "Less than a Bachelors"

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 800000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2022""")

    data = df["Country"].value_counts()

    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    labels = data.index

    label_tag = []


    for label in labels:
        tag = label[:3].upper()
        label_tag.append(tag)
    label_tag[0] = "USA"
    label_tag[2] = "UK & IRE"

    color_codes = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'grey', '#FFA500', '#800080', '#00FF00', '#008080', '#FF00FF',
                   '#FFFF00', '#A52A2A']

    squarify.plot(sizes=data, pad=0.5, color=color_codes, text_kwargs={'fontsize': 10, 'color': 'white'}, label=label_tag)

    st.write("""#### Number of Data from Different Countries""")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.axis("off")
    st.pyplot()

    st.write("""#### The Mean Salary by Country""")

    data = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### The Mean Salary by Country""")
    data = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)