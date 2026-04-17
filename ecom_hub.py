import streamlit as st
import os
import base64

# 1. CẤU HÌNH GIAO DIỆN (BẮT BUỘC ĐỂ TRÊN CÙNG)
st.set_page_config(page_title=" Ecom Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS CHUẨN APPLE STORE (HIỆU ỨNG & GRID)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { background-color: #FBFBFD; font-family: 'Inter', sans-serif; }
    
    /* Hero Section (Tiêu đề to canh giữa) */
    .hero { text-align: center; padding: 40px 0 30px 0; }
    .hero h1 { font-size: 52px; font-weight: 700; color: #1D1D1F; letter-spacing: -1.5px; margin-bottom: 10px; }
    .hero p { font-size: 22px; color: #86868B; font-weight: 500; }

    /* Thiết kế Card dạng lưới (Grid) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 24px !important;
        border: 1px solid rgba(0,0,0,0.04) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03) !important;
        padding: 24px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        height: 100%;
    }
    /* Hiệu ứng nảy (Wow) khi đưa chuột vào Card */
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(0,113,227,0.2) !important;
    }

    /* Typo trong Card */
    .card-title { font-size: 18px; font-weight: 600; color: #1D1D1F; line-height: 1.4; margin-bottom: 8px; text-transform: capitalize; height: 50px; overflow: hidden; }
    .card-meta { font-size: 14px; color: #86868B; font-weight: 500; margin-bottom: 20px;}

    /* Nút bấm phân cấp */
    .stButton>button { background-color: #F5F5F7 !important; color: #0071E3 !important; border-radius: 14px !important; font-weight: 600 !important; border: none !important; width: 100%; transition: 0.2s; }
    .stButton>button:hover { background-color: #E8E8ED !important; }
    .stDownloadButton>button { background-color: #0071E3 !important; color: #FFFFFF !important; border-radius: 14px !important; font-weight: 600 !important; border: none !important; width: 100%; }
    .stDownloadButton>button:hover { background-color: #0077ED !important; }

    /* Thanh tìm kiếm & Dropdown */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 14px !important; border: 1px solid #D2D2D7 !important; padding: 10px !important; font-size: 16px; background-color: #FFFFFF;}
    
    [data-testid="stAppToolbar"], footer, header { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 3. HÀM ĐỌC PDF (FIX LỖI TRẮNG MÀN HÌNH)
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Đổi sang thẻ object, nếu trình duyệt chặn sẽ báo lỗi cụ thể
    pdf_display = f'<object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="800px" style="border-radius: 16px; border: 1px solid #e5e5e7;"><p style="text-align:center; padding: 50px; color: #ff3b30;">Trình duyệt của bạn đang chặn hiển thị PDF ẩn. Vui lòng bấm nút TẢI XUỐNG bên dưới để xem.</p></object>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# 4. DANH MỤC LỌC THÔNG MINH
categories_keywords = {
    "Tất cả tài liệu": [],
    "🎯 Khách Hàng Tiềm Năng & Tạo Đơn": ["tiềm năng", "0đ", "báo giá", "sổ tiêm chủng", "gia đình", "friend"],
    "📞 Chăm Sóc Khách Hàng & Call Center": ["brc", "chăm sóc", "sau tiêm", "phản ứng", "pust"],
    "⚙️ Quản Lý Vận Hành & Tồn Kho": ["tồn kho", "xuất off", "trả hàng", "địa chỉ", "trễ hẹn", "đóng cửa", "điểm thưởng", "momo"],
    "👶 App Khách Hàng (Mẹ & Bé)": ["mẹ và bé", "me_va_be"]
}

# 5. HEADER (HERO SECTION)
st.markdown("""
<div class="hero">
    <h1>Ecom Support Hub</h1>
    <p>Trung tâm tài liệu & Quy trình vận hành Hệ thống</p>
</div>
""", unsafe_allow_html=True)

# 6. BỘ LỌC (FILTERS) VÀ TÌM KIẾM
col_search, col_filter = st.columns([2, 1])
with col_search:
    search_query = st.text_input("🔍", placeholder="Bạn cần tìm hướng dẫn gì? (VD: xuất off, tồn kho...)")
with col_filter:
    selected_category = st.selectbox("📂 Lọc theo Danh mục:", list(categories_keywords.keys()))

st.write("---")

# 7. QUÉT VÀ XỬ LÝ FILE
try:
    all_files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
    all_files.sort()
except:
    all_files = []

if not all_files:
    st.warning("⚠️ Chưa có file tài liệu nào. Bột nhớ upload lên GitHub nhé!")
else:
    # Lọc file
    filtered_files = []
    for file_name in all_files:
        # Lọc theo search bar
        if search_query and search_query.lower() not in file_name.lower():
            continue
        
        # Lọc theo Dropdown Category
        if selected_category != "Tất cả tài liệu":
            keywords = categories_keywords[selected_category]
            if not any(kw.lower() in file_name.lower() for kw in keywords):
                continue
                
        filtered_files.append(file_name)

    if not filtered_files:
        st.info("Không tìm thấy tài liệu phù hợp với bộ lọc hiện tại.")
    else:
        # 8. HIỂN THỊ DẠNG LƯỚI (GRID 3 CỘT NHƯ APP STORE)
        cols = st.columns(3) # Tạo 3 cột
        
        for index, file_name in enumerate(filtered_files):
            # Tính toán để rải đều Card vào 3 cột
            col = cols[index % 3] 
            
            display_name = file_name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
            file_ext = file_name.split('.')[-1].upper()
            
            with col:
                with st.container(border=True):
                    st.markdown(f"<div class='card-title'>{display_name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card-meta'>Định dạng: {file_ext}</div>", unsafe_allow_html=True)
                    
                    if file_ext == 'PDF':
                        if st.button("👁️ Xem ngay", key=f"view_{file_name}"):
                            st.session_state['viewing'] = file_name
                    else:
                        st.markdown("<p style='font-size:13px; color:#86868b; text-align:center; margin-bottom: 12px;'>Không hỗ trợ xem trực tiếp</p>", unsafe_allow_html=True)
                    
                    with open(file_name, "rb") as f:
                        st.download_button("⬇️ Tải xuống", data=f, file_name=file_name, key=f"dl_{file_name}")

        # Hiển thị View PDF nếu được bấm
        if st.session_state.get('viewing'):
            file_to_view = st.session_state['viewing']
            st.write("---")
            st.markdown(f"### Đang xem: {file_to_view}")
            if st.button("❌ Đóng tài liệu", type="primary"):
                st.session_state['viewing'] = None
                st.rerun()
            display_pdf(file_to_view)
