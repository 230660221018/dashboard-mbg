import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Dashboard Analisis Opini Publik MBG")
st.write("Analisis interaksi dan sentimen publik terhadap kasus keracunan Program Makan Bergizi Gratis (MBG)")

# Load data
df = pd.read_csv("data_opini.csv")

# Sidebar
st.sidebar.header("Informasi Dataset")
st.sidebar.write("Jumlah data:", df.shape[0])

# ======================
# Distribusi Sentimen
# ======================
st.subheader("Distribusi Sentimen")
sentiment_counts = df["sentimen"].value_counts()

fig1, ax1 = plt.subplots()
sentiment_counts.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Sentimen")
ax1.set_ylabel("Jumlah Komentar")
st.pyplot(fig1)

# ======================
# Heatmap Korelasi
# ======================
st.subheader("Heatmap Korelasi Antar Variabel Numerik")

kolom_numerik = [
    "memiliki_gambar",
    "memiliki_video",
    "memiliki_tautan",
    "jumlah_like",
    "jumlah_reply",
    "skor_sentimen"
]

corr = df[kolom_numerik].corr(method="pearson")

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# ======================
# Tabel Data
# ======================
st.subheader("Tabel Data Opini Publik")
st.dataframe(df)

