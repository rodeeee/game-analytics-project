from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd

# === Data Loading ===
df = pd.read_csv("../data/game_user_activity_clean.csv")

# === Statistik Dasar ===
mean_score = df['score'].mean()
mean_session = df['session_duration'].mean()
total_purchase = df['in_game_purchase'].sum()

genre_perf = df.groupby('game_genre')[['score', 'in_game_purchase']].mean().reset_index()
top_genre = genre_perf.loc[genre_perf['score'].idxmax(), 'game_genre']

device_perf = df.groupby('device')['session_duration'].mean().reset_index()
top_device = device_perf.loc[device_perf['session_duration'].idxmax(), 'device']

# === Laporan PDF ===
doc = SimpleDocTemplate("game_analysis_report.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("<b>Laporan Analisis Perilaku Pemain Game</b>", styles['Title']))
story.append(Spacer(1, 20))

story.append(Paragraph("📅 Periode Data: Data login dan aktivitas pemain dari file <i>game_user_activity_clean.csv</i>.", styles['Normal']))
story.append(Spacer(1, 15))

story.append(Paragraph("<b>Ringkasan Statistik</b>", styles['Heading2']))
data = [
    ["Rata-rata Durasi Main (menit)", f"{mean_session:.2f}"],
    ["Skor Rata-rata Pemain", f"{mean_score:.2f}"],
    ["Total Pembelian In-Game (USD)", f"{total_purchase:.2f}"]
]
t = Table(data, colWidths=[250, 150])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('GRID', (0,0), (-1,-1), 1, colors.grey),
    ('ALIGN', (1,0), (-1,-1), 'CENTER')
]))
story.append(t)
story.append(Spacer(1, 15))

story.append(Paragraph("<b>Temuan Utama</b>", styles['Heading2']))
story.append(Paragraph(f"- Genre dengan performa terbaik adalah <b>{top_genre}</b>.", styles['Normal']))
story.append(Paragraph(f"- Perangkat yang paling aktif digunakan adalah <b>{top_device}</b>.", styles['Normal']))
story.append(Paragraph(f"- Rata-rata skor pemain cukup tinggi ({mean_score:.2f}), menunjukkan tingkat kepuasan yang baik.", styles['Normal']))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>Insight dan Rekomendasi</b>", styles['Heading2']))
story.append(Paragraph("""
1. Fokuskan kampanye promosi ke genre dengan performa tinggi untuk meningkatkan engagement.  
2. Optimalkan pengalaman pengguna di perangkat yang paling sering digunakan.  
3. Kembangkan fitur sosial atau kompetitif untuk mempertahankan durasi bermain rata-rata yang sudah baik.  
4. Analisis lebih lanjut pembelian in-game per genre untuk strategi monetisasi lebih tepat sasaran.
""", styles['Normal']))

story.append(Spacer(1, 20))
story.append(Paragraph("<b>Kesimpulan</b>", styles['Heading2']))
story.append(Paragraph("""
Data menunjukkan tren positif dalam performa dan engagement pemain. Dengan pendekatan berbasis data ini,
tim pengembang dapat lebih memahami perilaku pengguna dan menyusun strategi produk yang lebih efektif.
""", styles['Normal']))

doc.build(story)
print("✅ Laporan selesai dibuat: game_analysis_report.pdf")
