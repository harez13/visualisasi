import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("clean_data.csv")
df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True, errors='coerce')
df['tahun'] = df['tanggal'].dt.year
df['bulan'] = df['tanggal'].dt.month

# Judul utama
st.title("📊 Dashboard Kualitas Udara Jakarta 2024")

# Sidebar navigasi
option = st.sidebar.selectbox(
    "Pilih Visualisasi:",
    (
        "1. Korelasi Antar Parameter Pencemar",
        "2. Rata-Rata Bulanan Parameter Pencemar",
        "3. Distribusi Kategori Kualitas Udara per Stasiun",
        "4. Frekuensi Parameter Pencemar Kritis per Stasiun",
        "5. Tren Harian PM2.5 per Stasiun"
    )
)

# List parameter pencemar
pollutants = ['pm_sepuluh', 'pm_duakomalima', 'sulfur_dioksida',
              'karbon_monoksida', 'ozon', 'nitrogen_dioksida']

# --- Visualisasi 1 ---
if option == "1. Korelasi Antar Parameter Pencemar":
    st.subheader("🔗 Korelasi Antar Parameter Pencemar")
    corr_matrix = df[pollutants].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=ax)
    st.pyplot(fig)

# --- Visualisasi 2 ---
elif option == "2. Rata-Rata Bulanan Parameter Pencemar":
    st.subheader("📆 Rata-Rata Bulanan Parameter Pencemar")
    pollutant_month = df.groupby("bulan")[pollutants].mean().T
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pollutant_month, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Parameter")
    st.pyplot(fig)

# --- Visualisasi 3 ---
elif option == "3. Distribusi Kategori Kualitas Udara per Stasiun":
    st.subheader("🏙️ Distribusi Kategori Kualitas Udara per Stasiun")
    kategori_matrix = df.groupby(["stasiun", "kategori"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(kategori_matrix, annot=True, cmap="Blues", fmt="d", ax=ax)
    st.pyplot(fig)

# --- Visualisasi 4 ---
elif option == "4. Frekuensi Parameter Pencemar Kritis per Stasiun":
    st.subheader("⚠️ Frekuensi Parameter Pencemar Kritis per Stasiun")
    critical_matrix = df.groupby(["stasiun", "parameter_pencemar_kritis"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(critical_matrix, annot=True, cmap="Oranges", fmt="d", ax=ax)
    st.pyplot(fig)

# --- Visualisasi 5 ---
elif option == "5. Tren Harian PM2.5 per Stasiun":
    st.subheader("📈 Tren Harian PM2.5 per Stasiun")
    pm25 = df[df["parameter_pencemar_kritis"] == "PM25"]
    pivot_pm25 = pm25.pivot_table(index="tanggal", columns="stasiun", values="pm_duakomalima")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_pm25.T, cmap="Reds", cbar_kws={'label': 'PM2.5 (µg/m³)'}, ax=ax)
    st.pyplot(fig)
