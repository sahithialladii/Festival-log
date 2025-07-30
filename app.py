import streamlit as st
from PIL import Image
import os
import pandas as pd
from utils import translate_text, extract_keywords
from db import init_db, insert_entry
import sqlite3
import os
os.environ["STREAMLIT_HOME"] = "./.streamlit"
os.makedirs("./.streamlit", exist_ok=True)


# Initialize DB
init_db()

# Page Configuration
st.set_page_config(page_title="Festival Log", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap');
        .stApp {
            background: linear-gradient(to right, #fff1eb, #ace0f9);
            font-family: 'Noto Sans Telugu', sans-serif;
        }
        .main-container {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        }
        h1, h2, h3, .stMarkdown {
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <h1 style="color:#ff4b4b;">🎉 Festival Log</h1>
        <p style="font-size:18px; color:#555;">తెలుగులో పండుగల జ్ఞాపకాలను రికార్డ్ చేయండి!</p>
    </div>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox("📌 Navigate", ["🎉 Festival Gallery", "📝 Upload Festival"])

# Session Defaults
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "keywords_telugu" not in st.session_state:
    st.session_state.keywords_telugu = ""

# Festival Gallery
if page == "🎉 Festival Gallery":
    st.title("📸 తెలుగు పండుగల గ్యాలరీ")
    try:
        conn = sqlite3.connect("festival_log.db")
        df = pd.read_sql_query("SELECT * FROM festival_entries", conn)
        conn.close()

        if not df.empty:
            for i, row in df.iterrows():
                with st.container():
                    cols = st.columns([1, 2])
                    with cols[0]:
                        if row['image_path']:
                            for img_path in row['image_path'].split(';'):
                                if os.path.exists(img_path):
                                    st.image(img_path, use_container_width=True)
                                else:
                                    st.image("default_festival.jpg", use_container_width=True)
                        else:
                            st.image("default_festival.jpg", use_container_width=True)
                    with cols[1]:
                        st.markdown(f"#### 🪔 {row['translated'][:30]}...")
                        st.markdown(f"**📝 వివరణ:** {row['translated']}")
                        st.markdown(f"**🔑 కీలకపదాలు:** {row['keywords_telugu']}")
                        st.markdown("---")

            st.download_button(
                "⬇️ Download All Entries as CSV",
                data=df.to_csv(index=False),
                file_name="all_festival_entries.csv",
                mime="text/csv"
            )
        else:
            st.info("⛔ ఇంకా పండుగల సమాచారం ఇవ్వలేదు. ఒకదాన్ని జోడించండి!")

    except Exception as e:
        st.error(f"❌ డేటాబేస్ లో లోపం: {e}")

# Upload Festival Page
elif page == "📝 Upload Festival":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📝 Describe the Festival")

    text_input = st.text_area("Festival Description (Any language)",
                               placeholder="E.g., Sankranti is celebrated with colorful rangoli...")

    uploaded_images = st.file_uploader("Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_images:
        for img in uploaded_images:
            st.image(img, caption="Uploaded Image", use_container_width=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Analyze"):
            if text_input:
                translated = translate_text(text_input, target_lang='te')
                st.session_state.translated = translated
                st.subheader("🔤 Translated Text (Telugu):")
                st.write(translated)

                keywords = extract_keywords(text_input)
                keywords_telugu = [translate_text(word, target_lang='te') for word in keywords]
                st.session_state.keywords_telugu = ", ".join(keywords_telugu)
                st.subheader("🗝️ Keywords Extracted (Telugu):")
                st.write(st.session_state.keywords_telugu)

    with col2:
        if st.button("💾 Save Entry"):
            if not text_input:
                st.warning("Please write something about the festival.")
            else:
                image_paths = []
                if uploaded_images:
                    os.makedirs("uploads", exist_ok=True)
                    for img in uploaded_images:
                        img_path = os.path.join("uploads", img.name)
                        with open(img_path, "wb") as f:
                            f.write(img.read())
                        image_paths.append(img_path)

                translated = translate_text(text_input, target_lang='te')
                keywords = extract_keywords(text_input)
                keywords_telugu = [translate_text(word, target_lang='te') for word in keywords]

                insert_entry(
                    text=text_input,
                    translated=translated,
                    keywords_telugu=", ".join(keywords_telugu),
                    image_path=';'.join(image_paths)
                )
                st.success("✅ Entry saved to the database!")

    with col3:
        if st.button("⬇️ Download Entry as CSV"):
            entry = {
                "Text": text_input,
                "Translated": st.session_state.translated,
                "Keywords (Telugu)": st.session_state.keywords_telugu
            }
            df = pd.DataFrame([entry])
            st.download_button("📥 Download CSV",
                               data=df.to_csv(index=False),
                               file_name="festival_log.csv",
                               mime="text/csv")

    st.markdown('</div>', unsafe_allow_html=True)

