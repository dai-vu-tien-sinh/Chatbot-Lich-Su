import streamlit as st
from groq import Groq
import json

# Dùng API key từ secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Load dữ liệu câu hỏi gợi ý
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Giao diện
st.title("📜 Chatbot Lịch Sử Việt Nam")
st.markdown("💬 Hỏi bất kỳ điều gì về lịch sử Việt Nam!")

# Hiển thị danh sách câu hỏi gợi ý
selected_question = st.selectbox("📚 Chọn câu hỏi mẫu:", [""] + data)

# Nếu người dùng chọn câu hỏi mẫu thì dùng làm prompt
prompt = st.text_area("✏️ Hoặc tự nhập câu hỏi:", value=selected_question if selected_question else "")

if st.button("🧠 Trả lời"):
    if not prompt.strip():
        st.warning("❗ Bạn chưa nhập câu hỏi.")
    else:
        with st.spinner("⏳ Đang suy nghĩ..."):
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",  # hoặc dùng "mistral-7b-8k" nếu bạn thích nhẹ
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý lịch sử Việt Nam, trả lời chính xác, thân thiện và dễ hiểu."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            st.success("✅ Đã có kết quả!")
            st.markdown("### 📝 Trả lời:")
            st.write(response.choices[0].message.content)
