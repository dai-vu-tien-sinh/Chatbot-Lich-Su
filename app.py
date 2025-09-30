
import streamlit as st
from groq import Groq
import json
import os
from personalities import get_personality, get_personality_options

# Khởi tạo client với GROQ_API_KEY từ environment variables hoặc secrets.toml
api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

# Load custom CSS
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load câu hỏi mẫu theo nhân vật từ data.json
with open("data.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

# Giao diện
st.set_page_config(page_title="Chatbot Lịch Sử Việt Nam", page_icon="📜", layout="wide")
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #8B0000; font-size: 3.5rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); margin-bottom: 0;">
        🏛️ CHATBOT LỊCH SỬ VIỆT NAM 🏛️
    </h1>
    <p style="font-size: 1.3rem; color: #DC143C; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        ✨ Trò chuyện với các anh hùng dân tộc ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Chọn nhân vật lịch sử
st.subheader("🎭 Chọn nhân vật lịch sử")
personality_options = get_personality_options()
selected_personality_key = st.selectbox(
    "Bạn muốn trò chuyện với ai?",
    options=[key for key, _ in personality_options],
    format_func=lambda x: next(name for key, name in personality_options if key == x),
    index=0
)

# Lấy thông tin nhân vật được chọn
current_personality = get_personality(selected_personality_key)

# Hiển thị thông tin nhân vật
st.info(f"**{current_personality.name}**: {current_personality.description}")

# Hiển thị lời chào từ nhân vật
if "current_personality_key" not in st.session_state or st.session_state.current_personality_key != selected_personality_key:
    st.session_state.current_personality_key = selected_personality_key
    st.session_state.show_greeting = True

if st.session_state.get("show_greeting", True):
    st.success(f"💬 **{current_personality.name}**: {current_personality.greeting}")

st.divider()

# Câu hỏi mẫu dành riêng cho nhân vật được chọn
st.subheader(f"📚 Câu hỏi gợi ý cho {current_personality.name}")
character_questions = questions_data.get(selected_personality_key, [])
selected_question = st.selectbox("Chọn câu hỏi mẫu:", [""] + character_questions)

# Nhập câu hỏi
prompt = st.text_area(
    "✏️ Hoặc nhập câu hỏi của bạn:", 
    value=selected_question if selected_question else "",
    placeholder=f"Hãy hỏi {current_personality.name} về lịch sử Việt Nam..."
)

# Gửi câu hỏi
if st.button(f"🧠 Hỏi {current_personality.name}"):
    if not prompt.strip():
        st.warning("❗ Bạn chưa nhập câu hỏi.")
    else:
        # Ẩn lời chào sau khi bắt đầu trò chuyện
        st.session_state.show_greeting = False
        
        with st.spinner(f"⏳ {current_personality.name} đang suy nghĩ..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": current_personality.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                st.success(f"✅ {current_personality.name} đã trả lời!")
                st.markdown(f"### 💬 {current_personality.name}:")
                
                # Hiển thị câu trả lời trong một container đẹp
                with st.container():
                    st.markdown(f"*{response.choices[0].message.content}*")
                    
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {str(e)}")
                st.info("💡 Hãy kiểm tra lại API key GROQ của bạn trong file secrets.toml")

# Thêm thông tin về app
with st.expander("ℹ️ Thông tin về app"):
    st.markdown("""
    **Chatbot Lịch Sử Việt Nam** cho phép bạn trò chuyện với các nhân vật lịch sử nổi tiếng:
    
    - 🏛️ **Lý Thường Kiệt**: Danh tướng triều Lý, tác giả "Nam quốc sơn hà"
    - 🌟 **Hồ Chí Minh**: Chủ tịch Hồ Chí Minh, lãnh tụ cách mạng
    - ⚔️ **Trần Hưng Đạo**: Đại tướng chống Mông Nguyên
    - 📚 **Học giả Lịch sử**: Nhà nghiên cứu khách quan
    
    Mỗi nhân vật có cách trả lời và phong cách riêng biệt dựa trên tính cách lịch sử của họ.
    """)
