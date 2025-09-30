
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
st.set_page_config(page_title="Chatbot Lịch Sử Việt Nam", page_icon="📜", layout="centered")
st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h1 style="color: #8B0000; font-size: 3.2rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); margin-bottom: 0.5rem;">
        🏛️ CHATBOT LỊCH SỬ VIỆT NAM 🏛️
    </h1>
    <p style="font-size: 1.2rem; color: #DC143C; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        ✨ Trò chuyện với các anh hùng dân tộc ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Chọn nhân vật lịch sử
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎭 Chọn nhân vật lịch sử")
    personality_options = get_personality_options()
    selected_personality_key = st.selectbox(
        "Bạn muốn trò chuyện với ai?",
        options=[key for key, _ in personality_options],
        format_func=lambda x: next(name for key, name in personality_options if key == x),
        index=0,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### ")
    if st.button("🔄 Làm mới", use_container_width=True):
        st.session_state.show_greeting = True
        st.rerun()

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
st.markdown(f"### 📚 Đặt câu hỏi cho {current_personality.name}")

character_questions = questions_data.get(selected_personality_key, [])
selected_question = st.selectbox(
    "Chọn câu hỏi gợi ý hoặc tự nhập câu hỏi:",
    ["--- Chọn câu hỏi mẫu ---"] + character_questions,
    label_visibility="collapsed"
)

# Nhập câu hỏi
prompt = st.text_area(
    "Nhập câu hỏi của bạn:", 
    value=selected_question if selected_question and selected_question != "--- Chọn câu hỏi mẫu ---" else "",
    placeholder=f"Ví dụ: Hãy kể về trận chiến nổi tiếng nhất của {current_personality.name}...",
    height=120,
    label_visibility="collapsed"
)

# Gửi câu hỏi
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    ask_button = st.button(f"🧠 Hỏi {current_personality.name}", use_container_width=True, type="primary")

if ask_button:
    if not prompt.strip():
        st.warning("❗ Vui lòng nhập câu hỏi trước khi gửi.")
    else:
        # Ẩn lời chào sau khi bắt đầu trò chuyện
        st.session_state.show_greeting = False
        
        with st.spinner(f"⏳ {current_personality.name} đang suy nghĩ..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": current_personality.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                
                st.divider()
                
                # Hiển thị câu hỏi
                st.markdown(f"### ❓ Câu hỏi của bạn:")
                st.markdown(f"> {prompt}")
                
                # Hiển thị câu trả lời trong một container đẹp
                st.markdown(f"### 💬 Câu trả lời từ {current_personality.name}:")
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(255, 248, 220, 0.8) 0%, rgba(255, 248, 220, 0.4) 100%);
                                padding: 1.5rem;
                                border-radius: 12px;
                                border-left: 5px solid #FFD700;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                                margin: 1rem 0;">
                        <p style="color: #2c3e50; font-size: 1.05rem; line-height: 1.8; margin: 0; text-align: justify;">
                            {response.choices[0].message.content}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success(f"✅ Câu trả lời hoàn tất! Bạn có thể đặt thêm câu hỏi khác.")
                    
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {str(e)}")
                st.info("💡 Vui lòng kiểm tra kết nối mạng hoặc thử lại sau.")

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
