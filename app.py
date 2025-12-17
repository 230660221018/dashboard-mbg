import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Dashboard Analisis Opini Publik MBG",
    layout="wide"
)

# ======================================================
# CUSTOM CSS – PROFESSIONAL & CLEAN
# ======================================================
st.markdown("""
<style>
body {
    background-color: #f4f6fa;
}

.block-container {
    padding-top: 1.8rem;
}

h1, h2, h3, h4 {
    color: #111827;
}

.hero {
    background: linear-gradient(90deg, #0f172a, #1e293b);
    padding: 2.2rem;
    border-radius: 18px;
    color: white;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 32px;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 15px;
    opacity: 0.9;
    max-width: 900px;
    line-height: 1.6;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.section-desc {
    font-size: 14px;
    color: #4b5563;
    margin-bottom: 1.2rem;
    max-width: 900px;
}

.card {
    background-color: white;
    padding: 1.6rem;
    border-radius: 16px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    margin-bottom: 1.8rem;
}

.kpi-card h4 {
    margin-bottom: 0.2rem;
    color: #6b7280;
    font-weight: 500;
}

.kpi-card h2 {
    margin: 0;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df.sort_values("tanggal")

df = load_data()

# ======================================================
# SIDEBAR – CLEAN & AKADEMIK
# ======================================================
st.sidebar.markdown("### Navigasi Analisis")

menu = st.sidebar.radio(
    "Pilih Menu",
    ["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"]
)

st.sidebar.divider()

st.sidebar.markdown("### Filter Data")

filter_sentimen = st.sidebar.multiselect(
    "Kategori Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(filter_sentimen)]

st.sidebar.divider()
st.sidebar.caption(
    "Dashboard ini dikembangkan untuk keperluan analisis data dan "
    "visualisasi opini publik dalam konteks akademik."
)

# ======================================================
# HERO HEADER
# ======================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">Dashboard Analisis Opini Publik MBG</div>
    <div class="hero-subtitle">
        Dashboard ini menyajikan hasil analisis visual terhadap data komentar publik
        terkait kasus keracunan Program Makan Bergizi Gratis (MBG). Analisis difokuskan
        pada pola aktivitas komentar, distribusi sentimen, serta hubungan antar variabel
        interaksi pengguna di media sosial.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# RINGKASAN
# ======================================================
if menu == "Ringkasan":
    st.markdown('<div class="section-title">Ringkasan Statistik Utama</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Bagian ini menyajikan gambaran umum karakteristik data komentar publik '
        'berdasarkan jumlah interaksi dan kecenderungan sentimen.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    kpi = [
        ("Total Komentar", len(df_filtered)),
        ("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2)),
        ("Rata-rata Balasan", round(df_filtered["jumlah_reply"].mean(), 2)),
        ("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2))
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], kpi):
        col.markdown(f"""
        <div class="card kpi-card">
            <h4>{label}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# TREN WAKTU – HARIAN RAPIH
# ======================================================
elif menu == "Tren Waktu":
    st.markdown('<div class="section-title">Tren Jumlah Komentar Harian</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Visualisasi ini menunjukkan perkembangan jumlah komentar publik dari waktu ke waktu '
        'berdasarkan tanggal unggahan, sehingga dapat diamati dinamika perhatian publik terhadap isu MBG.'
        '</div>',
        unsafe_allow_html=True
    )

    tren = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
        .reset_index(name="jumlah_komentar")
    )

    tren["tanggal"] = pd.to_datetime(tren["tanggal"])

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(tren["tanggal"], tren["jumlah_komentar"], linewidth=2.5)

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(alpha=0.3)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=9))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))

    plt.xticks(rotation=45, fontsize=9)
    plt.tight_layout()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# SENTIMEN
# ======================================================
elif menu == "Sentimen":
    st.markdown('<div class="section-title">Distribusi Sentimen Publik</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Bagian ini menggambarkan proporsi sentimen publik yang muncul dalam komentar, '
        'sehingga dapat diketahui kecenderungan persepsi masyarakat terhadap program MBG.'
        '</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    df_filtered["sentimen"].value_counts().plot(kind="bar", ax=ax)

    ax.set_xlabel("Kategori Sentimen")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(axis="y", alpha=0.3)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# KORELASI
# ======================================================
elif menu == "Korelasi":
    st.markdown('<div class="section-title">Korelasi Antar Variabel</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Analisis korelasi digunakan untuk mengidentifikasi hubungan antar variabel numerik '
        'yang berkaitan dengan karakteristik konten dan tingkat interaksi pengguna.'
        '</div>',
        unsafe_allow_html=True
    )

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

# ======================================================
# DATA
# ======================================================
elif menu == "Data":
    st.markdown('<div class="section-title">Tabel Data Opini Publik</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Tabel berikut menampilkan data komentar publik yang telah melalui proses pembersihan data '
        'dan digunakan sebagai dasar analisis pada dashboard ini.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


