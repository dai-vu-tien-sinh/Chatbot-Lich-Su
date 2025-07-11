import streamlit as st
from groq import Groq
import json

# Sử dụng GROQ_API_KEY từ secrets.toml
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Load danh sách câu hỏi mẫu
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Giao diện người dùng
st.title("📜 Chatbot Lịch Sử Việt Nam")
st.markdown("💬 Hỏi bất kỳ điều gì về lịch sử Việt Nam!")

# Câu hỏi mẫu
selected_question = st.selectbox("📚 Chọn câu hỏi mẫu:", [""] + data)

# Input người dùng
prompt = st.text_area("✏️ Hoặc nhập câu hỏi của bạn:", value=selected_question if selected_question else "")

if st.button("🧠 Trả lời"):
    if not prompt.strip():
        st.warning("❗ Bạn chưa nhập câu hỏi.")
    else:
        with st.spinner("⏳ Đang xử lý..."):
            response = client.chat.completions.create(
                model="mistral-7b-8k",  # ✅ model hiện đang hoạt động
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý lịch sử Việt Nam, trả lời chính xác, thân thiện và dễ hiểu."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            st.success("✅ Đã có câu trả lời!")
            st.markdown("### 📝 Trả lời:")
            st.write(response.choices[0].message.content)
