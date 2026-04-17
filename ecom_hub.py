import streamlit as st
import os
import base64

# 1. CẤU HÌNH GIAO DIỆN CHUẨN APPLE SUPPORT
st.set_page_config(page_title=" Ecom Knowledge Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Font chữ San Francisco chuẩn Apple & Nền xám nhạt */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color: #F5F5F7; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Ẩn thanh công cụ rườm rà */
    [data-testid="stAppToolbar"], footer, header { visibility: hidden !important; }

    /* Thiết kế Card trắng bo góc, đổ bóng mềm */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 18px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
        transform: translateY(-2px);
    }

    /* Tiêu đề & Text */
    h1 { color: #1D1D1F !important; font-weight: 700 !important; font-size: 36px !important; letter-spacing: -0.5px; }
    h2 { color: #1D1D1F !important; font-weight: 600 !important; font-size: 24px !important; margin-top: 20px;}
    .doc-title { color: #1D1D1F; font-size: 17px; font-weight: 600; margin-bottom: 5px; text-transform: capitalize; }
    .doc-type { color: #86868B; font-size: 13px; font-weight: 500; }

    /* Nút Xem (Secondary Button) */
    .stButton>button {
        background-color: #F5F5F7 !important; color: #0071E3 !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 10px 20px !important; width: 100%;
        transition: background-color 0.2s;
    }
    .stButton>button:hover { background-color: #E8E8ED !important; }

    /* Nút Tải (Primary Button) */
    .stDownloadButton>button {
        background-color: #0071E3 !important; color: #FFFFFF !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 10px 20px !important; width: 100%;
    }
    .stDownloadButton>button:hover { background-color: #0077ED !important; }

    /* Thanh tìm kiếm */
    .stTextInput input { border-radius: 12px !important; border: 1px solid #D2D2D7 !important; padding: 14px !important; font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

# 2. HÀM ĐỌC PDF TRỰC TIẾP TRÊN WEB
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Nhúng file PDF vào một khung iframe rộng
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" style="border-radius: 12px; border: 1px solid #e5e5e7;" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# 3. BỘ TỪ KHÓA ĐỂ PHÂN NHÓM TỰ ĐỘNG
categories_keywords = {
    "🎯 Khách Hàng Tiềm Năng & Tạo Đơn": ["tiềm năng", "0đ", "báo giá", "sổ tiêm chủng", "gia đình", "friend"],
    "📞 Chăm Sóc Khách Hàng & Call Center": ["brc", "chăm sóc", "sau tiêm", "phản ứng", "pust"],
    "⚙️ Quản Lý Vận Hành & Tồn Kho": ["tồn kho", "xuất off", "trả hàng", "địa chỉ", "trễ hẹn", "đóng cửa", "điểm thưởng", "momo"],
    "👶 App Khách Hàng (Mẹ & Bé)": ["mẹ và bé", "me_va_be"]
}

st.title(" Ecom Support")
st.markdown("<p style='color: #86868B; font-size: 18px; margin-bottom: 30px;'>Trung tâm trợ giúp & Tài liệu vận hành nội bộ.</p>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Tìm kiếm tài liệu hỗ trợ", placeholder="Ví dụ: Xuất off, tồn kho, đơn vệ tinh...")
st.write("---")

# 4. LUỒNG QUÉT VÀ PHÂN LOẠI FILE
try:
    all_files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
except:
    all_files = []

if not all_files:
    st.warning("⚠️ Bột ơi, hãy upload các file tài liệu lên GitHub nhé!")
else:
    # Gom file vào các nhóm dựa theo từ khóa trong tên file
    grouped_files = {cat: [] for cat in categories_keywords.keys()}
    grouped_files["📂 Tài liệu khác"] = []

    for file_name in all_files:
        if search_query and search_query.lower() not in file_name.lower():
            continue # Bỏ qua nếu không khớp tìm kiếm
        
        matched = False
        for cat, keywords in categories_keywords.items():
            if any(kw.lower() in file_name.lower() for kw in keywords):
                grouped_files[cat].append(file_name)
                matched = True
                break
        if not matched:
            grouped_files["📂 Tài liệu khác"].append(file_name)

    # 5. HIỂN THỊ GIAO DIỆN THEO TỪNG NHÓM
    for category, files in grouped_files.items():
        if files: # Chỉ hiển thị nhóm nào có tài liệu
            st.markdown(f"<h2>{category}</h2>", unsafe_allow_html=True)
            
            for file_name in files:
                display_name = file_name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
                file_ext = file_name.split('.')[-1].upper()
                
                with st.container(border=True):
                    # Chia cột: Tên tài liệu bên trái, Nút bấm bên phải
                    col1, col2, col3 = st.columns([5, 1.5, 1.5])
                    
                    with col1:
                        st.markdown(f"<div class='doc-title'>{display_name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='doc-type'>Tài liệu {file_ext}</div>", unsafe_allow_html=True)
                    
                    with col2:
                        # Chỉ hiển thị nút Xem nếu là file PDF
                        if file_ext == 'PDF':
                            if st.button("👁️ Xem tài liệu", key=f"view_{file_name}"):
                                st.session_state['viewing'] = file_name
                        else:
                            st.markdown("<p style='font-size:12px; color:#86868b; text-align:center; margin-top:10px;'>Phải tải về máy</p>", unsafe_allow_html=True)
                    
                    with col3:
                        with open(file_name, "rb") as f:
                            st.download_button("⬇️ Tải xuống", data=f, file_name=file_name, key=f"dl_{file_name}")
                
                # Nếu người dùng bấm "Xem tài liệu", hiển thị khung đọc PDF ngay bên dưới Card đó
                if st.session_state.get('viewing') == file_name:
                    st.markdown("<div style='margin-bottom: 30px;'>", unsafe_allow_html=True)
                    display_pdf(file_name)
                    if st.button("❌ Đóng tài liệu", key=f"close_{file_name}"):
                        st.session_state['viewing'] = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
