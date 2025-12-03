import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.title("Zomato Restaurant Cost Analysis")

# Load data
df = pd.read_csv("../Datasets/zomato.csv")

# Show unique locations
st.write("### Available Locations:")
st.write(df.location.unique())

# Streamlit input instead of console input()
l = st.text_input("Enter Location Name:")

if l:
    # Filter by location
    lo = df[df.location == l]

    # Check if location exists
    if lo.empty:
        st.error("No restaurants found for this location.")
    else:
        # Group and find top 10 restaurants by rating
        gr = lo.groupby('name')[['rate','approx_cost']].mean().nlargest(10, 'rate').reset_index()

        # Plot
        fig = plt.figure(figsize=(20, 8))
        sb.barplot(x=gr.name, y=gr.approx_cost, palette='summer')
        plt.xticks(rotation=90)
        plt.xlabel("Restaurant Name")
        plt.ylabel("Average Cost for Two")
        plt.title(f"Top 10 Restaurants in {l} by Rating")

        st.pyplot(fig)

        # Show table
        st.write("### Data Table")
        st.dataframe(gr)
