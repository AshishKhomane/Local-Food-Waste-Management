import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load datasets
# -----------------------------
claims = pd.read_csv("claims_data.csv")
food_listings = pd.read_csv("food_listings_data.csv")
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")

# -----------------------------
# Streamlit App Title
# -----------------------------
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

st.title("🍽️ Local Food Wastage Management Dashboard")

# -----------------------------
# Show Available Columns
# -----------------------------
st.subheader("🔎 Available Columns in Each Dataset")

with st.expander("Claims Data Columns"):
    st.json(list(claims.columns))

with st.expander("Food Listings Data Columns"):
    st.json(list(food_listings.columns))

with st.expander("Providers Data Columns"):
    st.json(list(providers.columns))

with st.expander("Receivers Data Columns"):
    st.json(list(receivers.columns))

# -----------------------------
# Sidebar Options
# -----------------------------
st.sidebar.header("Options")
show_claims = st.sidebar.checkbox("Show Claims Data")
show_food = st.sidebar.checkbox("Show Food Listings")
show_providers = st.sidebar.checkbox("Show Providers")
show_receivers = st.sidebar.checkbox("Show Receivers")

# -----------------------------
# Claims Data
# -----------------------------
if show_claims:
    st.subheader("📑 Claims Data")
    st.dataframe(claims.head())

    if "Status" in claims.columns:
        status_counts = claims["Status"].value_counts()

        fig, ax = plt.subplots()
        status_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Claims by Status")
        ax.set_xlabel("Status")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Column 'Status' not found in claims_data.csv")

# -----------------------------
# Food Listings
# -----------------------------
if show_food:
    st.subheader("🥗 Food Listings Data")
    st.dataframe(food_listings.head())

    if "Food_Name" in food_listings.columns:
        food_counts = food_listings["Food_Name"].value_counts().head(10)

        fig, ax = plt.subplots()
        food_counts.plot(kind="bar", ax=ax, color="lightgreen")
        ax.set_title("Top 10 Food Items Listed")
        ax.set_xlabel("Food Item")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Column 'Food_Name' not found in food_listings_data.csv")

# -----------------------------
# Providers Data
# -----------------------------
if show_providers:
    st.subheader("🏢 Providers Data")
    st.dataframe(providers.head())

    if "City" in providers.columns:
        provider_counts = providers["City"].value_counts().head(10)

        fig, ax = plt.subplots()
        provider_counts.plot(kind="bar", ax=ax, color="orange")
        ax.set_title("Providers by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Column 'City' not found in providers_data.csv")

# -----------------------------
# Receivers Data
# -----------------------------
if show_receivers:
    st.subheader("🙋 Receivers Data")
    st.dataframe(receivers.head())

    if "City" in receivers.columns:
        receiver_counts = receivers["City"].value_counts().head(10)

        fig, ax = plt.subplots()
        receiver_counts.plot(kind="bar", ax=ax, color="purple")
        ax.set_title("Receivers by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Column 'City' not found in receivers_data.csv")

# -----------------------------
# End of App
# -----------------------------
st.markdown("---")
st.markdown("✅ Dashboard Ready - Local Food Wastage Management")
