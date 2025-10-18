import matplotlib.pyplot as plt
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd

# === Data ===
df = pd.read_csv("../data/game_user_activity_clean.csv")

mean_score = df['score'].mean()
mean_session = df['session_duration'].mean()
total_purchase = df['in_game_purchase'].sum()

genre_perf = df.groupby('game_genre')[['score', 'in_game_purchase']].mean().reset_index()

# === Grafik: Rata-rata Skor per Genre ===
plt.figure(figsize=(6,4))
plt.bar(genre_perf['game_genre'], genre_perf['score'], color=['skyblue','royalblue','lightcoral','salmon','lightgreen'])
plt.title("Rata-rata Skor per Genre")
plt.xlabel("Genre")
plt.ylabel("Skor Rata-rata")
plt.tight_layout()
plt.savefig("plot_genre_score.png")
plt.close()

# === Laporan PDF ===
doc = SimpleDocTemplate("game_analysis_report_visual.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("<b>Laporan Analisis Perilaku Pemain Game (Versi Visual)</b>", styles['Title']))
story.append(Spacer(1, 20))

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
story.append(Spacer(1, 20))

story.append(Paragraph("<b>Visualisasi: Rata-rata Skor per Genre</b>", styles['Heading2']))
story.append(Image("plot_genre_score.png", width=400, height=300))
story.append(Spacer(1, 15))

story.append(Paragraph("<b>Insight Singkat</b>", styles['Heading2']))
story.append(Paragraph("""
Grafik di atas menunjukkan bahwa setiap genre memiliki performa skor yang relatif merata.
Hal ini bisa menunjukkan keseimbangan kualitas konten antar kategori,
namun perlu dianalisis lebih dalam genre mana yang berkontribusi paling besar terhadap monetisasi.
""", styles['Normal']))

doc.build(story)
print("✅ Laporan visual selesai dibuat: game_analysis_report_visual.pdf")
