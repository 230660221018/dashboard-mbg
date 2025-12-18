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
# ADVANCED STYLE – ENTERPRISE
# ======================================================
st.markdown("""
<style>
body { background-color: #f4f6fb; }

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    padding: 3rem;
    border-radius: 26px;
    color: white;
    margin-bottom: 2.8rem;
}

.hero-title {
    font-size: 40px;
    font-weight: 900;
}

.hero-subtitle {
    font-size: 16px;
    line-height: 1.75;
    opacity: 0.92;
    max-width: 1000px;
}

/* SECTION */
.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 0.4rem;
}

.section-desc {
    font-size: 14px;
    color: #475569;
    max-width: 950px;
    margin-bottom: 2rem;
}

/* KPI */
.kpi {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    padding: 1.8rem;
    border-radius: 22px;
    box-shadow: 0 18px 44px rgba(0,0,0,0.12);
    height: 100%;
}

.kpi-icon {
    font-size: 30px;
}

.kpi-value {
    font-size: 40px;
    font-weight: 900;
    margin-top: 0.5rem;
}

.kpi-label {
    font-size: 14px;
    color: #475569;
    margin-top: 0.2rem;
}

.kpi-desc {
    font-size: 13px;
    color: #64748b;
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
# SIDEBAR – SMART CONTROL
# ======================================================
st.sidebar.markdown("## 🎛️ Kontrol Analisis")

date_min, date_max = df["tanggal"].min(), df["tanggal"].max()
date_range = st.sidebar.date_input(
    "Rentang Waktu Analisis",
    value=(date_min, date_max)
)

filter_sentimen = st.sidebar.multiselect(
    "Fokus Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

menu = st.sidebar.radio(
    "Tampilan Analisis",
    ["Ringkasan Eksekutif", "Tren Opini", "Distribusi Sentimen", "Hubungan Variabel", "Data Mentah"]
)

df_filtered = df[
    (df["tanggal"].dt.date >= date_range[0]) &
    (df["tanggal"].dt.date <= date_range[1]) &
    (df["sentimen"].isin(filter_sentimen))
]

# ======================================================
# HERO
# ======================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">Dashboard Analisis Opini Publik MBG</div>
    <div class="hero-subtitle">
        Dashboard ini menyajikan hasil analisis visual terhadap data komentar publik
        terkait kasus keracunan Program Makan Bergizi Gratis (MBG). Analisis difokuskan
        pada dinamika opini, intensitas interaksi, serta kecenderungan sentimen publik
        di media sosial.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# RINGKASAN EKSEKUTIF (WOW)
# ======================================================
if menu == "Ringkasan Eksekutif":

    st.markdown('<div class="section-title">Ringkasan Eksekutif</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        'Gambaran tingkat perhatian publik dan kecenderungan opini terhadap isu MBG '
        'berdasarkan analisis data komentar.'
        '</div>',
        unsafe_allow_html=True
    )

    total = len(df_filtered)
    avg_like = df_filtered["jumlah_like"].mean()
    avg_reply = df_filtered["jumlah_reply"].mean()
    avg_sent = df_filtered["skor_sentimen"].mean()

    sent_label = (
        "Dominan Positif" if avg_sent > 0.05 else
        "Relatif Netral" if -0.05 <= avg_sent <= 0.05 else
        "Dominan Negatif"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-icon">💬</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-label">Total Komentar</div>
            <div class="kpi-desc">Volume perhatian publik terhadap isu MBG</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-icon">👍</div>
            <div class="kpi-value">{avg_like:.1f}</div>
            <div class="kpi-label">Rata-rata Like</div>
            <div class="kpi-desc">Indikasi apresiasi dan visibilitas komentar</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-icon">💬↩️</div>
            <div class="kpi-value">{avg_reply:.1f}</div>
            <div class="kpi-label">Rata-rata Balasan</div>
            <div class="kpi-desc">Tingkat diskusi lanjutan antar pengguna</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-icon">🧭</div>
            <div class="kpi-value">{avg_sent:.2f}</div>
            <div class="kpi-label">Kecenderungan Sentimen</div>
            <div class="kpi-desc">{sent_label} berdasarkan skor sentimen</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# SECTION LAIN (tetap stabil & rapi)
# ======================================================
elif menu == "Tren Opini":
    tren = df_filtered.groupby(df_filtered["tanggal"].dt.date).size().reset_index(name="jumlah")
    tren["tanggal"] = pd.to_datetime(tren["tanggal"])
    fig = px.line(tren, x="tanggal", y="jumlah", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Distribusi Sentimen":
    sent = df_filtered["sentimen"].value_counts().reset_index()
    sent.columns = ["sentimen", "jumlah"]
    fig = px.bar(sent, x="jumlah", y="sentimen", orientation="h", text="jumlah")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Hubungan Variabel":
    cols = ["jumlah_like", "jumlah_reply", "skor_sentimen"]
    corr = df_filtered[cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Data Mentah":
    st.dataframe(df_filtered, use_container_width=True, height=500)
