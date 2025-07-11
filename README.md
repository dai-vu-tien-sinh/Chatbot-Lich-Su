# 📜 Chatbot Lịch Sử Việt Nam (GROQ API)

Chatbot đơn giản trả lời các câu hỏi về lịch sử Việt Nam, sử dụng mô hình ngôn ngữ từ GROQ (LLaMA 3). Giao diện người dùng xây dựng bằng Streamlit.

---

## 🚀 Cách chạy local

### 1. Giải nén & chuyển vào thư mục

```bash
unzip chatbot_lich_su_groq.zip
cd chatbot_lich_su_groq
```

### 2. (Tuỳ chọn) Tạo môi trường ảo

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Cài thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 4. Thêm API key GROQ

Tạo file `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_live_your_real_groq_api_key_here"
```

Lấy key tại: https://console.groq.com/keys

### 5. Chạy app

```bash
streamlit run app.py
```

Sau đó truy cập: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Mô hình sử dụng

- `llama3-8b-8192` từ GROQ
- Trả lời ngắn gọn, thân thiện, dễ hiểu

---

## 📝 Tùy chỉnh

- Câu hỏi mẫu trong `data.json`
- API key trong `.streamlit/secrets.toml`
- Giao diện chính trong `app.py`

---

## 📦 Yêu cầu

- Python 3.8+
- Internet để truy cập API của GROQ

---

## 📬 Liên hệ


