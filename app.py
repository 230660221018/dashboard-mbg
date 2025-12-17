import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# PAGE CONFIGURATION
# ======================
st.set_page_config(
    page_title="Public Opinion Analysis Dashboard – MBG",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data_opini_clean.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df

df = load_data()

# ======================
# SIDEBAR NAVIGATION
# ======================
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "",
    [
        "Overview",
        "Temporal Analysis",
        "Sentiment Analysis",
        "Correlation Analysis",
        "Data Exploration"
    ]
)

st.sidebar.divider()

sentiment_filter = st.sidebar.multiselect(
    "Sentiment Filter",
    options=df["sentimen"].unique(),
    default=df["sentimen"].unique()
)

df_filtered = df[df["sentimen"].isin(sentiment_filter)]

# ======================
# OVERVIEW
# ======================
if menu == "Overview":
    st.title("Overview of Public Opinion on MBG")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Comments", len(df_filtered))
    col2.metric("Average Likes", round(df_filtered["jumlah_like"].mean(), 2))
    col3.metric("Average Replies", round(df_filtered["jumlah_reply"].mean(), 2))
    col4.metric("Average Sentiment Score", round(df_filtered["skor_sentimen"].mean(), 2))

    st.markdown("""
    This section provides a general overview of public engagement and sentiment
    regarding the Free Nutritious Meal Program (MBG) based on social media comments.
    """)

# ======================
# TEMPORAL ANALYSIS
# ======================
elif menu == "Temporal Analysis":
    st.title("Temporal Trend of Public Comments")

    df_time = (
        df_filtered
        .set_index("tanggal")
        .resample("D")
        .size()
        .reset_index(name="total_comments")
    )

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_time["tanggal"], df_time["total_comments"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Comments")
    ax.set_title("Daily Comment Volume Over Time")
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.markdown("""
    The line chart illustrates the temporal distribution of public comments.
    Fluctuations indicate changes in public attention following developments
    related to the MBG case.
    """)

# ======================
# SENTIMENT ANALYSIS
# ======================
elif menu == "Sentiment Analysis":
    st.title("Sentiment Distribution")

    sentiment_counts = df_filtered["sentimen"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    sentiment_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Sentiment Category")
    ax.set_ylabel("Number of Comments")
    ax.set_title("Distribution of Sentiment Categories")
    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

# ======================
# CORRELATION ANALYSIS
# ======================
elif menu == "Correlation Analysis":
    st.title("Correlation Between Numerical Variables")

    numeric_columns = [
        "memiliki_gambar",
        "memiliki_video",
        "memiliki_tautan",
        "jumlah_like",
        "jumlah_reply",
        "skor_sentimen"
    ]

    corr = df_filtered[numeric_columns].corr(method="pearson")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")

    st.pyplot(fig)

# ======================
# DATA EXPLORATION
# ======================
elif menu == "Data Exploration":
    st.title("Filtered Opinion Data")
    st.dataframe(df_filtered, use_container_width=True)
