import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np
import os

st.set_page_config(page_title="Otomatik Futbol AI", page_icon="⚽")
st.title("🤖 Yapay Zeka Otomatik Maç Kırpıcı")
st.write("Linki at, gerisini AI halletsin (Ses analizi ile golleri bulur).")

url = st.text_input("YouTube Maç/Highlight Linki:")
hassasiyet = st.slider("Hassasiyet (Ses Eşiği):", 0.1, 1.0, 0.5)

if st.button("Otomatik Comp Oluştur ✨"):
    if url:
        with st.status("AI Maçı İzliyor ve Dinliyor...", expanded=True) as status:
            # 1. Video İndirme
            st.write("📥 Video analiz için indiriliyor...")
            ydl_opts = {'format': 'best[ext=mp4]', 'outtmpl': 'mac.mp4', 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 2. Ses Analizi ile Önemli Anları Bulma
            st.write("🎧 Ses dalgaları taranıyor (Goller aranıyor)...")
            video = VideoFileClip("mac.mp4")
            audio = video.audio
            
            # Sesi parçalara böl ve yüksek sesli (coşkulu) anları bul
            duration = int(video.duration)
            step = 2 # Her 2 saniyede bir kontrol et
            important_moments = []
            
            for i in range(0, duration - 5, step):
                segment = audio.subclip(i, i+step)
                volume = np.max(segment.to_soundarray(fps=22050))
                if volume > (hassasiyet * 0.8): # Ses eşiği kontrolü
                    important_moments.append((max(0, i-5), min(duration, i+5)))

            # Çakışan anları birleştir
            st.write(f"✅ {len(important_moments)} adet önemli an tespit edildi!")
            
            # 3. Klipleri Kes ve Birleştir
            st.write("🎬 Video montajlanıyor...")
            final_clips = [video.subclip(start, end) for start, end in important_moments[:10]] # İlk 10 anı al
            if final_clips:
                final_video = concatenate_videoclips(final_clips)
                final_video.write_videofile("otomatik_comp.mp4", codec="libx264")
                status.update(label="İşlem Tamam!", state="complete")
                st.video("otomatik_comp.mp4")
            else:
                st.error("Hiç önemli an bulunamadı. Hassasiyeti düşürmeyi dene.")
    else:
        st.error("Lütfen bir link gir!")
