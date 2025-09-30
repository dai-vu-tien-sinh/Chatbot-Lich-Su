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
    css_with_bg = f"""
    <style>
    /* Custom styling for Vietnamese Historical Chatbot - Gemini Style */
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
        background: rgba(255, 255, 255, 0.94);
        z-index: -1;
    }}
    
    /* Glowing text effects for better readability */
    h1, h2, h3, h4, h5, h6 {{
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.9), 
                     0 0 20px rgba(255, 255, 255, 0.7),
                     0 0 30px rgba(255, 255, 255, 0.5),
                     2px 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    /* Glow effect for paragraphs and text */
    p, span, div {{
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.8),
                     0 1px 2px rgba(0, 0, 0, 0.2);
    }}

    /* Main content area */
    .main .block-container {{
        padding: 1rem 2rem;
        max-width: 1400px;
    }}

    /* Sidebar styling - Clean ChatGPT style */
    section[data-testid="stSidebar"] {{
        background: #f5f5f5 !important;
        box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        color: #2e2e2e;
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #2e2e2e !important;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }}

    section[data-testid="stSidebar"] .stButton button {{
        background: transparent;
        color: #2e2e2e;
        border: none;
        border-radius: 8px;
        font-weight: 400;
        font-size: 0.9rem;
        transition: all 0.15s ease;
        margin: 0.15rem 0;
        padding: 0.6rem 0.75rem;
        text-align: left;
    }}

    section[data-testid="stSidebar"] .stButton button:hover {{
        background: #e8e8e8;
    }}

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {{
        background: #e8e8e8;
        font-weight: 500;
    }}

    section[data-testid="stSidebar"] .stInfo {{
        background: #ffffff;
        border-left: 3px solid #2e2e2e;
        color: #2e2e2e;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 0.85rem;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: #e0e0e0 !important;
        margin: 1rem 0 !important;
    }}

    /* Chat container */
    .element-container {{
        margin-bottom: 0.5rem;
    }}

    /* Input area styling - Gemini style */
    .stTextInput input {{
        border: 1px solid #ddd;
        border-radius: 24px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}

    .stTextInput input:focus {{
        border-color: #8B0000;
        box-shadow: 0 0 0 2px rgba(220, 20, 60, 0.15);
        outline: none;
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

    /* Hide Streamlit header and footer */
    header[data-testid="stHeader"] {{
        display: none;
    }}
    footer {{visibility: hidden;}}
    
    /* Hide toolbar */
    .stAppToolbar {{
        display: none;
    }}
    
    /* Ensure sidebar is always visible */
    section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
    }}
    
    /* Make the last container (input area) fixed at bottom */
    .main .block-container > div:last-child {{
        position: fixed !important;
        bottom: 0 !important;
        left: 21rem !important;
        right: 0 !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
        z-index: 999999 !important;
        border-top: 3px solid #DC143C !important;
        max-height: 280px;
        overflow-y: auto;
    }}
    
    /* Add padding to main content to prevent overlap with fixed footer */
    .main .block-container {{
        padding-bottom: 320px !important;
    }}
    
    /* On mobile/narrow screens, adjust for no sidebar */
    @media (max-width: 768px) {{
        .main .block-container > div:last-child {{
            left: 0 !important;
        }}
    }}
    </style>
    """
    st.markdown(css_with_bg, unsafe_allow_html=True)

load_css()

with open("data.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

# Conversation history persistence
HISTORY_FILE = "conversation_history.json"

def save_conversation_history():
    """Save conversation history to file"""
    try:
        history_data = {
            "current_personality": st.session_state.current_personality_key,
            "messages": st.session_state.messages
        }
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def load_conversation_history():
    """Load conversation history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
                return history_data.get("current_personality", "ly_thuong_kiet"), history_data.get("messages", [])
    except Exception as e:
        print(f"Error loading history: {e}")
    return "ly_thuong_kiet", []

# Initialize session state with saved history
if "messages" not in st.session_state:
    saved_personality, saved_messages = load_conversation_history()
    st.session_state.messages = saved_messages
    st.session_state.current_personality_key = saved_personality
elif "current_personality_key" not in st.session_state:
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
                save_conversation_history()
                st.rerun()
    
    st.divider()
    
    current_personality = get_personality(st.session_state.current_personality_key)
    st.markdown("### 📖 Thông tin")
    st.info(f"**{current_personality.name}**\n\n{current_personality.description}")
    
    st.divider()
    
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        save_conversation_history()
        st.rerun()

st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #8B0000; margin: 0; font-size: 2rem; text-shadow: 0 0 15px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 0.8), 0 0 35px rgba(255, 255, 255, 0.6), 2px 2px 5px rgba(0, 0, 0, 0.4); font-weight: 700;">🏛️ {current_personality.name}</h1>
    <p style="color: #333; margin: 0.5rem 0; font-weight: 600; text-shadow: 0 0 10px rgba(255, 255, 255, 1), 0 1px 3px rgba(0, 0, 0, 0.3);">Chatbot Lịch Sử Việt Nam</p>
</div>
""", unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    if len(st.session_state.messages) == 0:
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem;">
            <div style="display: inline-block; background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%); 
                        color: white; 
                        padding: 1rem 2.5rem; 
                        border-radius: 50px; 
                        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.4);
                        margin-bottom: 2rem;">
                <h2 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 700;">👋 Xin chào!</h2>
            </div>
            <p style="font-size: 1.1rem; color: #FFD700; font-weight: 600; text-shadow: 0 0 10px rgba(255, 255, 255, 1), 0 1px 3px rgba(0, 0, 0, 0.25); line-height: 1.6; margin-top: 1.5rem;">{current_personality.greeting}</p>
            <p style="margin-top: 1rem; color: #444; font-weight: 500; text-shadow: 0 0 8px rgba(255, 255, 255, 0.9), 0 1px 2px rgba(0, 0, 0, 0.2);">Hãy đặt câu hỏi để bắt đầu cuộc trò chuyện.</p>
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

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Bottom container with input and sample questions - always at bottom
bottom_container = st.container()
with bottom_container:
    st.markdown("### 💡 Câu hỏi gợi ý")
    character_questions = questions_data.get(st.session_state.current_personality_key, [])
    cols = st.columns(3)
    for i, question in enumerate(character_questions[:3]):
        with cols[i]:
            if st.button(f"❓ {question[:30]}...", key=f"suggest_q_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": question})
                save_conversation_history()  # Save user message immediately
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
                        save_conversation_history()  # Save AI response
                    except Exception as e:
                        st.error(f"❌ Có lỗi xảy ra: {str(e)}")
                        save_conversation_history()  # Save even on error
                st.rerun()
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Nhập câu hỏi của bạn...",
                key="user_input",
                placeholder=f"Hỏi {current_personality.name} về lịch sử Việt Nam...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.form_submit_button("📤 Gửi", use_container_width=True, type="primary")
    
    st.markdown("""
    <style>
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 2px 8px rgba(220,20,60,.3) !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #FF1744 0%, #DC143C 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(220,20,60,.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

if send_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_conversation_history()  # Save user message immediately
    
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
            save_conversation_history()  # Save AI response
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
            save_conversation_history()  # Save even on error
    
    st.rerun()
