import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="Local Food Waste Management", layout="wide")

# Load data
@st.cache_data
def load_data():
    claims = pd.read_csv("claims_data.csv")
    food_listings = pd.read_csv("food_listings_data.csv")
    providers = pd.read_csv("providers_data.csv")
    receivers = pd.read_csv("receivers_data.csv")
    return claims, food_listings, providers, receivers

claims, food_listings, providers, receivers = load_data()

st.title("🍽️ Local Food Waste Management Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

# Filter 1: Claim Status
claim_status_filter = st.sidebar.multiselect(
    "Select Claim Status:",
    options=claims["Status"].unique(),
    default=claims["Status"].unique()
)

# Filter 2: Food Type
food_type_filter = st.sidebar.multiselect(
    "Select Food Type:",
    options=food_listings["Food_Type"].unique(),
    default=food_listings["Food_Type"].unique()
)

# Filter 3: Provider City
provider_city_filter = st.sidebar.multiselect(
    "Select Provider City:",
    options=providers["City"].unique(),
    default=providers["City"].unique()
)

# Filter 4: Receiver City
receiver_city_filter = st.sidebar.multiselect(
    "Select Receiver City:",
    options=receivers["City"].unique(),
    default=receivers["City"].unique()
)

# --- Apply Filters ---
claims = claims[claims["Status"].isin(claim_status_filter)]
food_listings = food_listings[food_listings["Food_Type"].isin(food_type_filter)]
providers = providers[providers["City"].isin(provider_city_filter)]
receivers = receivers[receivers["City"].isin(receiver_city_filter)]

# =============================
# 🔥 KPI Section
# =============================
st.markdown("## 📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Claims", claims["Claim_ID"].nunique())

with col2:
    st.metric("Total Food Quantity", int(food_listings["Quantity"].sum()))

with col3:
    st.metric("Active Providers", providers["Provider_ID"].nunique())

with col4:
    st.metric("Active Receivers", receivers["Receiver_ID"].nunique())

# =============================
# 📊 Charts & Insights
# =============================

# --- Section 1: Claims Overview ---
st.header("📌 Claims Overview")
claim_status = claims.groupby("Status")["Claim_ID"].count().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=claim_status, x="Status", y="Claim_ID", ax=ax, palette="viridis")
ax.set_title("Claims by Status")
ax.set_ylabel("Number of Claims")
st.pyplot(fig)

# --- Section 2: Food Listings ---
st.header("🥗 Food Listings by Type")
food_type = food_listings.groupby("Food_Type")["Food_ID"].count().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=food_type, x="Food_Type", y="Food_ID", ax=ax, palette="magma")
ax.set_title("Food Listings by Type")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- Section 3: Providers ---
st.header("🚚 Top Providers")
top_providers = food_listings.groupby("Provider_ID")["Quantity"].sum().reset_index()
top_providers = top_providers.merge(providers, on="Provider_ID").sort_values(by="Quantity", ascending=False).head(10)

fig, ax = plt.subplots()
sns.barplot(data=top_providers, x="Quantity", y="Name", ax=ax, palette="coolwarm")
ax.set_title("Top Providers by Quantity Supplied")
st.pyplot(fig)

# --- Section 4: Receivers ---
st.header("🏙️ Top Receiver Cities")
top_receivers = claims.groupby("Receiver_ID")["Claim_ID"].count().reset_index()
top_receivers = top_receivers.merge(receivers, on="Receiver_ID").groupby("City")["Claim_ID"].sum().reset_index().sort_values(by="Claim_ID", ascending=False).head(10)

fig, ax = plt.subplots()
sns.barplot(data=top_receivers, x="Claim_ID", y="City", ax=ax, palette="crest")
ax.set_title("Top Receiver Cities by Claims")
ax.set_xlabel("Number of Claims")
st.pyplot(fig)

# =============================
# 📄 Raw Data Section
# =============================
st.header("📂 Raw Data")
option = st.selectbox("Select a dataset to view:", ("Claims", "Food Listings", "Providers", "Receivers"))

if option == "Claims":
    st.dataframe(claims.head(50))
elif option == "Food Listings":
    st.dataframe(food_listings.head(50))
elif option == "Providers":
    st.dataframe(providers.head(50))
else:
    st.dataframe(receivers.head(50))
