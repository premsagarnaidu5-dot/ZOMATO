import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

st.title("Zomato Restaurant Analysis")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Live.csv")

    # Drop unnecessary columns
    df = df.drop([
        'url','online_order','book_table','phone','rest_type','dish_liked',
        'reviews_list','menu_item','listed_in(type)','listed_in(city)','address'
    ], axis=1)

    # Rename & clean cost column
    df = df.rename(columns={'approx_cost(for two people)': 'approx_cost'})
    df = df.fillna(0)
    df['approx_cost'] = df['approx_cost'].replace('[,]', '', regex=True).astype("int64")

    # Clean rate column
    df['rate'] = df['rate'].replace('[/5]', '', regex=True)
    df['rate'] = df['rate'].replace('NEW', 0)
    df['rate'] = df['rate'].replace('-', 0).astype("float64")

    return df

df = load_data()

# --- Sidebar Selection ---
st.sidebar.header("Select Options")

locations = sorted(df['location'].unique())
selected_location = st.sidebar.selectbox("Choose Location", locations)

# Filter by location
lo = df[df['location'] == selected_location]

# --- Grouping and selecting top 10 ---
gr = lo.groupby('name')[['rate', 'approx_cost']].mean().nlargest(10, 'rate').reset_index()

st.subheader(f"Top 10 Restaurants in {selected_location} by Rating")

# --- Plotting ---
fig, ax = plt.subplots(figsize=(20, 8))
sb.barplot(data=gr, x='name', y='approx_cost', palette='summer', ax=ax)
plt.xticks(rotation=90)
plt.xlabel("Restaurant Name")
plt.ylabel("Average Cost for Two")
plt.tight_layout()

st.pyplot(fig)

# Show data table
st.subheader("Data Table for Selected Restaurants")
st.dataframe(gr)
