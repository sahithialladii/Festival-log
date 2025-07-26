# import streamlit as st
# from PIL import Image
# import os
# import pandas as pd
# from utils import translate_text, extract_keywords
# from db import init_db, insert_entry
# import sqlite3

# # Initialize DB
# init_db()

# # Set page config
# st.set_page_config(page_title="Festival Log", layout="centered")

# # Custom Header
# st.markdown("""
#     <div style="text-align:center; padding: 1rem 0;">
#         <h1 style="color:#ff4b4b;"> Festival Log</h1>
#         <p style="font-size:18px; color:gray;">Preserve local culture by documenting festivals in your own words.</p>
#     </div>
# """, unsafe_allow_html=True)

# # Custom Background (optional aesthetic touch)
# st.markdown("""
#     <style>
#         .stApp {
#             background: linear-gradient(to right, #f9f9f9, #eef1ff);
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar navigation
# page = st.sidebar.selectbox(" Select a Page", ["Log Festival", "View Entries"])

# # Session state defaults
# if "translated" not in st.session_state:
#     st.session_state.translated = ""
# if "keywords_telugu" not in st.session_state:
#     st.session_state.keywords_telugu = ""

# # ---- Page 1: Log Festival ----
# if page == "Log Festival":
#     st.subheader(" Describe the Festival")

#     with st.container():
#         text_input = st.text_area(
#             "Festival Description",
#             placeholder="E.g., Sankranti is celebrated with colorful rangoli, kites, and family gatherings..."
#         )

#         col1, col2 = st.columns(2)
#         with col1:
#             uploaded_image = st.file_uploader(" Upload Image", type=["jpg", "jpeg", "png"])
#         with col2:
#             if uploaded_image:
#                 st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

#     st.markdown("---")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button(" Analyze"):
#             if text_input:
#                 st.subheader(" Translated Text (Telugu):")
#                 translated = translate_text(text_input, target_lang='te')
#                 st.session_state.translated = translated
#                 st.write(translated)

#                 st.subheader(" Keywords Extracted:")
#                 keywords = extract_keywords(text_input)
#                 keywords_telugu = [translate_text(word, target_lang='te') for word in keywords]
#                 st.session_state.keywords_telugu = ", ".join(keywords_telugu)
#                 st.write(st.session_state.keywords_telugu)

#     with col2:
#         if st.button(" Save Entry"):
#             if not text_input:
#                 st.warning("Please write something about the festival.")
#             else:
#                 image_path = ""
#                 if uploaded_image is not None:
#                     os.makedirs("uploads", exist_ok=True)
#                     image_path = os.path.join("uploads", uploaded_image.name)
#                     with open(image_path, "wb") as f:
#                         f.write(uploaded_image.read())

#                 insert_entry(
#                     text=text_input,
#                     translated=st.session_state.translated,
#                     keywords_telugu=st.session_state.keywords_telugu,
#                     image_path=image_path
#                 )
#                 st.success(" Entry saved to the database!")

#     with col3:
#         if st.button(" Download Entry as CSV"):
#             entry = {
#                 "Text": text_input,
#                 "Translated": st.session_state.translated,
#                 "Keywords (Telugu)": st.session_state.keywords_telugu
#             }
#             df = pd.DataFrame([entry])
#             st.download_button(" Download CSV", data=df.to_csv(index=False), file_name="festival_log.csv", mime="text/csv")

# # ---- Page 2: View Entries ----
# elif page == "View Entries":
#     st.subheader(" Saved Festival Entries")

#     try:
#         conn = sqlite3.connect("festival_log.db")
#         df = pd.read_sql_query("SELECT * FROM festival_entries", conn)
#         conn.close()

#         if not df.empty:
#             for i, row in df.iterrows():
#                 with st.expander(f" Festival {i+1}"):
#                     st.markdown(f"**Original Description:** {row['text']}")
#                     st.markdown(f"**Translated (Telugu):** {row['translated']}")
#                     st.markdown(f"**Keywords (Telugu):** {row['keywords_telugu']}")
#                     if row['image_path'] and os.path.exists(row['image_path']):
#                         st.image(row['image_path'], use_column_width=True)
#                     else:
#                         st.markdown("_No image uploaded_")

#             st.markdown("---")
#             st.download_button(
#                 "\ud83d\udcc5 Download All Entries as CSV",
#                 data=df.to_csv(index=False),
#                 file_name="all_festival_entries.csv",
#                 mime="text/csv"
#             )
#         else:
#             st.info("No entries found yet. Try logging a new festival.")

#     except Exception as e:
#         st.error(f"An error occurred while loading the database: {e}")

# # Footer
# st.markdown("""
#     <hr>
#     <div style="text-align:center; font-size: 14px;">
#         Made with  during Summer of AI 2025 • Sahithi Alladi
#     </div>
# """, unsafe_allow_html=True)








import streamlit as st
from PIL import Image
import os
import pandas as pd
from utils import translate_text, extract_keywords
from db import init_db, insert_entry
import sqlite3

# Initialize DB
init_db()

# Set page config
st.set_page_config(page_title="Festival Log", layout="centered")

# ---- Custom CSS Styling ----
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #fdfbfb, #ebedee);
        }
        h1, h2, h3, .stMarkdown {
            color: #333333;
        }
        .main-container {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        }
        .upload-col {
            background-color: #f0f4ff;
            padding: 1rem;
            border-radius: 10px;
        }
        .css-1aumxhk {  /* Fix selectbox label if emoji is broken */
            white-space: nowrap;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <h1 style="color:#ff4b4b;">🎉 Festival Log</h1>
        <p style="font-size:18px; color:#555;">Preserve local culture by documenting festivals in your own words.</p>
    </div>
""", unsafe_allow_html=True)

# ---- Sidebar ----
page = st.sidebar.selectbox("📌 Select a Page", ["Log Festival", "View Entries"])

# ---- Session Defaults ----
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "keywords_telugu" not in st.session_state:
    st.session_state.keywords_telugu = ""

# ---- Page 1: Log Festival ----
if page == "Log Festival":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📝 Describe the Festival")

    text_input = st.text_area(
        "Festival Description",
        placeholder="E.g., Sankranti is celebrated with colorful rangoli, kites, and family gatherings..."
    )

    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    with col2:
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Analyze"):
            if text_input:
                st.subheader("🔤 Translated Text (Telugu):")
                translated = translate_text(text_input, target_lang='te')
                st.session_state.translated = translated
                st.write(translated)

                st.subheader("🗝️ Keywords Extracted:")
                keywords = extract_keywords(text_input)
                keywords_telugu = [translate_text(word, target_lang='te') for word in keywords]
                st.session_state.keywords_telugu = ", ".join(keywords_telugu)
                st.write(st.session_state.keywords_telugu)

    with col2:
        if st.button("💾 Save Entry"):
            if not text_input:
                st.warning("Please write something about the festival.")
            else:
                image_path = ""
                if uploaded_image is not None:
                    os.makedirs("uploads", exist_ok=True)
                    image_path = os.path.join("uploads", uploaded_image.name)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.read())

                insert_entry(
                    text=text_input,
                    translated=st.session_state.translated,
                    keywords_telugu=st.session_state.keywords_telugu,
                    image_path=image_path
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
            st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="festival_log.csv", mime="text/csv")

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Page 2: View Entries ----
elif page == "View Entries":
    st.subheader("📚 Saved Festival Entries")

    try:
        conn = sqlite3.connect("festival_log.db")
        df = pd.read_sql_query("SELECT * FROM festival_entries", conn)
        conn.close()

        if not df.empty:
            for i, row in df.iterrows():
                with st.expander(f"📖 Festival {i+1}"):
                    st.markdown(f"**📝 Original Description:** {row['text']}")
                    st.markdown(f"**🔤 Translated (Telugu):** {row['translated']}")
                    st.markdown(f"**🗝️ Keywords (Telugu):** {row['keywords_telugu']}")
                    if row['image_path'] and os.path.exists(row['image_path']):
                        st.image(row['image_path'], use_column_width=True)
                    else:
                        st.markdown("_No image uploaded_")

            st.markdown("---")
            st.download_button(
                "⬇️ Download All Entries as CSV",
                data=df.to_csv(index=False),
                file_name="all_festival_entries.csv",
                mime="text/csv"
            )
        else:
            st.info("📭 No entries found yet. Try logging a new festival.")

    except Exception as e:
        st.error(f"❌ An error occurred while loading the database: {e}")

# ---- Footer ----
st.markdown("""
    <hr>
    <div style="text-align:center; font-size: 14px;">
        Made with ❤️ during Summer of AI 2025 • Sahithi Alladi
    </div>
""", unsafe_allow_html=True)
