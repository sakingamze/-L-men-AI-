import streamlit as st
from google import genai
import re

# --- Model ve client ---
client = genai.Client()
MODEL_NAME = "models/gemini-2.5-flash"

st.set_page_config(
    page_title="Lümen-AI ✨",
    page_icon="✨",
    layout="wide"
)

# --- Modern gri tonlar CSS ---
st.markdown("""
<style>
/* Genel arka plan ve yazılar */
body, .stApp {
    background-color: #2E2E2E;  /* koyu gri */
    color: #FFFFFF;              /* beyaz yazı */
    font-family: "Segoe UI", sans-serif;
}

/* Header ve başlıklar */
h1, h2, h3, h4 {
    color: #FFFFFF;
}

/* Textarea ve input kutusu */
.stTextArea textarea {
    background-color: #3C3C3C;  /* orta gri */
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 8px;
}

/* Button stil */
.stButton button {
    background-color: #5A5A5A;  /* gri ton */
    color: #FFFFFF;
    font-weight: bold;
    border-radius: 6px;
    padding: 6px 12px;
}
.stButton button:hover {
    background-color: #777777;
}

/* Markdown / Kod kutusu */
.stMarkdown, .stCodeBlock {
    background-color: #3C3C3C;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #555555;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.header("✨ Lümen-AI")
st.write("Kodunu paylaş, yapay zeka analiz etsin ve kısa, net öneriler sunsun.")

# --- Mentör profili ve öneri modu ---
mentor_level = st.selectbox(
    "Mentör Profili:",
    ["Junior", "Senior", "Security Expert", "Performance Guru"]
)
tip_mode = st.radio(
    "Öneri Modu:",
    ["Kısa ipucu", "Detaylı açıklama"]
)

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    code_input = st.text_area(
        "Analiz edilecek kodu buraya ekleyin:",
        height=400
    )
    analyze_button = st.button("🔍 Analiz Et ✨")

with col2:
    st.subheader("📝 Mentorun Analizi")

    if analyze_button:
        if code_input.strip():
            with st.spinner("Kodu inceliyorum, lütfen bekleyin..."):
                try:
                    # --- Kod dili algılama ---
                    if re.search(r"\bdef\b|\bimport\b", code_input):
                        code_lang = "Python"
                    elif re.search(r"\bfunction\b|console\.log", code_input):
                        code_lang = "JavaScript"
                    elif re.search(r"\bpublic class\b|\bSystem\.out\.println", code_input):
                        code_lang = "Java"
                    elif re.search(r"\busing\b|Console\.WriteLine", code_input):
                        code_lang = "C#"
                    else:
                        code_lang = "Bilinmiyor"

                    # --- Prompt ---
                    prompt = f"""
Sen tecrübeli bir yazılım mentörüsün ({mentor_level}) ve öneri modu {tip_mode}.

Aşağıdaki {code_lang} kodunu analiz et:
- Syntax ve mantık hatalarını tespit et
- Performans önerileri ver
- Güvenlik açıklarını kontrol et (SQL injection, XSS)
- Kod kalite puanı ver (1-10)
- Kısa veya detaylı açıklama yap (mod {tip_mode})
- Gerekirse refactor edilmiş örnek kod ver
Tüm açıklamalar Türkçe olsun

Kod:
{code_input}
"""

                    # --- Model çağrısı ---
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt
                    )

                    # --- Sonuçları göster ---
                    st.markdown("**📌 Analiz ve Öneriler:**")
                    st.code(response.text, language=code_lang.lower() if code_lang != "Bilinmiyor" else None)

                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("⚠️ Lütfen analiz edilecek bir kod girin.")
