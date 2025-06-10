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
df.columns = df.columns.str.strip().str.lower()  # membersihkan nama kolom

# Daftar kolom polutan berdasarkan isi dataset
pollutants = ['pm_duakomalima', 'pm_sepuluh', 'sulfur_dioksida', 'karbon_monoksida', 'ozon', 'nitrogen_dioksida']
st.write("Kolom tersedia:", df.columns.tolist())


# Validasi: pastikan kolom ini ada dalam dataframe
pollutants = [col for col in pollutants if col in df.columns]

# Pastikan cukup data untuk visualisasi
if len(pollutants) >= 2:
    corr = df[pollutants].corr()

    # Plot heatmap
    st.title("Korelasi Antar Polutan")
    st.markdown("Matriks berikut menunjukkan hubungan antar polutan. Korelasi tinggi (mendekati 1 atau -1) artinya dua polutan sering naik-turun bersama.")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.caption("Contoh: Jika PM2.5 dan PM10 memiliki korelasi 0.9, berarti saat PM2.5 tinggi, PM10 juga biasanya tinggi.")
else:
    st.warning("Tidak cukup data polutan untuk membuat heatmap korelasi.")

st.subheader("4️⃣ Sebaran PM2.5")
bins = st.slider("Jumlah kelompok (bin) histogram:", 5, 50, 15)
fig4, ax4 = plt.subplots()
sns.histplot(df['pm_duakomalima'], bins=bins, kde=True, color='salmon', ax=ax4)
ax4.set_title("Sebaran PM2.5 di Jakarta")
ax4.set_xlabel("PM2.5")
ax4.set_ylabel("Jumlah Hari")
st.pyplot(fig4)
st.caption("📌 Gunakan histogram untuk memahami seberapa sering udara termasuk tidak sehat.")

st.subheader("5️⃣ Distribusi PM2.5 per Bulan")
df['bulan'] = df['tanggal'].dt.month_name()
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.boxplot(x='bulan', y='pm_duakomalima', data=df, palette="crest", ax=ax5)
ax5.set_title("Distribusi PM2.5 Berdasarkan Bulan")
ax5.set_xlabel("Bulan")
ax5.set_ylabel("PM2.5")
plt.xticks(rotation=45)
st.pyplot(fig5)
st.caption("📌 Bandingkan kualitas udara antar bulan. Bulan dengan nilai tinggi → potensi bahaya lebih besar.")


