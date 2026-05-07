import streamlit as st
from cleaning import clean_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Coffee Shop Analytics",
    page_icon="☕",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = clean_data()

# =========================
# HEADER
# =========================
st.title("☕ Coffee Shop Analytics Dashboard")
st.caption("Insight otomatis dari data penjualan")

st.divider()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🎛️ Filter Dashboard")

selected_kota = st.sidebar.multiselect(
    "Pilih Kota",
    options=df["Kota"].unique(),
    default=df["Kota"].unique()
)

selected_produk = st.sidebar.multiselect(
    "Pilih Produk",
    options=df["Produk"].unique(),
    default=df["Produk"].unique()
)

# filter data
filtered_df = df[
    (df["Kota"].isin(selected_kota)) &
    (df["Produk"].isin(selected_produk))
]

# =========================
# KPI
# =========================
total_sales = filtered_df["Sales"].sum()
avg_sales = filtered_df["Sales"].mean()
top_produk = filtered_df.groupby("Produk")["Sales"].sum().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Sales",
    f"Rp {total_sales:,.0f}"
)

col2.metric(
    "📊 Avg Sales",
    f"Rp {avg_sales:,.0f}"
)

col3.metric(
    "🔥 Top Product",
    top_produk
)

st.divider()

# =========================
# CHARTS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Sales per Kota")
    kota_chart = filtered_df.groupby("Kota")["Sales"].sum()
    st.bar_chart(kota_chart)

with col2:
    st.subheader("☕ Sales per Produk")
    produk_chart = filtered_df.groupby("Produk")["Sales"].sum()
    st.bar_chart(produk_chart)

st.divider()

# =========================
# SALES TREND
# =========================
st.subheader("📈 Sales Trend")

trend = filtered_df.groupby("Tanggal")["Sales"].sum()
st.line_chart(trend)

st.divider()

# =========================
# INSIGHT
# =========================
st.subheader("🧠 Insight Otomatis")

top_kota = filtered_df.groupby("Kota")["Sales"].sum().idxmax()

st.success(
    f"""
    📍 Kota dengan penjualan tertinggi: {top_kota}

    ☕ Produk paling laku: {top_produk}

    💰 Total penjualan: Rp {total_sales:,.0f}
    """
)

st.divider()

# =========================
# TABLE
# =========================
st.subheader("📄 Cleaned Data")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Cleaned Data",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)