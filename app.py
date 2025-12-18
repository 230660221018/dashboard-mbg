# ==============================
# app.py
# Dashboard Analisis Komentar Publik
# Redesign KPI Profesional & Mudah Dipahami
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------
# KONFIGURASI HALAMAN
# ------------------------------
st.set_page_config(
    page_title="Dashboard Analisis Komentar Publik",
    page_icon="📊",
    layout="wide"
)

# ------------------------------
# STYLE GLOBAL
# ------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f6f7fb;
    }
    .kpi-card {
        background: linear-gradient(135deg, #ffffff, #f9fafc);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        height: 100%;
    }
    .kpi-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: 700;
        color: #111827;
    }
    .kpi-desc {
        font-size: 13px;
        color: #4b5563;
        margin-top: 6px;
    }
    .sent-pos { color: #16a34a; font-weight: 600; }
    .sent-neg { color: #dc2626; font-weight: 600; }
    .sent-net { color: #f59e0b; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# LOAD DATA (CONTOH)
# GANTI DENGAN DATASET ASLI ANDA
# ------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    data = pd.DataFrame({
        "tanggal": pd.date_range("2024-01-01", periods=80),
        "like": np.random.poisson(4, 80),
        "balasan": np.random.binomial(1, 0.25, 80),
        "sentimen": np.random.choice([
            "Positif", "Negatif", "Netral"
        ], p=[0.35, 0.45, 0.20], size=80)
    })

    data["skor_sentimen"] = data["sentimen"].map({
        "Positif": 1,
        "Netral": 0,
        "Negatif": -1
    })

    return data

df = load_data()

# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.title("⚙️ Kontrol Analisis")
st.sidebar.markdown("Gunakan filter untuk menyesuaikan tampilan data.")

sent_filter = st.sidebar.multiselect(
    "Filter Sentimen",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

filtered_df = df[df["sentimen"].isin(sent_filter)]

# ------------------------------
# HEADER
# ------------------------------
st.markdown("## 📊 Ringkasan Statistik Utama")
st.markdown(
    "Dashboard ini menyajikan **indikator kinerja utama (KPI)** untuk membantu memahami **tingkat interaksi** dan **kecenderungan sentimen komentar publik** secara ringkas dan intuitif."
)

# ------------------------------
# HITUNG KPI
# ------------------------------

jumlah_komentar = len(filtered_df)
rata_like = filtered_df["like"].mean()
rata_balasan = filtered_df["balasan"].mean()
rata_sentimen = filtered_df["skor_sentimen"].mean()

if rata_sentimen > 0.1:
    sent_label = "Dominan Positif"
    sent_class = "sent-pos"
elif rata_sentimen < -0.1:
    sent_label = "Dominan Negatif"
    sent_class = "sent-neg"
else:
    sent_label = "Cenderung Netral"
    sent_class = "sent-net"

# ------------------------------
# KPI CARDS (REDESIGN TOTAL)
# ------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Komentar</div>
        <div class="kpi-value">{jumlah_komentar}</div>
        <div class="kpi-desc">Jumlah keseluruhan komentar yang dianalisis setelah filter diterapkan.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Rata-rata Like</div>
        <div class="kpi-value">{rata_like:.2f}</div>
        <div class="kpi-desc">Rata-rata jumlah like yang diterima setiap komentar sebagai indikator ketertarikan audiens.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Rata-rata Balasan</div>
        <div class="kpi-value">{rata_balasan:.2f}</div>
        <div class="kpi-desc">Proporsi komentar yang memicu diskusi lanjutan melalui balasan.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Indeks Sentimen</div>
        <div class="kpi-value">{rata_sentimen:.2f}</div>
        <div class="kpi-desc">Kecenderungan sentimen publik: <span class="{sent_class}">{sent_label}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# PENJELASAN SENTIMEN (BIAR AUDIENS PAHAM)
# ------------------------------
st.markdown("---")
st.markdown("### 🧠 Cara Membaca Indeks Sentimen")

st.info(
    """
    **Indeks Sentimen** dihitung dari skor berikut:
    
    • **+1** → Komentar Positif  
    • **0** → Komentar Netral  
    • **-1** → Komentar Negatif

    Nilai rata-rata mendekati **+1** menunjukkan persepsi publik yang sangat positif, sedangkan nilai mendekati **-1** menunjukkan sentimen negatif yang dominan.
    """
)

# ------------------------------
# VISUALISASI SENTIMEN
# ------------------------------
st.markdown("### 📈 Distribusi Sentimen Komentar")

sent_count = filtered_df["sentimen"].value_counts().reset_index()
sent_count.columns = ["Sentimen", "Jumlah"]

fig = px.bar(
    sent_count,
    x="Sentimen",
    y="Jumlah",
    text="Jumlah",
    title="Distribusi Jumlah Komentar Berdasarkan Sentimen"
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=18
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# TABEL DETAIL (OPSIONAL)
# ------------------------------
with st.expander("📄 Lihat Data Komentar"):
    st.dataframe(filtered_df, use_container_width=True)

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("---")
st.caption("Dashboard ini dirancang untuk membantu analisis data secara cepat, intuitif, dan komunikatif bagi audiens non-teknis maupun akademik.")
