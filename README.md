
# 📜 Chatbot Lịch Sử Việt Nam

Một ứng dụng chatbot tương tác với các nhân vật lịch sử Việt Nam nổi tiếng! Trò chuyện với Hồ Chí Minh, Lý Thường Kiệt, Trần Hưng Đạo và nhiều hơn nữa. Sử dụng mô hình ngôn ngữ GROQ (LLaMA 3) và giao diện Streamlit.

## 🎭 Nhân vật có sẵn

- 🌟 **Hồ Chí Minh**: Chủ tịch Hồ Chí Minh, lãnh tụ vĩ đại của dân tộc
- 🏛️ **Lý Thường Kiệt**: Danh tướng triều Lý, tác giả "Nam quốc sơn hà"  
- ⚔️ **Trần Hưng Đạo**: Đại tướng chống quân Mông Nguyên
- 📚 **Học giả Lịch sử**: Nhà nghiên cứu lịch sử khách quan

Mỗi nhân vật có:
- **Câu hỏi gợi ý riêng biệt** phù hợp với bối cảnh lịch sử
- **Phong cách trả lời độc đáo** dựa trên tính cách lịch sử
- **Lời chào đặc trưng** phản ánh địa vị và thời đại

## 🚀 Chạy trên Replit

### 1. Fork/Clone dự án này
### 2. Thiết lập GROQ API Key

**Cách 1: Sử dụng Secrets (Khuyến nghị)**
1. Mở **Tools** → **Secrets**
2. Thêm secret mới:
   - **Key**: `GROQ_API_KEY`
   - **Value**: API key của bạn từ [console.groq.com](https://console.groq.com/keys)

**Cách 2: File secrets.toml**
Tạo file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_real_groq_api_key_here"
```

### 3. Chạy ứng dụng
Nhấn nút **Run** hoặc chạy:
```bash
streamlit run app.py
```

## 🧠 Công nghệ sử dụng

- **Frontend**: Streamlit
- **LLM**: GROQ (LLaMA 3-8B-8192)
- **Language**: Python 3.12
- **Hosting**: Replit

## 📂 Cấu trúc dự án

```
├── app.py                 # Ứng dụng Streamlit chính
├── personalities.py       # Định nghĩa các nhân vật lịch sử
├── data.json             # Câu hỏi gợi ý cho từng nhân vật
├── CUSTOMIZATION_GUIDE.md # Hướng dẫn thêm nhân vật mới
├── requirements.txt      # Dependencies Python
└── README.md            # Tài liệu này
```

## ✨ Tính năng

- 🎭 **4 nhân vật lịch sử** với tính cách riêng biệt
- 📚 **Câu hỏi gợi ý thông minh** cho từng nhân vật
- 💬 **Giao diện thân thiện** với Streamlit
- 🔒 **Bảo mật API key** qua Replit Secrets
- 🎨 **Dễ tùy chỉnh** - thêm nhân vật mới trong vài phút

## 🛠️ Tùy chỉnh

### Thêm nhân vật mới
Xem hướng dẫn chi tiết trong [CUSTOMIZATION_GUIDE.md](CUSTOMIZATION_GUIDE.md)

### Chỉnh sửa câu hỏi gợi ý
Sửa file `data.json` để thêm/sửa câu hỏi cho từng nhân vật

### Điều chỉnh phản hồi AI
Trong `app.py`, bạn có thể thay đổi:
- `temperature=0.7` (độ sáng tạo)
- `max_tokens=600` (độ dài phản hồi)

## 🔧 Phát triển local

```bash
# Clone repository
git clone <your-repo-url>
cd chatbot-lich-su-viet-nam

# Cài dependencies
pip install -r requirements.txt

# Thiết lập API key trong .streamlit/secrets.toml

# Chạy ứng dụng
streamlit run app.py
```

## 🤝 Đóng góp

1. Fork dự án này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án được phát hành dưới [MIT License](LICENSE).

## 📞 Liên hệ

Nếu bạn có câu hỏi hoặc đề xuất, hãy tạo issue trong repository này.

---

⭐ **Đừng quên star repo nếu bạn thấy hữu ích!**
