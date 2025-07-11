import streamlit as st
from groq import Groq
import json

# Khởi tạo client với GROQ_API_KEY từ secrets.toml
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Load câu hỏi mẫu từ data.json
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Giao diện
st.set_page_config(page_title="Chatbot Lịch Sử", page_icon="📜")
st.title("📜 Chatbot Lịch Sử Việt Nam")
st.markdown("Hỏi gì về lịch sử Việt Nam, mình sẽ trả lời!")

# Câu hỏi mẫu
selected_question = st.selectbox("📚 Chọn câu hỏi mẫu:", [""] + data)

# Nhập câu hỏi
prompt = st.text_area("✏️ Hoặc nhập câu hỏi của bạn:", value=selected_question if selected_question else "")

# Gửi câu hỏi
if st.button("🧠 Trả lời"):
    if not prompt.strip():
        st.warning("❗ Bạn chưa nhập câu hỏi.")
    else:
        with st.spinner("⏳ Đang suy nghĩ..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",  # ✅ model đang hoạt động trên Groq
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý lịch sử Việt Nam, trả lời ngắn gọn, chính xác, thân thiện và dễ hiểu."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            st.success("✅ Đã có câu trả lời!")
            st.markdown("### 📖 Trả lời:")
            st.write(response.choices[0].message.content)
