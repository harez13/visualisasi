import streamlit as st

st.set_page_config(
    page_title = 'App'
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Load data
df = pd.read_csv("clean_data.csv")

# Pastikan tanggal dalam format datetime
df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True, errors='coerce')

# Tambahkan kolom tahun & bulan jika belum ada
df['bulan'] = df['tanggal'].dt.month
df['tahun'] = df['tanggal'].dt.year

st.title("Tren Kategori Kualitas Udara per Bulan")
st.subheader("Parameter Pencemar Kritis: PM2.5")

# Pilihan stasiun
stasiun_list = sorted(df['stasiun'].dropna().unique())
selected_stasiun = st.selectbox("Pilih Stasiun Pemantauan:", stasiun_list)

# Filter data berdasarkan stasiun dan parameter PM2.5
filtered_df = df[(df['stasiun'] == selected_stasiun) & (df['parameter_pencemar_kritis'] == "PM25")]

# Hitung jumlah kategori per bulan
kategori_tren_bulanan = filtered_df.groupby(['bulan', 'kategori']).size().unstack(fill_value=0)

# Plot
st.write(f"Tren kategori kualitas udara bulanan di **{selected_stasiun}**:")

fig, ax = plt.subplots(figsize=(12, 6))
kategori_tren_bulanan.plot(ax=ax, marker='o')
plt.title(f"Tren Kategori Kualitas Udara per Bulan - {selected_stasiun}")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Hari")
plt.xticks(ticks=range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", 
                                       "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Kategori")
st.pyplot(fig)


st.title("Tren Kategori Kualitas Udara per Bulan")
st.subheader("Parameter Pencemar Kritis: PM2.5")
df['nama_bulan'] = df['bulan'].apply(lambda x: calendar.month_name[x])

# Buat pivot table: jumlah kategori per stasiun per bulan
pivot_kategori = df.pivot_table(
    index='stasiun',
    columns='nama_bulan',
    values='kategori',
    aggfunc=lambda x: (x == 'TIDAK SEHAT').sum(),  # contoh: hanya hitung 'TIDAK SEHAT'
    fill_value=0
)

# Urutkan bulan agar kronologis
ordered_months = list(calendar.month_name)[1:]  # ['January', ..., 'December']
pivot_kategori = pivot_kategori[ordered_months]

# Plot heatmap
plt.figure(figsize=(14, 6))
sns.heatmap(pivot_kategori, annot=True, fmt='d', cmap='Reds', linewidths=0.5)
plt.title('Jumlah Hari dengan Kategori "TIDAK SEHAT" per Stasiun per Bulan (2024)', fontsize=14)
plt.xlabel('Bulan')
plt.ylabel('Stasiun')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(pt)
