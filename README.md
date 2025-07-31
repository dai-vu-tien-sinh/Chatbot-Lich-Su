
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

#### 🔑 Bước 1: Lấy GROQ API Key
1. Truy cập [console.groq.com/keys](https://console.groq.com/keys)
2. Đăng nhập hoặc tạo tài khoản miễn phí
3. Nhấn **Create API Key**
4. Sao chép API key (bắt đầu bằng `gsk_`)

#### 🔒 Bước 2: Thêm API Key vào Replit

**Cách 1: Sử dụng Secrets (Khuyến nghị)**
1. Mở **Tools** → **Secrets** trong sidebar
2. Nhấn **+ New Secret**
3. Điền thông tin:
   - **Key**: `GROQ_API_KEY`
   - **Value**: API key bạn vừa sao chép (ví dụ: `gsk_abc123...`)
4. Nhấn **Add Secret**

**Cách 2: File secrets.toml**
Tạo file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

#### ⚠️ Khắc phục lỗi "GROQ_API_KEY not found"

Nếu gặp lỗi: `st.secrets has no key "GROQ_API_KEY"`, làm theo các bước sau:

1. **Kiểm tra Secrets đã được thêm chưa**:
   - Vào **Tools** → **Secrets**
   - Đảm bảo có key `GROQ_API_KEY` trong danh sách

2. **Restart ứng dụng**:
   - Nhấn **Stop** rồi **Run** lại
   - Hoặc dùng **Ctrl+C** trong console rồi chạy lại

3. **Kiểm tra chính tả**:
   - Key phải là `GROQ_API_KEY` (in hoa, có dấu gạch dưới)
   - Value phải bắt đầu bằng `gsk_`

4. **Nếu vẫn lỗi, thử cách 2**:
   - Tạo file `.streamlit/secrets.toml`
   - Thêm nội dung như mẫu trên

### 3. Chạy ứng dụng
Nhấn nút **Run** hoặc chạy:
```bash
streamlit run app.py
```

✅ **Thành công**: Khi thấy thông báo "You can now view your Streamlit app in your browser" và không có lỗi GROQ_API_KEY

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

## 🛠️ Khắc phục sự cố

### Lỗi thường gặp

**1. `KeyError: 'GROQ_API_KEY'`**
```
st.secrets has no key "GROQ_API_KEY"
```
**Giải pháp**: Làm theo hướng dẫn ở mục "Thiết lập GROQ API Key" ở trên

**2. `Invalid API key`**
```
401 Unauthorized
```
**Giải pháp**: 
- Kiểm tra API key có đúng định dạng `gsk_...` không
- Tạo API key mới tại [console.groq.com/keys](https://console.groq.com/keys)

**3. App không load được**
```
WebSocket onclose
```
**Giải pháp**: 
- Nhấn **Stop** rồi **Run** lại
- Kiểm tra console có lỗi gì không

**4. Không thể trò chuyện với nhân vật**
**Giải pháp**:
- Đảm bảo đã nhập câu hỏi
- Kiểm tra kết nối internet
- Thử restart app

## 📞 Liên hệ

Nếu bạn có câu hỏi hoặc đề xuất, hãy tạo issue trong repository này.

---

⭐ **Đừng quên star repo nếu bạn thấy hữu ích!**
