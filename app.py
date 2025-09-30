import streamlit as st
from groq import Groq
import json
import os
import base64
from personalities import get_personality, get_personality_options

st.set_page_config(
    page_title="Chatbot Lịch Sử Việt Nam", 
    page_icon="📜", 
    layout="wide",
    initial_sidebar_state="expanded"
)

api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

def get_base64_background():
    with open('attached_assets/z7055735395182_b42d68da9f2bdba54b1a9c73c7841e86_1759215395425.jpg', 'rb') as f:
        return base64.b64encode(f.read()).decode()

def load_css():
    bg_image = get_base64_background()
    css = f"""
    <style>
    /* Vietnamese Historical Chatbot - Gemini Style with Blurred Background */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(8px);
        background: rgba(255, 255, 255, 0.85);
        z-index: 0;
        pointer-events: none;
    }}
    
    /* Main content on top of blur */
    .main {{
        position: relative;
        z-index: 1;
    }}

    /* Main content area */
    .main .block-container {{
        padding: 1rem 2rem;
        max-width: 1400px;
    }}

    /* Gemini-style Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 248, 248, 0.95) 100%);
        backdrop-filter: blur(10px);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        color: #202124;
    }}

    section[data-testid="stSidebar"] h2 {{
        color: #DC143C !important;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }}
    
    section[data-testid="stSidebar"] h3 {{
        color: #5f6368 !important;
        font-weight: 500;
        font-size: 0.9rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }}

    section[data-testid="stSidebar"] .stButton button {{
        background: white;
        color: #202124;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        font-weight: 400;
        transition: all 0.2s ease;
        margin: 0.2rem 0;
        padding: 0.6rem 1rem;
        text-align: left;
    }}

    section[data-testid="stSidebar"] .stButton button:hover {{
        background: #f8f9fa;
        border-color: #dadce0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        color: white;
        border: none;
        font-weight: 500;
    }}
    
    section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #c41230 0%, #7a0000 100%);
        box-shadow: 0 2px 6px rgba(220, 20, 60, 0.3);
    }}

    section[data-testid="stSidebar"] .stInfo {{
        background: linear-gradient(135deg, rgba(220, 20, 60, 0.1) 0%, rgba(139, 0, 0, 0.05) 100%);
        border-left: 4px solid #DC143C;
        color: #202124;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 0.85rem;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: rgba(0, 0, 0, 0.1) !important;
        margin: 1rem 0 !important;
    }}

    /* Chat container */
    .element-container {{
        margin-bottom: 0.5rem;
    }}

    /* Input area styling */
    .stTextInput input {{
        border: 2px solid #DC143C;
        border-radius: 24px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    .stTextInput input:focus {{
        border-color: #8B0000;
        box-shadow: 0 0 0 3px rgba(220, 20, 60, 0.2);
    }}

    /* Send button */
    .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        color: white;
        border: none;
        border-radius: 24px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(220, 20, 60, 0.3);
    }}

    .stButton button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.4);
    }}

    /* Spinner */
    .stSpinner > div {{
        border-top-color: #DC143C !important;
    }}

    /* Error messages */
    .stError {{
        background: linear-gradient(135deg, rgba(220, 20, 60, 0.15) 0%, rgba(220, 20, 60, 0.05) 100%);
        border-left: 4px solid #DC143C;
        border-radius: 8px;
    }}

    /* Remove default padding */
    .stMarkdown {{
        margin-bottom: 0;
    }}

    /* Smooth scrolling */
    html {{
        scroll-behavior: smooth;
    }}

    /* Ensure hamburger menu is visible */
    button[kind="header"] {{
        visibility: visible !important;
    }}
    
    /* Hide Streamlit footer only */
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

with open("data.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_personality_key" not in st.session_state:
    st.session_state.current_personality_key = "ly_thuong_kiet"

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
    
    current_personality = get_personality(st.session_state.current_personality_key)
    st.markdown("### 📖 Thông tin")
    st.info(f"**{current_personality.name}**\n\n{current_personality.description}")
    
    st.divider()
    
    st.markdown("### 💡 Câu hỏi gợi ý")
    character_questions = questions_data.get(st.session_state.current_personality_key, [])
    for i, question in enumerate(character_questions[:3]):
        if st.button(f"❓ {question[:40]}...", key=f"suggest_{i}", use_container_width=True):
            st.session_state.current_question = question
    
    st.divider()
    
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #8B0000; margin: 0; font-size: 2rem;">🏛️ {current_personality.name}</h1>
    <p style="color: #666; margin: 0.5rem 0;">Chatbot Lịch Sử Việt Nam</p>
</div>
""", unsafe_allow_html=True)

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
                    <div style="background: white;
                                color: #2c3e50; 
                                padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 18px 4px; 
                                max-width: 70%;
                                border: 2px solid #FFD700;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                line-height: 1.6;">
                        <strong style="color: #8B0000;">💬 {current_personality.name}:</strong><br><br>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

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

if send_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    
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
            
            ai_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
    
    st.rerun()
