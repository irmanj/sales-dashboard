import streamlit as st
import pandas as pd
from cleaning import clean_data

# ===== CONFIG =====
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")
st.caption("Insight otomatis dari data penjualan")

st.info("Upload file CSV untuk melihat dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = clean_data(uploaded_file)

        # ===== FILTER =====
        st.sidebar.header("🎛️ Filter")

        selected_kota = st.sidebar.multiselect(
            "Pilih Kota",
            options=df["Kota"].dropna().unique(),
            default=df["Kota"].dropna().unique()
        )

        df = df[df["Kota"].isin(selected_kota)]

        # ===== KPI =====
        total_sales = df["Sales"].sum()
        total_data = len(df)
        avg_sales = df["Sales"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Sales", f"Rp {total_sales:,.0f}")
        col2.metric("📦 Total Data", total_data)
        col3.metric("📊 Avg Sales", f"Rp {avg_sales:,.0f}")

        st.divider()

        # ===== INSIGHT =====
        st.subheader("🧠 Insight Otomatis")

        if not df.empty:
            top_kota = df.groupby("Kota")["Sales"].sum().idxmax()
            top_sales = df.groupby("Kota")["Sales"].sum().max()

            st.success(f"🏆 Kota dengan sales tertinggi: **{top_kota} (Rp {top_sales:,.0f})**")

        st.divider()

        # ===== TABLE =====
        st.subheader("📄 Cleaned Data")
        st.dataframe(df, use_container_width=True)

        # ===== CHART =====
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏙️ Sales per Kota")
            kota_sales = df.groupby("Kota")["Sales"].sum().sort_values(ascending=False)
            st.bar_chart(kota_sales)

        with col2:
            st.subheader("📈 Sales Trend")
            df_trend = df.dropna(subset=["Tanggal"])
            trend = df_trend.groupby(df_trend["Tanggal"].dt.to_period("M"))["Sales"].sum()
            trend.index = trend.index.astype(str)
            st.line_chart(trend)

        st.divider()

        # ===== DOWNLOAD =====
        st.subheader("📥 Download Data")

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Clean Data",
            data=csv,
            file_name="clean_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("Terjadi error saat memproses data 😢")
        st.text(str(e))