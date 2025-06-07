import streamlit as st

st.set_page_config(
    page_title = 'App'
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("clean_data.csv")

# Konversi tanggal jika diperlukan
if 'tanggal' in df.columns:
    df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True, errors='coerce')

# Tambahkan kolom tahun jika belum ada
if 'tahun' not in df.columns:
    df['tahun'] = pd.DatetimeIndex(df['tanggal']).year

st.title("Tren Kategori Kualitas Udara per Tahun")
st.subheader("Berdasarkan Parameter Pencemar Kritis = PM2.5")

# Pilihan stasiun
stasiun_list = sorted(df['stasiun'].dropna().unique())
selected_stasiun = st.selectbox("Pilih Stasiun Pemantauan:", stasiun_list)

# Filter data berdasarkan pilihan
filtered_df = df[(df['stasiun'] == selected_stasiun) & (df['parameter_pencemar_kritis'] == "PM25")]

# Hitung jumlah kategori per tahun
kategori_tren_tahunan = filtered_df.groupby(['tahun', 'kategori']).size().unstack(fill_value=0)

# Visualisasi
st.write(f"Tren Kategori Kualitas Udara di **{selected_stasiun}** berdasarkan data tahunan:")

fig, ax = plt.subplots(figsize=(10, 6))
kategori_tren_tahunan.plot(ax=ax, marker='o')
plt.title(f"Tren Kategori Kualitas Udara per Tahun - {selected_stasiun}")
plt.xlabel("Tahun")
plt.ylabel("Jumlah Hari")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Kategori")
st.pyplot(fig)
