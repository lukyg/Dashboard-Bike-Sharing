import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Dashboard Penyewaan Sepeda")
st.sidebar.header("🎚️ Filter Data")


data = pd.read_csv("main_data.csv")

# Mapping bulan ke musim untuk filter
season_months = {
    "spring": ["december", "january", "february", "march"],
    "summer": ["april", "may", "june"],
    "fall": ["july", "august", "september"],
    "winter": ["october", "november"],
}

season_order = ["spring", "summer", "fall", "winter"]

selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(data["year_mapped"].unique()))
selected_season = st.sidebar.selectbox("Pilih Musim", season_order)

# Menampilkan hanya bulan yang sesuai dengan musim
available_months = season_months[selected_season]
selected_month = st.sidebar.selectbox("Pilih Bulan", available_months)

# Filter Data
filtered_data = data[
    (data["year_mapped"] == selected_year) & 
    (data["month_mapped"] == selected_month) & 
    (data["season_mapped"] == selected_season)
]

# Scorecards
st.subheader("Jumlah Penyewa")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Casual Users", value=int(filtered_data["casual"].sum()))
    with col2:
        st.metric(label="Registered Users", value=int(filtered_data["registered"].sum()))
    with col3:
        st.metric(label="Total Rentals", value=int(filtered_data["casual"].sum() + filtered_data["registered"].sum()))

st.markdown("---")

# Visualisasi piechart dan barchart
col1, col2 = st.columns(2)

with col1:
    # Piechart untuk jumalah penyewa
    st.subheader("Statistik Penyewaan Sepeda")

    labels = ["Casual Users", "Registered Users"]
    values = [filtered_data["casual"].sum(), filtered_data["registered"].sum()]
    colors = ["#A8DADC", "#457B9D"] 

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})
    ax.set_title("Distribusi Penyewaan Sepeda")

    st.pyplot(fig)

with col2:
    # Barchart untuk pengaruh musim
    st.subheader("Pengaruh Musim Terhadap Penyewa")
    with st.container():
        seasonal_pattern = filtered_data.groupby("season_mapped")[['casual', 'registered']].mean().reset_index()
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        sns.barplot(data=seasonal_pattern.melt(id_vars="season_mapped", var_name="Tipe Penyewa", value_name="Jumlah Penyewa"),
                    x="season_mapped", y="Jumlah Penyewa", hue="Tipe Penyewa", 
                    palette={"casual": "#A8DADC", "registered": "#457B9D"}, order=season_order)
        ax3.set_xlabel("Musim")
        ax3.set_ylabel("Rata-rata Penyewa")
        ax3.set_title("Pengaruh Musim terhadap Penyewaan Sepeda")
        st.pyplot(fig3)

st.markdown("---")

# Grafik Pola penyewaan sepeda berdasarkan hari kerja
st.subheader("Pola Penyewaan Sepeda pada Hari Kerja vs Hari Libur")
with st.container():
    hourly_pattern = filtered_data.groupby(["is_working_day_mapped", "hour"])[["casual", "registered"]].mean().reset_index()
    fig2, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Casual
    sns.lineplot(ax=axes[0], data=hourly_pattern, x="hour", y="casual", hue="is_working_day_mapped", 
                 palette=["#A8DADC", "#457B9D"]) 
    axes[0].set_title("Casual (Hari Kerja vs Hari Libur)")
    axes[0].set_xlabel("Jam dalam Sehari")
    axes[0].set_ylabel("Rata-rata Penyewa")
    axes[0].set_yticks(range(0, 500, 50))
    axes[0].grid(True)

    # Registered
    sns.lineplot(ax=axes[1], data=hourly_pattern, x="hour", y="registered", hue="is_working_day_mapped", 
                 palette=["#A8DADC", "#457B9D"]) 
    axes[1].set_title("Registered (Hari Kerja vs Hari Libur)")
    axes[1].set_xlabel("Jam dalam Sehari")
    axes[1].set_ylabel("Rata-rata Penyewa")
    axes[1].set_yticks(range(0, 500, 50))
    axes[1].grid(True)

    st.pyplot(fig2)

st.markdown("---")