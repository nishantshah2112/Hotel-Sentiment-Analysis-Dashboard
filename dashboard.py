import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_excel("Sentiment_Analysis_Output.xlsx")

st.set_page_config(page_title="Hotel Sentiment Dashboard", layout="wide")
st.title("🏨 Global Hotel Sentiment Dashboard")

# Sidebar Filters
city_filter = st.sidebar.multiselect(
    "Select City", options=df["City"].unique(), default=df["City"].unique()
)
filtered_df = df[df["City"].isin(city_filter)]

# KPI Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews Analyzed", len(filtered_df))
col2.metric("Average Sentiment Score", f"{filtered_df['Sentiment Score'].mean():.2f}")
col3.metric(
    "% Positive Reviews",
    f"{(len(filtered_df[filtered_df['Sentiment Category']=='Positive']) / len(filtered_df) * 100):.1f}%",
)

# Charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sentiment Distribution")
    fig_pie = px.pie(
        filtered_df,
        names="Sentiment Category",
        color="Sentiment Category",
        color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"},
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("Top Hotels by Sentiment")
    # Group by hotel and get mean score
    top_hotels = (
        filtered_df.groupby("Hotel Name")["Sentiment Score"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig_bar = px.bar(
        top_hotels,
        x="Sentiment Score",
        y="Hotel Name",
        orientation="h",
        color="Sentiment Score",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Review Data")
st.dataframe(filtered_df)
