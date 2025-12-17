import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Dashboard Analisis Opini Publik MBG",
    layout="wide"
)

# ======================
# MEMUAT DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df.sort_values("tanggal")

df = load_data()

# ======================
# NAVIGASI (SIDEBAR)
# ======================
st.sidebar.title("Navigasi Analisis")

menu = st.sidebar.radio(
    "",
    [
        "Ringkasan Data",
        "Tren Opini dari Waktu ke Waktu",
        "Distribusi Sentimen Publik",
        "Analisis Korelasi",
        "Eksplorasi Data"
    ]
)

st.sidebar.divider()

filter_sentimen = st.sidebar.multiselect(
    "Filter Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(filter_sentimen)]

# ======================
# HALAMAN 1: RINGKASAN
# ======================
if menu == "Ringkasan Data":
    st.title("Ringkasan Kondisi Opini Publik")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Komentar", len(df_filtered))
    col2.metric("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2))
    col3.metric("Rata-rata Balasan", round(df_filtered["jumlah_reply"].mean(), 2))
    col4.metric("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2))

    st.markdown("""
    Halaman ini menyajikan gambaran umum kondisi data opini publik
    terkait kasus keracunan Program Makan Bergizi Gratis (MBG)
    berdasarkan tingkat interaksi dan sentimen pengguna.
    """)

# ======================
# HALAMAN 2: TREN WAKTU
# ======================
elif menu == "Tren Opini dari Waktu ke Waktu":
    st.title("Tren Jumlah Komentar dari Waktu ke Waktu")

    tren_harian = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
        .reset_index(name="jumlah_komentar")
    )

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(tren_harian["tanggal"], tren_harian["jumlah_komentar"])
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.set_title("Perkembangan Aktivitas Komentar Harian")
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.markdown("""
    Visualisasi ini menunjukkan dinamika aktivitas komentar publik
    dari waktu ke waktu. Lonjakan jumlah komentar mengindikasikan
    meningkatnya perhatian masyarakat terhadap perkembangan isu MBG.
    """)

# ======================
# HALAMAN 3: SENTIMEN
# ======================
elif menu == "Distribusi Sentimen Publik":
    st.title("Distribusi Sentimen Opini Publik")

    sentimen_count = df_filtered["sentimen"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    sentimen_count.plot(kind="bar", ax=ax)
    ax.set_xlabel("Kategori Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    ax.set_title("Dominasi Sentimen Publik")
    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

# ======================
# HALAMAN 4: KORELASI
# ======================
elif menu == "Analisis Korelasi":
    st.title("Analisis Korelasi Antar Variabel Numerik")

    kolom_numerik = [
        "memiliki_gambar",
        "memiliki_video",
        "memiliki_tautan",
        "jumlah_like",
        "jumlah_reply",
        "skor_sentimen"
    ]

    corr = df_filtered[kolom_numerik].corr(method="pearson")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Heatmap Korelasi")

    st.pyplot(fig)

# ======================
# HALAMAN 5: DATA
# ======================
elif menu == "Eksplorasi Data":
    st.title("Eksplorasi Data Opini Publik")
    st.dataframe(df_filtered, use_container_width=True)
