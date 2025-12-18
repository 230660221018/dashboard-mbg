import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Dashboard Analisis Opini Publik MBG",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CUSTOM CSS – CLEAN & SENIOR
# ======================================================
st.markdown("""
<style>
body { background-color: #f5f7fb; }

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.5rem;
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
}

.hero-subtitle {
    font-size: 15px;
    opacity: 0.9;
    max-width: 960px;
    line-height: 1.7;
}

.card {
    background-color: white;
    padding: 1.8rem;
    border-radius: 20px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.08);
    margin-bottom: 1.8rem;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
}

.section-desc {
    font-size: 14px;
    color: #475569;
    max-width: 900px;
    margin-bottom: 1.4rem;
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
st.sidebar.markdown("## Navigasi Analisis")

menu = st.sidebar.radio(
    "Menu Dashboard",
    ["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"]
)

st.sidebar.divider()

filter_sentimen = st.sidebar.multiselect(
    "Kategori Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(filter_sentimen)]

# ======================================================
# HERO (TEKS TIDAK DIUBAH)
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

    metrics = [
        ("Total Komentar", len(df_filtered)),
        ("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2)),
        ("Rata-rata Balasan", round(df_filtered["jumlah_reply"].mean(), 2)),
        ("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2))
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        col.markdown(f"""
        <div class="card">
            <h4 style="color:#64748b">{label}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# TREN WAKTU – INTERACTIVE
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

    fig = px.area(
        tren,
        x="tanggal",
        y="jumlah_komentar",
        markers=True,
        labels={
            "tanggal": "Tanggal",
            "jumlah_komentar": "Jumlah Komentar"
        }
    )

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified"
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# SENTIMEN – INTERACTIVE BAR
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

    sent = df_filtered["sentimen"].value_counts().reset_index()
    sent.columns = ["sentimen", "jumlah"]

    fig = px.bar(
        sent,
        x="jumlah",
        y="sentimen",
        orientation="h",
        text="jumlah"
    )

    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=20, b=10)
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# KORELASI – INTERACTIVE HEATMAP
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

    cols = [
        "memiliki_gambar",
        "memiliki_video",
        "memiliki_tautan",
        "jumlah_like",
        "jumlah_reply",
        "skor_sentimen"
    ]

    corr = df_filtered[cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )

    fig.update_layout(height=420)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
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

    keyword = st.text_input("Cari kata kunci")

    if keyword:
        df_show = df_filtered[df_filtered.apply(
            lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    else:
        df_show = df_filtered

    st.caption(f"Menampilkan {len(df_show)} dari {len(df_filtered)} data")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_show, use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)
