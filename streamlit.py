import pandas as pd
import streamlit as st

df = pd.read_csv("clean_data.csv")

# Bersihkan nama kolom agar aman digunakan
df.columns = df.columns.str.strip().str.lower()

# Tampilkan nama kolom untuk memverifikasi
st.write("Kolom tersedia:", df.columns.tolist())

# Konversi kolom tanggal
df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
valid_dates = df['tanggal'].dropna()

if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.slider(
        "Pilih rentang tanggal:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    start_date, end_date = date_range
    mask = (df['tanggal'].dt.date >= start_date) & (df['tanggal'].dt.date <= end_date)
    filtered_df = df[mask]

    # Pastikan kolom pm2_5 tersedia
    if 'pm2_5' in filtered_df.columns:
        st.line_chart(filtered_df.set_index('tanggal')['pm2_5'])
    else:
        st.error("Kolom 'pm2_5' tidak ditemukan setelah pembersihan.")
else:
    st.error("Data tanggal tidak valid atau kosong.")
