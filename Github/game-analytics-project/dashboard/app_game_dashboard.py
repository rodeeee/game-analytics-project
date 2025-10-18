import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# Konfigurasi halaman
st.set_page_config(page_title="Executive Dashboard Game Analytics", layout="wide")

# Load data
df = pd.read_csv("../data/game_user_activity_clean.csv")
if df.empty:
    st.error("Data gagal dimuat. Pastikan file game_user_activity_clean.csv ada dan tidak kosong.")
    st.stop()

df['login_date'] = pd.to_datetime(df['login_date'])

st.title("🎮 Executive Dashboard - Aktivitas Pemain Game")

# KPI Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rata-rata Durasi Main (menit)", f"{df['session_duration'].mean():.2f}")
with col2:
    st.metric("Skor Rata-rata", f"{df['score'].mean():.2f}")
with col3:
    st.metric("Total Pembelian In-Game (USD)", f"{df['in_game_purchase'].sum():.2f}")

# Grafik Genre
st.subheader("Distribusi Genre Game")
genre_chart = px.bar(df.groupby('game_genre')['score'].mean().reset_index(),
                     x='game_genre', y='score', color='game_genre',
                     title='Rata-rata Skor per Genre')
st.plotly_chart(genre_chart, use_container_width=True)

# Grafik Device
st.subheader("Durasi Main Berdasarkan Device")
device_chart = px.box(df, x='device', y='session_duration', color='device',
                      title='Distribusi Durasi Main per Perangkat')
st.plotly_chart(device_chart, use_container_width=True)

# Insight Otomatis
st.subheader("📈 Insight Otomatis")
top_genre = df.groupby('game_genre')['score'].mean().idxmax()
most_used_device = df['device'].mode()[0]

insight = (
    f"Genre dengan performa terbaik adalah **{top_genre}**, "
    f"dengan skor rata-rata tertinggi. "
    f"Sebagian besar pemain menggunakan **{most_used_device}** "
    f"sebagai perangkat utama mereka."
)
st.markdown(insight)

# Export ke PDF
def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Executive Dashboard Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, insight)
    pdf.output("dashboard_report.pdf")
    st.success("Laporan berhasil diekspor sebagai dashboard_report.pdf")

if st.button("📤 Ekspor Insight ke PDF"):
    export_to_pdf()
