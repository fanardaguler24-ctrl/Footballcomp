import streamlit as st

st.set_page_config(page_title="Football AI Comp", page_icon="⚽")
st.title("⚽ Otomatik Futbol Comp Yapıcı")

st.markdown("### Maç videosunu analiz et ve comp oluştur!")

link = st.text_input("Maç Linkini Buraya Yapıştır (YouTube/MP4):")
oyuncu = st.text_input("Odaklanılacak Oyuncu:", "Cristiano Ronaldo")

if st.button("Comp Oluştur ve Analiz Et ✨"):
    if link:
        with st.spinner(f"AI {oyuncu} isimli oyuncuyu arıyor..."):
            st.info("Video taranıyor, bu işlem vakit alabilir.")
            # Bu kısım ileride gerçek AI ile değişecek, şimdilik demo:
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            st.success("İşlem Başarıyla Tamamlandı!")
    else:
        st.error("Lütfen geçerli bir link girin!")
