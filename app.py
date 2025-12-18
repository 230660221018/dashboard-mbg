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
# QUERY PARAM HANDLER (NAVIGATION FIX)
# ======================================================
query_params = st.query_params
default_menu = query_params.get("menu", ["Ringkasan"])[0]

# ======================================================
# CUSTOM CSS – WOW & SENIOR
# ======================================================
st.markdown("""
<style>
body { background-color: #f5f7fb; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}

.hero {
    background: linear-gradient(120deg, #020617, #1e293b);
    padding: 2.8rem;
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
    padding: 1.7rem;
    border-radius: 20px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.08);
    margin-bottom: 1.6rem;
}

.kpi-link {
    text-decoration: none;
    color: inherit;
}

.kpi-link:hover {
    transform: scale(1.015);
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
    ["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"],
    index=["Ringkasan", "Tren Waktu", "Sentimen", "Korelasi", "Data"].index(default_menu)
)

st.sidebar.divider()

filter_sentimen = st.sidebar.multiselect(
    "Kategori Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(filter_sentimen)]

# ======================================================
# HERO (TIDAK DIUBAH)
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
# RINGKASAN (KPI CLICKABLE — FIXED)
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
        ("Total Komentar", len(df_filtered), "Tren Waktu"),
        ("Rata-rata Like", round(df_filtered["jumlah_like"].mean(), 2), "Korelasi"),
        ("Rata-rata Balasan", round(df_filtered["jumlah_reply"].mean(), 2), "Korelasi"),
        ("Rata-rata Skor Sentimen", round(df_filtered["skor_sentimen"].mean(), 2), "Sentimen")
    ]

    for col, (label, value, target) in zip([col1, col2, col3, col4], kpis):
        col.markdown(f"""
        <a class="kpi-link" href="?menu={target}">
            <div class="card">
                <h4 style="color:#64748b">{label}</h4>
                <h2>{value}</h2>
                <p style="font-size:13px;color:#3b82f6">Klik untuk detail</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

# ======================================================
# TREN WAKTU
# ======================================================
elif menu == "Tren Waktu":
    tren = df_filtered.groupby(df_filtered["tanggal"].dt.date).size().reset_index(name="jumlah")
    tren["tanggal"] = pd.to_datetime(tren["tanggal"])

    fig = px.area(
        tren,
        x="tanggal",
        y="jumlah",
        markers=True,
        labels={"tanggal": "Tanggal", "jumlah": "Jumlah Komentar"}
    )

    fig.update_layout(height=420, hovermode="x unified")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# SENTIMEN
# ======================================================
elif menu == "Sentimen":
    sent = df_filtered["sentimen"].value_counts().reset_index()
    sent.columns = ["sentimen", "jumlah"]

    fig = px.bar(sent, x="jumlah", y="sentimen", orientation="h", text="jumlah")
    fig.update_layout(height=360)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# KORELASI
# ======================================================
elif menu == "Korelasi":
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
        color_continuous_scale="RdBu_r"
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# DATA
# ======================================================
elif menu == "Data":
    keyword = st.text_input("Cari kata kunci")

    df_show = df_filtered if not keyword else df_filtered[
        df_filtered.apply(lambda r: r.astype(str).str.contains(keyword, case=False).any(), axis=1)
    ]

    st.caption(f"Menampilkan {len(df_show)} dari {len(df_filtered)} data")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_show, use_container_width=True, height=460)
    st.markdown('</div>', unsafe_allow_html=True)
