
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
st.set_page_config(
    page_title="Chatbot Lịch Sử Việt Nam", 
    page_icon="📜", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_personality_key" not in st.session_state:
    st.session_state.current_personality_key = "ly_thuong_kiet"

# Sidebar for character selection
with st.sidebar:
    st.markdown("## 🏛️ Lịch Sử Việt Nam")
    st.markdown("### 🎭 Chọn nhân vật")
    
    personality_options = get_personality_options()
    
    for key, name in personality_options:
        if st.button(
            name, 
            key=f"btn_{key}",
            use_container_width=True,
            type="primary" if key == st.session_state.current_personality_key else "secondary"
        ):
            if key != st.session_state.current_personality_key:
                st.session_state.current_personality_key = key
                st.session_state.messages = []
                st.rerun()
    
    st.divider()
    
    # Character info
    current_personality = get_personality(st.session_state.current_personality_key)
    st.markdown("### 📖 Thông tin")
    st.info(f"**{current_personality.name}**\n\n{current_personality.description}")
    
    st.divider()
    
    # Suggested questions
    st.markdown("### 💡 Câu hỏi gợi ý")
    character_questions = questions_data.get(st.session_state.current_personality_key, [])
    for i, question in enumerate(character_questions[:3]):
        if st.button(f"❓ {question[:40]}...", key=f"suggest_{i}", use_container_width=True):
            st.session_state.current_question = question
    
    st.divider()
    
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat area
st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #8B0000; margin: 0; font-size: 2rem;">🏛️ {current_personality.name}</h1>
    <p style="color: #666; margin: 0.5rem 0;">Chatbot Lịch Sử Việt Nam</p>
</div>
""", unsafe_allow_html=True)

# Display chat messages
chat_container = st.container()
with chat_container:
    if len(st.session_state.messages) == 0:
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <h2 style="color: #DC143C;">👋 Xin chào!</h2>
            <p style="font-size: 1.1rem;">{current_personality.greeting}</p>
            <p style="margin-top: 1rem;">Hãy đặt câu hỏi để bắt đầu cuộc trò chuyện.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                    <div style="background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%); 
                                color: white; 
                                padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 4px 18px; 
                                max-width: 70%;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                    <div style="background: linear-gradient(135deg, rgba(255, 248, 220, 0.95) 0%, rgba(255, 248, 220, 0.8) 100%);
                                color: #2c3e50; 
                                padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 18px 4px; 
                                max-width: 70%;
                                border-left: 4px solid #FFD700;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                line-height: 1.6;">
                        <strong style="color: #8B0000;">💬 {current_personality.name}:</strong><br><br>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Input area at bottom
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Create columns for input area
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "Nhập câu hỏi của bạn...",
        key="user_input",
        placeholder=f"Hỏi {current_personality.name} về lịch sử Việt Nam...",
        label_visibility="collapsed",
        value=st.session_state.get("current_question", "")
    )
    if "current_question" in st.session_state:
        del st.session_state.current_question

with col2:
    send_button = st.button("📤 Gửi", use_container_width=True, type="primary")

# Handle send button
if send_button and user_input.strip():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner(f"⏳ {current_personality.name} đang suy nghĩ..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": current_personality.system_prompt},
                    *[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            # Add AI response to chat
            ai_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
    
    st.rerun()

# Handle Enter key
if user_input and not send_button:
    st.markdown("""
    <script>
    const input = window.parent.document.querySelector('input[type="text"]');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const button = window.parent.document.querySelector('button[kind="primary"]');
                if (button) button.click();
            }
        });
    }
    </script>
    """, unsafe_allow_html=True)
