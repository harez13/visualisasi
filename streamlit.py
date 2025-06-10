import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dan persiapkan data
df = pd.read_csv("clean_data.csv")
try:
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    st.success("Tanggal berhasil diparse secara otomatis.")
except Exception as e:
    st.error(f"Gagal mengubah kolom tanggal: {e}")
    st.stop()

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

st.subheader("2️⃣ Rata-rata PM2.5 Berdasarkan Rentang Waktu")
# Pastikan konversi tanggal aman
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

    st.write("Jumlah data pada rentang:", len(filtered_df))
    st.line_chart(filtered_df.set_index('tanggal')['pm2_5'])
else:
    st.error("Data tanggal tidak tersedia atau semua baris tanggal invalid.")
date_range = st.slider("Pilih rentang tanggal:", min_value=min_date, max_value=max_date, value=(min_date, max_date))

date_filtered = df[(df['tanggal'] >= date_range[0]) & (df['tanggal'] <= date_range[1])]
avg_by_station = date_filtered.groupby('stasiun')['pm_duakomalima'].mean().sort_values()

fig2, ax2 = plt.subplots()
sns.barplot(x=avg_by_station.values, y=avg_by_station.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Rata-rata PM2.5")
ax2.set_ylabel("Stasiun")
st.pyplot(fig2)
st.caption("📌 Pilih rentang tanggal untuk melihat lokasi mana yang paling berpolusi.")

st.subheader("3️⃣ Korelasi Antar Polutan")
pollutants = ['pm_sepuluh', 'pm_duakomalima', 'so2', 'co', 'o3', 'no2']
corr = df[pollutants].corr()

fig3, ax3 = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax3)
ax3.set_title("Matriks Korelasi Antar Polutan")
st.pyplot(fig3)
st.caption("📌 Hubungan erat antar polutan dapat menunjukkan sumber yang sama (misal: kendaraan).")

st.subheader("4️⃣ Sebaran PM2.5")
bins = st.slider("Jumlah kelompok (bin) histogram:", 5, 50, 15)
fig4, ax4 = plt.subplots()
sns.histplot(df['pm_duakomalima'], bins=bins, kde=True, color='salmon', ax=ax4)
ax4.set_title("Sebaran PM2.5 di Jakarta")
ax4.set_xlabel("PM2.5")
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

