import streamlit as st
import os

# 1. CẤU HÌNH GIAO DIỆN CHUẨN APPLE (SANG - XỊN - MỊN)
st.set_page_config(page_title=" Ecom Knowledge Hub", layout="wide")

st.markdown("""
    <style>
    /* Nền xám nhạt Apple và Font chữ chuyên nghiệp */
    .stApp { background-color: #f5f5f7; font-family: "SF Pro Display", -apple-system, sans-serif; }
    
    /* Thiết kế Card (Thẻ) bo góc, đổ bóng nhẹ */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #e5e5e7 !important;
        background-color: #ffffff !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }
    
    /* Nút bấm Apple Blue */
    .stDownloadButton button {
        background-color: #0071e3 !important;
        color: white !important;
        border-radius: 22px !important;
        border: none !important;
        padding: 6px 20px !important;
        font-weight: 500 !important;
        width: 100%;
    }
    .stDownloadButton button:hover { background-color: #0077ed !important; border: none !important; }
    
    /* Làm đẹp tiêu đề và thanh search */
    h1 { color: #1d1d1f; font-weight: 700; font-size: 32px !important; }
    .stTextInput input { border-radius: 12px !important; border: 1px solid #d2d2d7 !important; height: 45px; }
    
    /* Ẩn thanh công cụ rườm rà */
    [data-testid="stAppToolbar"] { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 2. GIAO DIỆN CHÍNH
st.title(" Ecom Knowledge Hub")
st.markdown("<p style='color: #86868b; font-size: 18px; margin-bottom: 25px;'>Tra cứu tài liệu hướng dẫn vận hành hệ thống RSA & App Long Châu.</p>", unsafe_allow_html=True)

# Thanh tìm kiếm thông minh
search_query = st.text_input("🔍 Bạn đang tìm hướng dẫn cho tính năng nào?", placeholder="Nhập từ khóa (VD: momo, xuất off, trả hàng, gia đình...)")

# 3. HỆ THỐNG QUÉT FILE TỰ ĐỘNG (KHÔNG CẦN NHẬP TÊN FILE THỦ CÔNG)
# Quét toàn bộ file trong thư mục GitHub
all_files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
all_files.sort()

if not all_files:
    st.info("👋 Bột ơi, hãy upload các file PDF/PPTX lên GitHub để hệ thống hiển thị nhé!")
else:
    # Lọc file theo tìm kiếm
    filtered_files = [f for f in all_files if search_query.lower() in f.lower()] if search_query else all_files
    
    if not filtered_files:
        st.warning(f"Không tìm thấy tài liệu nào khớp với từ khóa: '{search_query}'")
    else:
        # Hiển thị dạng Card
        for file_name in filtered_files:
            # Làm đẹp tên file để hiển thị (bỏ đuôi, bỏ dấu gạch ngang)
            display_name = file_name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
            
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"<div style='font-size: 19px; font-weight: 600; color: #1d1d1f;'>📄 {display_name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 13px; color: #86868b;'>Định dạng: {file_name.split('.')[-1].upper()}</div>", unsafe_allow_html=True)
                with col2:
                    with open(file_name, "rb") as f:
                        st.download_button(label="Mở File", data=f, file_name=file_name, key=file_name)

st.sidebar.markdown("###  Hướng dẫn")
st.sidebar.info("Hệ thống sẽ tự động hiển thị mọi file tài liệu Bột upload lên GitHub. Chỉ cần tìm kiếm và bấm 'Mở File' để xem chi tiết.")
