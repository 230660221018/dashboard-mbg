import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Dashboard Opini Publik MBG",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df

df = load_data()

# ======================
# SIDEBAR = NAVBAR
# ======================
st.sidebar.markdown("## 📊 MBG Dashboard")
st.sidebar.markdown("Analisis Opini Publik")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "📊 Overview",
        "📈 Tren Komentar",
        "💬 Analisis Sentimen",
        "🔥 Korelasi Data",
        "📁 Data Opini"
    ]
)

st.sidebar.divider()

# FILTER GLOBAL
sentimen_filter = st.sidebar.multiselect(
    "Filter Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(sentimen_filter)]

# ======================
# OVERVIEW
# ======================
if menu == "📊 Overview":
    st.title("📊 Overview Opini Publik MBG")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Komentar", len(df_filtered))
    col2.metric("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2))
    col3.metric("Rata-rata Reply", round(df_filtered["jumlah_reply"].mean(), 2))
    col4.metric("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2))

    st.markdown("""
    Halaman ini menyajikan ringkasan statistik utama dari data opini publik  
    terhadap kasus keracunan **Program Makan Bergizi Gratis (MBG)**.
    """)

# ======================
# TREN KOMENTAR
# ======================
elif menu == "📈 Tren Komentar":
    st.title("📈 Tren Komentar dari Waktu ke Waktu")

    df_tren = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
    )

    fig, ax = plt.subplots()
    df_tren.plot(ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.set_title("Tren Jumlah Komentar Harian")
    st.pyplot(fig)

    st.markdown("""
    Visualisasi ini menunjukkan dinamika jumlah komentar pengguna dari waktu  
    ke waktu. Pola peningkatan dan penurunan komentar mencerminkan tingkat  
    perhatian publik terhadap perkembangan isu keracunan MBG.
    """)

# ======================
# ANALISIS SENTIMEN
# ======================
elif menu == "💬 Analisis Sentimen":
    st.title("💬 Distribusi Sentimen Opini Publik")

    sentiment_counts = df_filtered["sentimen"].value_counts()

    fig, ax = plt.subplots()
    sentiment_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    st.pyplot(fig)

    st.markdown("""
    Diagram ini memperlihatkan distribusi sentimen opini publik yang  
    diklasifikasikan ke dalam kategori positif, negatif, dan netral.
    """)

# ======================
# KORELASI
# ======================
elif menu == "🔥 Korelasi Data":
    st.title("🔥 Korelasi Antar Variabel Numerik")

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
    st.pyplot(fig)

    st.markdown("""
    Heatmap ini menggambarkan hubungan antar variabel numerik yang  
    berkaitan dengan tingkat interaksi dan sentimen opini publik.
    """)

# ======================
# DATA
# ======================
elif menu == "📁 Data Opini":
    st.title("📁 Data Opini Publik (Tersaring)")
    st.dataframe(df_filtered, use_container_width=True)
