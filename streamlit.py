import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Baca dan bersihkan data
df = pd.read_csv("clean_data.csv")
df.columns = df.columns.str.strip().str.lower()

# Konversi tanggal
df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')

# Hapus baris yang tanggalnya tidak valid
df = df.dropna(subset=['tanggal'])

# Tentukan nilai min dan max untuk slider
min_date = df['tanggal'].min().date()
max_date = df['tanggal'].max().date()

# UI Slider rentang tanggal
st.title("Rata-rata PM2.5 Berdasarkan Rentang Waktu")
st.markdown("Gunakan slider di bawah untuk memilih rentang waktu dan lihat bagaimana polusi udara berubah dari waktu ke waktu.")

date_range = st.slider(
    "Pilih rentang tanggal:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter data berdasarkan tanggal yang dipilih
start_date, end_date = date_range
mask = (df['tanggal'].dt.date >= start_date) & (df['tanggal'].dt.date <= end_date)
filtered_df = df[mask]

# Tampilkan line chart jika data tersedia
if 'pm_duakomalima' in filtered_df.columns and not filtered_df.empty:
    st.line_chart(filtered_df.set_index('tanggal')['pm_duakomalima'])
    st.caption("Grafik menunjukkan tren kadar PM2.5 dalam rentang waktu yang dipilih. PM2.5 adalah partikel udara halus yang berbahaya jika terhirup dalam jangka panjang.")
else:
    st.warning("Tidak ada data yang tersedia dalam rentang tanggal ini atau kolom 'pm2_5' tidak ditemukan.")


# Dropdown stasiun
st.subheader("1️⃣ Tren Harian PM2.5 per Stasiun")
selected_station = st.selectbox("Pilih Stasiun:", df['stasiun'].unique())

filtered = df[df['stasiun'] == selected_station]
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='tanggal', y='pm_duakomalima', ax=ax, color='teal')
ax.set_title(f'Tren Harian PM2.5 - {selected_station}')
ax.set_ylabel('PM2.5')
ax.set_xlabel('Tanggal')
st.pyplot(fig)
st.caption("📌 Lihat apakah kualitas udara memburuk/meningkat di stasiun yang dipilih.")

st.subheader("3️⃣ Korelasi Antar Polutan")
pollutants = ['pm_sepuluh', 'pm_duakomalima', 'so2', 'co', 'o3', 'no2']
corr = df[pollutants].corr()

fig3, ax3 = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax3)
ax3.set_title("Matriks Korelasi Antar Polutan")
st.pyplot(fig3)
st.caption("📌 Hubungan erat antar polutan dapat menunjukkan sumber yang sama (misal: kendaraan).")

