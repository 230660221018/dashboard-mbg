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
# CUSTOM CSS (PROFESSIONAL LOOK)
# ======================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
.dashboard-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.dashboard-subtitle {
    font-size: 16px;
    color: #6c757d;
    margin-bottom: 2rem;
}
.card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df.sort_values("tanggal")

df = load_data()

# ======================
# SIDEBAR NAVIGASI
# ======================
st.sidebar.title("Dashboard MBG")
menu = st.sidebar.radio(
    "Menu Analisis",
    [
        "Ringkasan",
        "Tren Waktu",
        "Sentimen",
        "Korelasi",
        "Data"
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
# HEADER UTAMA
# ======================
st.markdown('<div class="dashboard-title">Dashboard Analisis Opini Publik MBG</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Analisis data komentar publik terkait kasus keracunan Program Makan Bergizi Gratis (MBG)</div>', unsafe_allow_html=True)

# ======================
# RINGKASAN
# ======================
if menu == "Ringkasan":
    st.markdown('<div class="section-title">Ringkasan Statistik Utama</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    for col, title, value in zip(
        [col1, col2, col3, col4],
        ["Total Komentar", "Rata-rata Like", "Rata-rata Balasan", "Rata-rata Skor Sentimen"],
        [
            len(df_filtered),
            round(df_filtered["jumlah_like"].mean(), 2),
            round(df_filtered["jumlah_reply"].mean(), 2),
            round(df_filtered["skor_sentimen"].mean(), 2)
        ]
    ):
        col.markdown(f"""
        <div class="card">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# ======================
# TREN WAKTU
# ======================
elif menu == "Tren Waktu":
    st.markdown('<div class="section-title">Tren Aktivitas Komentar</div>', unsafe_allow_html=True)

    tren = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
        .reset_index(name="jumlah_komentar")
    )

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(tren["tanggal"], tren["jumlah_komentar"])
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(alpha=0.3)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# SENTIMEN
# ======================
elif menu == "Sentimen":
    st.markdown('<div class="section-title">Distribusi Sentimen Publik</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    df_filtered["sentimen"].value_counts().plot(kind="bar", ax=ax)
    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(axis="y", alpha=0.3)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# KORELASI
# ======================
elif menu == "Korelasi":
    st.markdown('<div class="section-title">Korelasi Antar Variabel Numerik</div>', unsafe_allow_html=True)

    kolom_numerik = [
        "memiliki_gambar",
        "memiliki_video",
        "memiliki_tautan",
        "jumlah_like",
        "jumlah_reply",
        "skor_sentimen"
    ]

    corr = df_filtered[kolom_numerik].corr()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# DATA
# ======================
elif menu == "Data":
    st.markdown('<div class="section-title">Data Opini Publik</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
