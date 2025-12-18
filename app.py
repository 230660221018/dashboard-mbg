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
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CUSTOM CSS – SENIOR LEVEL DASHBOARD
# ======================================================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.5rem;
}

h1, h2, h3, h4 {
    color: #0f172a;
}

.hero {
    background: linear-gradient(120deg, #020617, #1e293b);
    padding: 2.6rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 2.4rem;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 0.6rem;
}

.hero-subtitle {
    font-size: 15px;
    opacity: 0.9;
    max-width: 960px;
    line-height: 1.7;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.section-desc {
    font-size: 14px;
    color: #475569;
    margin-bottom: 1.4rem;
    max-width: 900px;
}

.card {
    background-color: white;
    padding: 1.9rem;
    border-radius: 20px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.08);
    margin-bottom: 1.9rem;
}

.kpi-card {
    text-align: center;
}

.kpi-card h4 {
    font-size: 14px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 0.2rem;
}

.kpi-card h2 {
    font-size: 30px;
    font-weight: 800;
    margin: 0;
    color: #020617;
}

.data-info {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 0.6rem;
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
# SIDEBAR
# ======================================================
st.sidebar.markdown("## 📌 Navigasi Analisis")

menu = st.sidebar.radio(
    "Menu Dashboard",
    ["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"]
)

st.sidebar.divider()

st.sidebar.markdown("### 🎯 Filter Data")

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
# HERO HEADER (TIDAK DIUBAH TEKS)
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
        ("Total Komentar", f"{len(df_filtered):,}"),
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
# TREN WAKTU
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

    fig, ax = plt.subplots(figsize=(13, 4.8))
    ax.plot(
        tren["tanggal"],
        tren["jumlah_komentar"],
        linewidth=2.8,
        marker="o",
        markersize=4
    )

    ax.fill_between(
        tren["tanggal"],
        tren["jumlah_komentar"],
        alpha=0.08
    )

    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Komentar")
    ax.grid(alpha=0.25)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))

    plt.xticks(rotation=35, fontsize=9)
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

    fig, ax = plt.subplots(figsize=(7, 4.5))
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

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# DATA – USER FRIENDLY
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

    st.markdown(
        '<div class="data-info">'
        'Gunakan fitur pencarian, pengurutan kolom, dan scroll untuk menelusuri data dengan lebih mudah.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=450
    )
    st.markdown('</div>', unsafe_allow_html=True)
