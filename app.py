import streamlit as st
import pandas as pd
from cleaning import clean_data
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Dashboard")
st.caption("Dashboard analisis penjualan sederhana")

st.info("Upload file CSV untuk melihat dashboard")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = clean_data(uploaded_file)

        st.sidebar.header("Filter")

        selected_kota = st.sidebar.multiselect(
            "Pilih Kota",
            options=df["Kota"].unique(),
            default=df["Kota"].unique()
        )

        df = df[df["Kota"].isin(selected_kota)]

        # ===== KPI =====
        total_sales = df["Sales"].sum()
        total_data = len(df)

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Sales", f"Rp {total_sales:,.0f}")
        col2.metric("📦 Total Data", total_data)

        st.divider()

        # ===== TABLE =====
        st.subheader("📄 Cleaned Data")
        st.dataframe(df, use_container_width=True)

        # ===== SALES PER KOTA =====
        st.subheader("🏙️ Sales per Kota")
        kota_sales = df.groupby("Kota")["Sales"].sum().sort_values(ascending=False)
        st.bar_chart(kota_sales)

        # ===== TREND =====
        st.subheader("📈 Sales Trend")
        df = df.dropna(subset=["Tanggal"])
        trend = df.groupby(df["Tanggal"].dt.to_period("M"))["Sales"].sum()
        trend.index = trend.index.astype(str)
        st.line_chart(trend)

    except Exception as e:
        st.error("Terjadi error saat memproses data 😢")
        st.text(str(e))

else:
    st.info("Silakan upload file CSV untuk mulai")