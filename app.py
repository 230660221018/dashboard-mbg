import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Analisis Opini Publik MBG",
    layout="wide"
)

# =========================
# CUSTOM CSS – WEBSITE STYLE
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f6fa;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(90deg, #111827, #1f2937);
    padding: 2.2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 32px;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.9;
    max-width: 900px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #111827;
}

.card {
    background-color: white;
    padding: 1.6rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}

.kpi-card h4 {
    margin-bottom: 0.3rem;
    color: #6b7280;
    font-weight: 500;
}

.kpi-card h2 {
    margin: 0;
    color: #111827;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df.sort_values("tanggal")

df = load_data()

# =========================
# SIDEBAR NAVIGASI
# =========================
st.sidebar.title("Menu Analisis")

menu = st.sidebar.radio(
    "Pilih Tampilan",
    ["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"]
)

st.sidebar.divider()

filter_sentimen = st.sidebar.multiselect(
    "Filter Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(filter_sentimen)]

# =========================
# HEADER UTAMA
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">Dashboard Analisis Opini Publik MBG</div>
    <div class="hero-subtitle">
        Dashboard ini menyajikan analisis visual terhadap data komentar publik
        terkait kasus keracunan Program Makan Bergizi Gratis (MBG) berdasarkan
        aktivitas, sentimen, serta pola interaksi pengguna di media sosial.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# RINGKASAN
# =========================
if menu == "Ringkasan":
    st.markdown('<div class="section-title">Ringkasan Statistik Utama</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    kpi_data = [
        ("Total Komentar", len(df_filtered)),
        ("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2)),
        ("Rata-rata Balasan", round(df_filtered["jumlah_reply"].mean(), 2)),
        ("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2))
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], kpi_data):
        col.markdown(f"""
        <div class="card kpi-card">
            <h4>{label}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# =========================
# TREN WAKTU – HARIAN RAPIH
# =========================
elif menu == "Tren Waktu":
    st.markdown('<div class="section-title">Tren Jumlah Komentar Harian</div>', unsafe_allow_html=True)

    tren_harian = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
        .reset_index(name="jumlah_komentar")
    )

    tren_harian["tanggal"] = pd.to_datetime(tren_harian["tanggal"])

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        tren_harian["tanggal"],
        tren_harian["jumlah_komentar"],
        linewidth=2.5
    )

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(alpha=0.3)

    # FORMAT TANGGAL BIAR TIDAK BERHIMPITAN
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))

    plt.xticks(rotation=45, fontsize=9)
    plt.tight_layout()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# SENTIMEN
# =========================
elif menu == "Sentimen":
    st.markdown('<div class="section-title">Distribusi Sentimen Publik</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    df_filtered["sentimen"].value_counts().plot(kind="bar", ax=ax)

    ax.set_xlabel("Kategori Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(axis="y", alpha=0.3)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# KORELASI
# =========================
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

# =========================
# DATA
# =========================
elif menu == "Data":
    st.markdown('<div class="section-title">Tabel Data Opini Publik</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
