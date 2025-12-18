import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Dashboard Analisis Opini Publik MBG",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# STYLE – PROFESSIONAL & CLEAN
# ======================================================
st.markdown("""
<style>
body { background-color: #f6f7fb; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}

.hero {
    background: linear-gradient(120deg, #020617, #1e293b);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2.5rem;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 15px;
    line-height: 1.7;
    opacity: 0.9;
    max-width: 980px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.section-desc {
    font-size: 14px;
    color: #475569;
    max-width: 900px;
    margin-bottom: 1.6rem;
}

.kpi-card {
    background: white;
    padding: 1.6rem;
    border-radius: 18px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.08);
}

.kpi-label {
    font-size: 14px;
    color: #64748b;
}

.kpi-value {
    font-size: 36px;
    font-weight: 800;
    margin-top: 0.4rem;
}

.kpi-desc {
    font-size: 13px;
    color: #475569;
    margin-top: 0.6rem;
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
# SIDEBAR – ANALYSIS CONTROL
# ======================================================
st.sidebar.markdown("## 🔎 Pengaturan Analisis")

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

# ======================================================
# HERO
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
# RINGKASAN (KPI YANG MASUK AKAL)
# ======================================================
if menu == "Ringkasan":

    st.markdown('<div class="section-title">Ringkasan Statistik Utama</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Bagian ini menyajikan gambaran umum karakteristik data komentar publik '
        'berdasarkan intensitas interaksi dan kecenderungan sentimen.'
        '</div>',
        unsafe_allow_html=True
    )

    total_komentar = len(df_filtered)
    avg_like = df_filtered["jumlah_like"].mean()
    avg_reply = df_filtered["jumlah_reply"].mean()
    avg_sentiment = df_filtered["skor_sentimen"].mean()

    sentimen_kecenderungan = (
        "Cenderung Positif" if avg_sentiment > 0.05 else
        "Relatif Netral" if -0.05 <= avg_sentiment <= 0.05 else
        "Cenderung Negatif"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Komentar</div>
            <div class="kpi-value">{total_komentar}</div>
            <div class="kpi-desc">Jumlah seluruh komentar yang dianalisis</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Rata-rata Like</div>
            <div class="kpi-value">{avg_like:.2f}</div>
            <div class="kpi-desc">Tingkat apresiasi pengguna terhadap komentar</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Rata-rata Balasan</div>
            <div class="kpi-value">{avg_reply:.2f}</div>
            <div class="kpi-desc">Indikasi diskusi lanjutan dalam komentar</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Kecenderungan Sentimen</div>
            <div class="kpi-value">{avg_sentiment:.2f}</div>
            <div class="kpi-desc">{sentimen_kecenderungan} berdasarkan skor rata-rata</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# TREN WAKTU
# ======================================================
elif menu == "Tren Waktu":

    st.markdown('<div class="section-title">Tren Jumlah Komentar Harian</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Visualisasi ini menunjukkan dinamika jumlah komentar publik dari waktu ke waktu.'
        '</div>',
        unsafe_allow_html=True
    )

    tren = df_filtered.groupby(df_filtered["tanggal"].dt.date).size().reset_index(name="jumlah")
    tren["tanggal"] = pd.to_datetime(tren["tanggal"])

    fig = px.line(
        tren,
        x="tanggal",
        y="jumlah",
        markers=True,
        labels={"tanggal": "Tanggal", "jumlah": "Jumlah Komentar"}
    )

    fig.update_layout(height=420, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# SENTIMEN
# ======================================================
elif menu == "Sentimen":

    st.markdown('<div class="section-title">Distribusi Sentimen Publik</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Distribusi ini menunjukkan proporsi sentimen yang muncul dalam komentar publik.'
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

    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# KORELASI
# ======================================================
elif menu == "Korelasi":

    st.markdown('<div class="section-title">Korelasi Antar Variabel</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Analisis korelasi untuk melihat hubungan antar variabel numerik dalam data.'
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
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# DATA
# ======================================================
elif menu == "Data":

    st.markdown('<div class="section-title">Tabel Data Komentar</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Menampilkan data komentar yang telah melalui proses pembersihan.'
        '</div>',
        unsafe_allow_html=True
    )

    keyword = st.text_input("Cari kata kunci komentar")

    if keyword:
        df_show = df_filtered[df_filtered.astype(str).apply(
            lambda x: x.str.contains(keyword, case=False)).any(axis=1)]
    else:
        df_show = df_filtered

    st.caption(f"Menampilkan {len(df_show)} dari {len(df_filtered)} data")
    st.dataframe(df_show, use_container_width=True, height=450)
