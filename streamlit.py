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
    st.line_chart(filtered_df.set_index('tanggal')['pm_duakomalima'])
else:
    st.error("Data tanggal tidak tersedia atau semua baris tanggal invalid.")

avg_by_station = date_filtered.groupby('stasiun')['pm_duakomalima'].mean().sort_values()

fig2, ax2 = plt.subplots()
sns.barplot(x=avg_by_station.values, y=avg_by_station.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Rata-rata PM2.5")
ax2.set_ylabel("Stasiun")
st.pyplot(fig2)
st.caption("📌 Pilih rentang tanggal untuk melihat lokasi mana yang paling berpolusi.")
