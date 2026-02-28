import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

st.set_page_config(page_title="Futbol Comp Maker", page_icon="⚽")
st.title("✂️ Çoklu Pozisyon Kesici ve Birleştirici")

url = st.text_input("YouTube Maç Linki:")
zamanlar = st.text_input("Kesilecek Saniyeler (Örn: 10-20, 50-60):", placeholder="10-20, 50-60")

if st.button("Comp'u Oluştur 🚀"):
    if url and zamanlar:
        with st.status("Video İşleniyor...", expanded=True) as status:
            st.write("📥 Video indiriliyor...")
            ydl_opts = {'format': 'best[ext=mp4]', 'outtmpl': 'mac.mp4', 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            st.write("✂️ Pozisyonlar kesiliyor...")
            video = VideoFileClip("mac.mp4")
            klipler = []
            
            # Zamanları parçala (10-20, 50-60 gibi)
            for aralik in zamanlar.split(','):
                bas, son = aralik.strip().split('-')
                klipler.append(video.subclip(int(bas), int(son)))
            
            st.write("🎬 Klipler birleştiriliyor...")
            final_video = concatenate_videoclips(klipler)
            final_video.write_videofile("final_comp.mp4", codec="libx264")
            
            status.update(label="Comp Hazır!", state="complete")
        
        st.video("final_comp.mp4")
        with open("final_comp.mp4", "rb") as f:
            st.download_button("📥 Videoyu İndir", f, file_name="futbol_comp.mp4")
    else:
        st.error("Lütfen link ve zaman aralıklarını girin!")
