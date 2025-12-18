import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

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
    padding: 1.6rem;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 0.4rem;
}

.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
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
# MONGODB CONNECTION
# ======================================================
MONGO_URI = "mongodb+srv://kelompok2:4MMZcM7wapHV0h00@cluster0.ez7evbb.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["mbg_opini"]
collection = db["data_opini"]

# ======================================================
# LOAD DATA (DARI MONGODB)
# ======================================================
@st.cache_data
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
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

    kpis = [
        ("Total Komentar", f"{len(df_filtered)}"),
        ("Rata-rata Like", f"{df_filtered['jumlah_like'].mean():.2f}"),
        ("Rata-rata Balasan", f"{df_filtered['jumlah_reply'].mean():.2f}"),
        ("Rata-rata Skor Sentimen", f"{df_filtered['skor_sentimen'].mean():.2f}")
    ]

    for col, (title, value) in zip([col1, col2, col3, col4], kpis):
        col.markdown(f"""
        <div class="card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# TREN WAKTU
# ======================================================
elif menu == "Tren Waktu":
    st.markdown('<div class="section-title">Tren Jumlah Komentar Harian</div>', unsafe_allow_html=True)

    tren = (
        df_filtered
        .groupby(df_filtered["tanggal"].dt.date)
        .size()
        .reset_index(name="jumlah_komentar")
    )
    tren["tanggal"] = pd.to_datetime(tren["tanggal"])

    fig = px.area(tren, x="tanggal", y="jumlah_komentar", markers=True)
    fig.update_layout(height=420, hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# SENTIMEN
# ======================================================
elif menu == "Sentimen":
    st.markdown('<div class="section-title">Distribusi Sentimen Publik</div>', unsafe_allow_html=True)

    sent = df_filtered["sentimen"].value_counts().reset_index()
    sent.columns = ["sentimen", "jumlah"]

    fig = px.bar(sent, x="jumlah", y="sentimen", orientation="h", text="jumlah")
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# KORELASI
# ======================================================
elif menu == "Korelasi":
    st.markdown('<div class="section-title">Korelasi Antar Variabel</div>', unsafe_allow_html=True)

    cols = [
        "memiliki_gambar",
        "memiliki_video",
        "memiliki_tautan",
        "jumlah_like",
        "jumlah_reply",
        "skor_sentimen"
    ]

    corr = df_filtered[cols].corr()

    fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r")
    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# DATA
# ======================================================
elif menu == "Data":
    st.markdown('<div class="section-title">Tabel Data Opini Publik</div>', unsafe_allow_html=True)

    keyword = st.text_input("Cari kata kunci komentar")

    if keyword:
        df_show = df_filtered[df_filtered.apply(
            lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    else:
        df_show = df_filtered

    st.caption(f"Menampilkan {len(df_show)} dari {len(df_filtered)} data")
    st.dataframe(df_show, use_container_width=True, height=450)



