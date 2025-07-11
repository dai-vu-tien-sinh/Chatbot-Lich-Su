import streamlit as st
import openai
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📜 Chatbot Lịch Sử Việt Nam")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
titles = [item["title"] for item in data]
st.write("**Bạn có thể hỏi về:**", ", ".join(titles))

question = st.text_input("❓ Nhập câu hỏi:")
if st.button("Gửi") and question:
    context = ""
    for item in data:
        if item["title"].lower() in question.lower():
            context = item["content"]
            break

    prompt = (
        "Bạn là giáo viên dạy lịch sử Việt Nam.\n"
        f"Dưới đây là dữ liệu tham khảo:\n{context}\n\n"
        f"Câu hỏi: {question}\n"
        "Trả lời ngắn gọn, dễ hiểu."
    )

    with st.spinner("Đang xử lý..."):
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        st.success("✅ Trả lời:")
        st.write(resp.choices[0].message["content"])
