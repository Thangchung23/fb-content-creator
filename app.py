import streamlit as st
from google import genai
import os

# Cấu hình tiêu đề trang web
st.set_page_config(page_title="AI Content Creator - Facebook", layout="wide")

st.title("🏗️🌿 AI Content Creator cho Facebook")
st.write("Hệ thống AI Agent tự động viết bài ngách Xây dựng - Mẹo vặt - Sức khỏe")

# Tên file ẩn dùng để lưu API Key trên máy của bạn
CONFIG_FILE = ".env_api_key"

# Đọc API Key đã lưu trước đó (nếu có)
saved_api_key = ""
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        saved_api_key = f.read().strip()

# Ô nhập API Key (nếu đã lưu sẽ tự động điền sẵn vào)
api_key_input = st.text_input("Nhập Gemini API Key của bạn:", value=saved_api_key, type="password")

# Nút lưu API Key để không phải nhập lại lần sau
if st.button("💾 Lưu API Key này lại"):
    if api_key_input.strip():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(api_key_input.strip())
        st.success("Đã lưu API Key thành công! Từ lần sau bạn không cần nhập lại nữa.")
    else:
        st.warning("Vui lòng nhập API Key trước khi lưu!")

if api_key_input:
    # Khởi tạo client khi có Key
    try:
        client = genai.Client(api_key=api_key_input)
        
        # Menu chọn ngách nội dung
        category = st.selectbox(
            "Chọn ngách nội dung:",
            (
                "🏠 Mẹo xây dựng nhà (Kinh nghiệm thực chiến, vật liệu, cấu trúc)",
                "🎒 Mẹo vặt đời sống (Tối ưu không gian, mẹo nhanh hữu ích)",
                "🥗 Mẹo sức khỏe từ thực phẩm (Dinh dưỡng lành mạnh, thực vật)"
            )
        )
        
        # Ô nhập ý tưởng thô của bạn
        specific_idea = st.text_area(
            "Nhập ý tưởng hoặc từ khóa bạn muốn viết hôm nay:", 
            placeholder="Ví dụ: Sai lầm khi đổ bê tông móng hoặc Mẹo chọn thực phẩm sạch..."
        )
        
        if st.button("🚀 Yêu cầu Agent viết bài"):
            if specific_idea.strip() == "":
                st.warning("Vui lòng nhập ý tưởng cụ thể trước khi bấm tạo!")
            else:
                with st.spinner("🤖 AI Agent đang phân tích và biên soạn bài viết chuẩn viral..."):
                    try:
                        system_instruction = """
                        Bạn là một Content Creator chuyên nghiệp, chuyên sáng tạo nội dung Facebook 
                        với các ngách: Kiến thức xây dựng nhà thực chiến, Mẹo vặt đời sống, và Mẹo sức khỏe thực phẩm.
                        Văn phong: Gần gũi, thực tế, sắc sảo, trình bày rõ ràng, ngắt đoạn ngắn, emoji hợp lý.
                        """
                        
                        prompt = f"""
                        Dựa vào lĩnh vực: '{category}' và ý tưởng cụ thể: '{specific_idea}', 
                        hãy viết hoàn chỉnh 1 bài đăng Facebook cuốn hút gồm:
                        1. Hook (Tiêu đề giật gân, gây tò mò).
                        2. Body (Nội dung chính chia thành các bước, gạch đầu dòng rõ ràng).
                        3. Tip độc quyền / Lưu ý vàng.
                        4. CTA (Kêu gọi bình luận/chia sẻ).
                        5. Gợi ý hình ảnh/video minh họa kèm theo.
                        """
                        
                        # Cập nhật sang mô hình chuẩn mới nhất theo thông báo hệ thống
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt,
                            config=genai.types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.7,
                            )
                        )
                        
                        st.success("✨ Đã hoàn thành bài viết! Bạn có thể copy nội dung bên dưới:")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Đã có lỗi xảy ra khi gọi AI: {e}")
                        
    except Exception as e:
        st.error(f"Lỗi khởi tạo Client: {e}")
else:
    st.info("💡 Vui lòng nhập Gemini API Key của bạn vào ô trên để mở khóa ứng dụng.")
