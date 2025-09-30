import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import json
import os
import base64
import time
from html import escape
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
        padding: 1rem 2rem 0rem 2rem;
        max-width: 1400px;
    }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(139, 0, 0, 0.95) 0%, rgba(220, 20, 60, 0.95) 100%);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        color: white;
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #FFD700 !important;
        font-weight: 600;
    }}

    section[data-testid="stSidebar"] .stButton button {{
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        margin: 0.25rem 0;
    }}

    section[data-testid="stSidebar"] .stButton button:hover {{
        background: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(4px);
    }}

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {{
        background: rgba(255, 215, 0, 0.3);
        border: 2px solid #FFD700;
        font-weight: 600;
    }}

    section[data-testid="stSidebar"] .stInfo {{
        background: rgba(255, 255, 255, 0.15);
        border-left: 4px solid #FFD700;
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255, 255, 255, 0.3) !important;
        margin: 1.5rem 0 !important;
    }}

    /* Chat container */
    .element-container {{
        margin-bottom: 0rem;
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
    
    /* Hide the scroll iframe component */
    iframe[height="0"] {{
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
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
    
    /* Hide the default sidebar collapse arrow */
    button[kind="header"] {{
        display: none !important;
    }}
    
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}
    
    /* Ensure sidebar is visible by default */
    section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        position: relative !important;
        left: 0 !important;
        transform: none !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        width: 21rem !important;
    }}
    
    /* Style the toggle button */
    button[key="sidebar_toggle"] {{
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(220, 20, 60, 0.4) !important;
    }}
    
    button[key="sidebar_toggle"]:hover {{
        background: linear-gradient(135deg, #FF1744 0%, #DC143C 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.5) !important;
    }}
    
    /* Fixed bottom container for input area - like ChatGPT - edge to edge */
    #fixed-input-area {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: auto !important;
        box-sizing: border-box !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px) !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
        z-index: 1000 !important;
        border-top: 3px solid #DC143C !important;
    }}
    
    /* Inner container handles sidebar offset */
    #fixed-input-area .fixed-inner {{
        padding-left: calc(21rem + 1rem) !important;
        padding-right: 1rem !important;
    }}
    
    /* Hide the empty wrapper - doesn't contain Streamlit widgets */
    #fixed-input-area {{
        display: none !important;
    }}
    
    /* Make ONLY the chat form fixed at the bottom - constrain height to prevent overlay */
    div[data-testid="stForm"]:last-of-type {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1100 !important;
        height: auto !important;
        min-height: 0 !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
        border-top: 3px solid #DC143C !important;
        padding: 20px 0.5rem 0.5rem calc(21rem + 0.5rem) !important;
    }}
    
    /* Make sure sidebar has solid background and sits above input */
    section[data-testid="stSidebar"] {{
        background-color: #8B0000 !important;
        opacity: 1 !important;
        z-index: 1101 !important;
    }}
    </style>
    """
    st.markdown(css_with_bg, unsafe_allow_html=True)

load_css()

# Initialize sidebar toggle state
if "sidebar_hidden" not in st.session_state:
    st.session_state.sidebar_hidden = False

# Apply CSS based on sidebar state and add floating button when hidden
if st.session_state.sidebar_hidden:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    section[data-testid="stMain"] {
        margin-left: 0 !important;
    }
    section[data-testid="stMain"] > div {
        padding-top: 3.25rem !important;
    }
    #fixed-input-area .fixed-inner {
        padding-left: 1rem !important;
    }
    div[data-testid="stForm"]:last-of-type {
        padding-left: 1rem !important;
    }
    button[title="Mở menu"] {
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        right: 0 !important;
        z-index: 1200 !important;
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        color: white !important;
        border-radius: 0 !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 2px 8px rgba(220, 20, 60, 0.4) !important;
        border-bottom: 3px solid #8B0000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Show floating button to open sidebar when it's hidden
    if st.button("☰", key="open_sidebar", help="Mở menu"):
        st.session_state.sidebar_hidden = False
        st.rerun()
else:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

with open("data.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

# Conversation history persistence
HISTORY_FILE = "conversation_history.json"

def save_conversation_history():
    """Save current conversation to file"""
    try:
        # Load existing conversations
        all_conversations = load_all_conversations()
        
        # Get or create conversation ID (handle None or missing)
        if 'current_conversation_id' not in st.session_state or st.session_state.current_conversation_id is None:
            st.session_state.current_conversation_id = str(int(time.time() * 1000))
        
        conv_id = st.session_state.current_conversation_id
        
        # Update conversation
        all_conversations[conv_id] = {
            "id": conv_id,
            "personality": st.session_state.current_personality_key,
            "messages": st.session_state.messages,
            "timestamp": int(time.time()),
            "title": get_conversation_title(st.session_state.messages)
        }
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(all_conversations, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def load_all_conversations():
    """Load all conversations from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Handle old format
                if isinstance(data, dict) and "current_personality" in data:
                    # Convert old format to new
                    conv_id = str(int(time.time() * 1000))
                    return {
                        conv_id: {
                            "id": conv_id,
                            "personality": data.get("current_personality", "ly_thuong_kiet"),
                            "messages": data.get("messages", []),
                            "timestamp": int(time.time()),
                            "title": get_conversation_title(data.get("messages", []))
                        }
                    }
                return data
    except Exception as e:
        print(f"Error loading history: {e}")
    return {}

def get_conversation_title(messages):
    """Get conversation title from first user message"""
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:50]
            return title + "..." if len(msg["content"]) > 50 else title
    return "Cuộc trò chuyện mới"

def load_conversation_history():
    """Load most recent conversation"""
    conversations = load_all_conversations()
    if conversations:
        # Get most recent conversation
        latest = max(conversations.values(), key=lambda x: x.get("timestamp", 0))
        return latest["personality"], latest["messages"], latest["id"]
    return "ly_thuong_kiet", [], None

def auto_scroll_to_bottom():
    """Auto-scroll to bottom of page with smooth animation"""
    # Increment scroll counter to force script re-execution
    if 'scroll_counter' not in st.session_state:
        st.session_state.scroll_counter = 0
    st.session_state.scroll_counter += 1
    
    # Smooth animated scroll approach - hidden iframe
    components.html(
        f"""
        <div style="display: none; height: 0; width: 0; position: absolute; visibility: hidden;"></div>
        <script>
        var counter = {st.session_state.scroll_counter};
        
        function smoothScrollTo(element, target, duration) {{
            var start = element.scrollTop;
            var change = target - start;
            var startTime = performance.now();
            
            function animateScroll(currentTime) {{
                var elapsed = currentTime - startTime;
                var progress = Math.min(elapsed / duration, 1);
                
                // Easing function for smooth animation (ease-in-out)
                var easeProgress = progress < 0.5 
                    ? 2 * progress * progress 
                    : -1 + (4 - 2 * progress) * progress;
                
                element.scrollTop = start + (change * easeProgress);
                
                if (progress < 1) {{
                    requestAnimationFrame(animateScroll);
                }}
            }}
            
            requestAnimationFrame(animateScroll);
        }}
        
        function doScroll() {{
            var targetDoc = window.parent.document;
            
            // Find scrollable containers and animate them
            var selectors = [
                'div[data-testid="stAppViewContainer"]',
                'section[data-testid="stMain"]',
                '.main'
            ];
            
            selectors.forEach(function(selector) {{
                var elem = targetDoc.querySelector(selector);
                if (elem && elem.scrollHeight > elem.clientHeight) {{
                    smoothScrollTo(elem, elem.scrollHeight, 1200); // 1200ms = 1.2 seconds for slow smooth scroll
                }}
            }});
        }}
        
        // Try with delays to ensure content is loaded
        setTimeout(doScroll, 100);
        setTimeout(doScroll, 400);
        setTimeout(doScroll, 800);
        </script>
        """,
        height=0,
        scrolling=False
    )

# Initialize session state with saved history
if "messages" not in st.session_state:
    saved_personality, saved_messages, conv_id = load_conversation_history()
    st.session_state.messages = saved_messages
    st.session_state.current_personality_key = saved_personality
    st.session_state.current_conversation_id = conv_id
    # Trigger scroll if we loaded existing messages
    if len(saved_messages) > 0:
        st.session_state.should_scroll = True
elif "current_personality_key" not in st.session_state:
    st.session_state.current_personality_key = "ly_thuong_kiet"

with st.sidebar:
    st.markdown("## 🏛️ Lịch Sử Việt Nam")
    
    # Toggle button to hide sidebar
    if st.button("✕ Đóng menu" if not st.session_state.sidebar_hidden else "☰ Mở menu", 
                 key="sidebar_toggle", 
                 use_container_width=True,
                 type="secondary"):
        st.session_state.sidebar_hidden = not st.session_state.sidebar_hidden
        st.rerun()
    
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
                # Start a new conversation when switching personalities
                st.session_state.current_personality_key = key
                st.session_state.messages = []
                st.session_state.current_conversation_id = None  # Force new conversation ID
                st.rerun()
    
    st.divider()
    
    current_personality = get_personality(st.session_state.current_personality_key)
    st.markdown("### 📖 Thông tin")
    st.info(f"**{current_personality.name}**\n\n{current_personality.description}")
    
    st.divider()
    
    # Past conversations section
    st.markdown("### 💬 Lịch sử trò chuyện")
    all_convs = load_all_conversations()
    if all_convs:
        # Sort by timestamp (most recent first)
        sorted_convs = sorted(all_convs.values(), key=lambda x: x.get("timestamp", 0), reverse=True)
        
        # Show up to 10 most recent conversations
        for conv in sorted_convs[:10]:
            conv_id = conv["id"]
            title = conv.get("title", "Cuộc trò chuyện")
            is_current = st.session_state.get("current_conversation_id") == conv_id
            
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"{'📍 ' if is_current else '📄 '}{title[:35]}",
                    key=f"load_conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    # Load this conversation
                    st.session_state.messages = conv["messages"]
                    st.session_state.current_personality_key = conv["personality"]
                    st.session_state.current_conversation_id = conv_id
                    st.session_state.should_scroll = True
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_conv_{conv_id}", help="Xóa"):
                    # Delete conversation
                    del all_convs[conv_id]
                    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                        json.dump(all_convs, f, ensure_ascii=False, indent=2)
                    if conv_id == st.session_state.get("current_conversation_id"):
                        st.session_state.messages = []
                        st.session_state.current_conversation_id = None
                    st.rerun()
    else:
        st.info("Chưa có lịch sử trò chuyện")
    
    # New conversation button
    if st.button("➕ Cuộc trò chuyện mới", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.current_conversation_id = None
        st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Xóa tất cả lịch sử", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_conversation_id = None
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.rerun()

st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #8B0000; margin: 0; font-size: 2rem; text-shadow: 0 0 15px rgba(255, 255, 255, 1), 0 0 25px rgba(255, 255, 255, 0.8), 0 0 35px rgba(255, 255, 255, 0.6), 2px 2px 5px rgba(0, 0, 0, 0.4); font-weight: 700;">🏛️ {current_personality.name}</h1>
    <p style="color: #333; margin: 0.5rem 0; font-weight: 600; text-shadow: 0 0 10px rgba(255, 255, 255, 1), 0 1px 3px rgba(0, 0, 0, 0.3);">Chatbot Lịch Sử Việt Nam</p>
</div>
""", unsafe_allow_html=True)

# Suggested questions at the top
st.markdown('<div style="margin: 1rem 0;">', unsafe_allow_html=True)
st.markdown('<p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #666; font-weight: 600; text-shadow: 0 0 8px rgba(255, 255, 255, 0.9);">💡 Câu hỏi gợi ý:</p>', unsafe_allow_html=True)
character_questions = questions_data.get(st.session_state.current_personality_key, [])
cols = st.columns(3)
for i, question in enumerate(character_questions[:3]):
    with cols[i]:
        if st.button(f"❓ {question[:30]}...", key=f"suggest_q_top_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": question})
            save_conversation_history()
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
                    save_conversation_history()
                    st.session_state.should_scroll = True
                except Exception as e:
                    st.error(f"❌ Có lỗi xảy ra: {str(e)}")
                    save_conversation_history()
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

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
                <div style="display: flex; justify-content: flex-end; margin: 0.5rem 0 0 0;">
                    <div style="background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%); 
                                color: white; 
                                padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 4px 18px; 
                                max-width: 70%;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                overflow-wrap: anywhere;
                                word-break: break-word;
                                white-space: pre-wrap;
                                line-height: 1.6;">
                        {escape(message["content"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 0.5rem 0 0 0;">
                    <div style="background: linear-gradient(135deg, rgba(255, 248, 220, 0.95) 0%, rgba(255, 248, 220, 0.8) 100%);
                                color: #2c3e50; 
                                padding: 1rem 1.5rem; 
                                border-radius: 18px 18px 18px 4px; 
                                max-width: 70%;
                                border-left: 4px solid #FFD700;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                overflow-wrap: anywhere;
                                word-break: break-word;
                                white-space: pre-wrap;
                                line-height: 1.6;">
                        <strong style="color: #8B0000;">💬 {escape(current_personality.name)}:</strong><br><br>
                        {escape(message["content"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Add spacer for bottom padding (minimal gap + input box height)
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

# Scroll to bottom button (floating) - inject into parent document
components.html("""
<script>
(function() {
    var parentDoc = window.parent.document;
    var scrollContainer = null;
    var scrollButton = null;
    var scrollListener = null;
    
    function findScrollContainer() {
        var selectors = [
            'section[data-testid="stAppViewContainer"]',
            'div[data-testid="stAppViewContainer"]',
            'section[data-testid="stMain"]'
        ];
        
        for (var i = 0; i < selectors.length; i++) {
            var elem = parentDoc.querySelector(selectors[i]);
            if (elem && elem.scrollHeight > elem.clientHeight) {
                return elem;
            }
        }
        return null;
    }
    
    function scrollToBottom() {
        if (scrollContainer) {
            scrollContainer.scrollTo({
                top: scrollContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
    
    function checkScrollPosition() {
        if (!scrollContainer || !scrollButton) return;
        
        var scrollTop = scrollContainer.scrollTop;
        var scrollHeight = scrollContainer.scrollHeight;
        var clientHeight = scrollContainer.clientHeight;
        
        // Show button if more than 200px from bottom
        if (scrollHeight - scrollTop - clientHeight > 200) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
    
    function createButton() {
        // Remove old button if exists
        var oldButton = parentDoc.getElementById('scroll-to-bottom-btn');
        if (oldButton) {
            oldButton.remove();
        }
        
        // Create button container
        scrollButton = parentDoc.createElement('div');
        scrollButton.id = 'scroll-to-bottom-btn';
        scrollButton.style.cssText = 'position:fixed;bottom:80px;right:30px;z-index:999999;display:none;';
        
        // Create button element
        var btn = parentDoc.createElement('button');
        btn.innerHTML = '⬇️';
        btn.style.cssText = 'background:linear-gradient(135deg,#DC143C 0%,#8B0000 100%);color:white;border:none;border-radius:50%;width:50px;height:50px;font-size:24px;cursor:pointer;box-shadow:0 4px 12px rgba(220,20,60,0.5);transition:all 0.3s ease;';
        btn.onmouseover = function() { this.style.transform = 'scale(1.1)'; };
        btn.onmouseout = function() { this.style.transform = 'scale(1)'; };
        btn.onclick = scrollToBottom;
        
        scrollButton.appendChild(btn);
        parentDoc.body.appendChild(scrollButton);
    }
    
    function initialize() {
        scrollContainer = findScrollContainer();
        if (scrollContainer) {
            createButton();
            
            // Remove old listener if exists
            if (scrollListener) {
                scrollContainer.removeEventListener('scroll', scrollListener);
            }
            
            // Add scroll listener
            scrollListener = checkScrollPosition;
            scrollContainer.addEventListener('scroll', checkScrollPosition);
            
            // Initial check
            checkScrollPosition();
        }
    }
    
    // Initialize after delay
    setTimeout(initialize, 1000);
    
    // Re-initialize periodically for dynamic content
    setInterval(initialize, 2000);
})();
</script>
""", height=0)

# Fixed input area at bottom - wrap in explicit container
st.markdown('<div id="fixed-input-area"><div class="fixed-inner">', unsafe_allow_html=True)
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

st.markdown('</div></div></div>', unsafe_allow_html=True)  # Close input wrapper, fixed-inner, and fixed-input-area

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
            st.session_state.should_scroll = True
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
            save_conversation_history()  # Save even on error
    
    st.rerun()

# Auto-scroll to bottom after messages are added
if st.session_state.get('should_scroll', False):
    auto_scroll_to_bottom()
    st.session_state.should_scroll = False
