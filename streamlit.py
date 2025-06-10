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
