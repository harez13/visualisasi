import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi visual
sns.set(style="whitegrid")
st.set_page_config(layout="wide")

# Judul aplikasi
st.title("📊 Visualisasi Kualitas Udara Jakarta")
st.write("""
Aplikasi ini menampilkan lima visualisasi untuk membantu masyarakat umum memahami data polusi udara di Jakarta.
""")

# Load data
df = pd.read_csv("clean_data.csv")
df['tanggal'] = pd.to_datetime(df['tanggal'], format='%d/%m/%Y')

# Visualisasi 1: Rata-rata PM2.5 berdasarkan stasiun
st.subheader("1️⃣ Rata-rata PM2.5 Berdasarkan Stasiun")
st.write("Menunjukkan area di Jakarta dengan tingkat PM2.5 tertinggi.")
avg_pm25 = df.groupby("stasiun")["pm_duakomalima"].mean().sort_values()
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=avg_pm25.values, y=avg_pm25.index, palette="coolwarm", ax=ax1)
ax1.set_xlabel("Rata-rata PM2.5")
ax1.set_ylabel("Stasiun")
st.pyplot(fig1)
st.caption("📌 PM2.5 adalah partikel kecil yang berbahaya jika terhirup. Semakin tinggi batang, semakin buruk kualitas udara.")

# Visualisasi 2: Tren harian PM2.5
st.subheader("2️⃣ Tren Harian PM2.5")
st.write("Menunjukkan bagaimana kualitas udara berubah setiap harinya.")
daily_pm25 = df.groupby('tanggal')['pm_duakomalima'].mean()
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(x=daily_pm25.index, y=daily_pm25.values, color='darkorange', ax=ax2)
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("PM2.5")
ax2.set_title("Tren Harian PM2.5 di Jakarta")
plt.xticks(rotation=45)
st.pyplot(fig2)
st.caption("📌 Lonjakan menunjukkan hari-hari dengan udara yang lebih buruk. Hindari aktivitas luar saat PM2.5 tinggi.")

# Visualisasi 3: Proporsi Kategori Kualitas Udara
st.subheader("3️⃣ Proporsi Kategori Kualitas Udara")
st.write("Menampilkan persentase hari dengan udara Baik, Sedang, atau Tidak Sehat.")
bins = [0, 50, 100, 500]
labels = ['Baik', 'Sedang', 'Tidak Sehat']
df['kategori_pm25'] = pd.cut(df['pm_duakomalima'], bins=bins, labels=labels)
kategori_count = df['kategori_pm25'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(kategori_count, labels=kategori_count.index, autopct='%1.1f%%', colors=['green', 'yellow', 'red'], startangle=140)
ax3.axis('equal')
st.pyplot(fig3)
st.caption("📌 Sebagian besar hari termasuk kategori 'Sedang'. Hari dengan 'Tidak Sehat' harus diwaspadai.")

# Visualisasi 4: Korelasi antar polutan
st.subheader("4️⃣ Korelasi Antar Polutan")
st.write("Menunjukkan seberapa erat hubungan antara berbagai jenis polusi udara.")
pollutants = ['pm_sepuluh', 'pm_duakomalima', 'so2', 'co', 'o3', 'no2']
corr = df[pollutants].corr()
fig4, ax4 = plt.subplots()
sns.heatmap(corr, annot=True, cmap='YlOrRd', ax=ax4)
ax4.set_title("Matriks Korelasi Polutan")
st.pyplot(fig4)
st.caption("📌 Warna lebih gelap berarti polutan saling berkaitan. Misalnya, PM10 dan PM2.5 biasanya meningkat bersamaan.")

# Visualisasi 5: Polusi PM2.5 per Bulan
st.subheader("5️⃣ Distribusi PM2.5 per Bulan")
st.write("Memperlihatkan bulan mana yang cenderung memiliki polusi lebih tinggi.")
df['bulan'] = df['tanggal'].dt.month_name()
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.boxplot(x='bulan', y='pm_duakomalima', data=df, palette="Spectral", ax=ax5)
ax5.set_title("Distribusi PM2.5 Berdasarkan Bulan")
ax5.set_xlabel("Bulan")
ax5.set_ylabel("PM2.5")
plt.xticks(rotation=45)
st.pyplot(fig5)
st.caption("📌 Kotak mewakili kisaran polusi tiap bulan. Bulan dengan nilai tinggi berarti perlu kewaspadaan lebih.")

