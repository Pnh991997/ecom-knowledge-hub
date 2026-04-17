import streamlit as st
import os
import base64

# 1. CẤU HÌNH & CSS "TẬN DIỆT" KHOẢNG TRỐNG (WOW UI)
st.set_page_config(page_title=" Ecom Support Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Xóa sạch padding/margin mặc định của Streamlit */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { height: 0px !important; display: none !important; }
    
    .stApp { background-color: #F5F5F7; font-family: "SF Pro Display", -apple-system, sans-serif; }

    /* Card thiết kế chuẩn Apple Store */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 20px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
        padding: 24px !important;
        transition: all 0.3s cubic-bezier(0, 0, 0.5, 1);
        height: 100% !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.1) !important;
        border: 1px solid #0071E3 !important;
    }

    /* Tiêu đề & Tóm tắt */
    .file-title { color: #1D1D1F; font-size: 18px; font-weight: 700; margin-bottom: 8px; line-height: 1.3; }
    .file-summary { color: #86868B; font-size: 14px; line-height: 1.5; margin-bottom: 15px; height: 42px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

    /* Nút bấm Apple Style */
    .stButton>button { background-color: #F5F5F7 !important; color: #0071E3 !important; border-radius: 12px !important; font-weight: 600 !important; border: none !important; width: 100%; }
    .stDownloadButton>button { background-color: #0071E3 !important; color: #FFFFFF !important; border-radius: 12px !important; font-weight: 600 !important; border: none !important; width: 100%; }
    
    /* Search Bar & Selectbox */
    .stTextInput input { border-radius: 15px !important; background-color: #E8E8ED !important; border: none !important; padding: 15px !important; }
    .stSelectbox div[data-baseweb="select"] { border-radius: 15px !important; background-color: #FFFFFF !important; }

    [data-testid="stAppToolbar"] { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 2. DATABASE TÓM TẮT (AI INSIGHTS)
# Tui đã đọc file của Bột và viết sẵn tóm tắt ở đây
summaries = {
    "tiềm năng": "Quản lý phiếu KHTN V2, tự động chia data cho Sale và thiết lập thời gian gọi lại.",
    "0đ": "Quy trình tự động cập nhật phiếu KHTN khi CTV Ecom đẩy đơn cọc 0đ thành công.",
    "báo giá": "Tra cứu nhanh danh sách vắc xin theo nhóm bệnh và in báo giá ngay tại quầy.",
    "sổ tiêm chủng": "Gợi ý phác đồ tiêm tiếp theo dựa trên lịch sử tiêm chủng thực tế của khách.",
    "gia đình": "Thiết lập nhóm gia đình phòng vệ, gộp tích lũy và đổi điểm F-Sell cho người thân.",
    "brc": "Xem lịch sử tin nhắn Broadcast gửi cho khách và đánh giá mức độ quan tâm.",
    "sau tiêm": "Theo dõi sức khỏe khách hàng sau tiêm vắc xin đặc biệt (Sốt xuất huyết...).",
    "xuất off": "Công cụ tạo và duyệt phiếu Xuất Off cho các đơn hàng lỗi cần xử lý thủ công.",
    "momo": "Hướng dẫn khách hàng quét mã thanh toán MoMo và luồng đẩy đơn tự động.",
    "tồn kho": "Cảnh báo khi số lượng vắc xin không đủ trả mũi cho khách đã hẹn trong 3 ngày.",
    "địa chỉ": "Chuẩn hóa dữ liệu địa chỉ khách hàng theo cấu trúc 2 cấp/3 cấp mới nhất.",
    "trễ hẹn": "Chính sách thu phí gia hạn hoặc vô hiệu hóa mũi tiêm khi khách trễ lịch >31 ngày.",
    "đóng cửa": "Luồng xử lý chặn đơn và tự động gửi tin nhắn dời lịch khi trung tâm tạm đóng cửa.",
    "điểm thưởng": "Quy định cộng điểm Hx (VD: H5 = 5.000đ) khi sale chốt đơn hàng HOT thành công.",
    "mẹ và bé": "Theo dõi xu hướng phát triển, mọc răng của bé và tính năng AI kể truyện."
}

def get_summary(file_name):
    for key, val in summaries.items():
        if key in file_name.lower(): return val
    return "Tài liệu hướng dẫn chi tiết về các tính năng và quy trình vận hành trên hệ thống."

# 3. PHÂN NHÓM TỰ ĐỘNG
categories = {
    "Tất cả tài liệu": [],
    "🎯 KHTN & Tạo Đơn": ["tiềm năng", "0đ", "báo giá", "sổ tiêm chủng"],
    "💎 Chính sách & Khuyến mãi": ["gia đình", "friend", "điểm thưởng", "momo"],
    "⚙️ Vận hành & Tồn kho": ["tồn kho", "xuất off", "trả hàng", "địa chỉ", "trễ hẹn", "đóng cửa"],
    "📞 CSKH & Call Center": ["brc", "chăm sóc", "sau tiêm", "pust"],
    "👶 App Khách Hàng": ["mẹ và bé", "me_va_be"],
    "📂 Tài liệu khác": []
}

# 4. GIAO DIỆN CHÍNH
st.markdown("<h1 style='margin-bottom:0px;'> Ecom Support Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868B; font-size: 18px; margin-top:0px;'>Tìm kiếm hướng dẫn & Quy trình vận hành.</p>", unsafe_allow_html=True)

# Thanh Filter & Search nằm ngang
c1, c2 = st.columns([2, 1])
with c1:
    search = st.text_input("", placeholder="Bạn muốn tìm gì? (momo, xuất off, điểm thưởng...)", label_visibility="collapsed")
with c2:
    # Fix lỗi trắng thanh lọc bằng cách set index mặc định
    cat_list = list(categories.keys())
    sel_cat = st.selectbox("", cat_list, index=0, label_visibility="collapsed")

# QUÉT FILE
try:
    files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
    files.sort()
except:
    files = []

# PHÂN LOẠI FILE VÀO NHÓM
categorized_data = {c: [] for c in categories}
for f in files:
    matched = False
    for c, keys in categories.items():
        if c == "Tất cả tài liệu" or c == "📂 Tài liệu khác": continue
        if any(k in f.lower() for k in keys):
            categorized_data[c].append(f)
            matched = True
            break
    if not matched:
        categorized_data["📂 Tài liệu khác"].append(f)

# HIỂN THỊ
display_files = []
if sel_cat == "Tất cả tài liệu":
    display_files = files
else:
    display_files = categorized_data[sel_cat]

# Lọc theo search
if search:
    display_files = [f for f in display_files if search.lower() in f.lower()]

if not display_files:
    st.info("Không tìm thấy tài liệu phù hợp.")
else:
    cols = st.columns(3)
    for i, f in enumerate(display_files):
        with cols[i % 3]:
            with st.container(border=True):
                name = f.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
                st.markdown(f"<div class='file-title'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='file-summary'>{get_summary(f)}</div>", unsafe_allow_html=True)
                
                c_v, c_d = st.columns(2)
                with c_v:
                    if f.endswith('.pdf'):
                        if st.button("👁️ Xem", key=f"v_{f}"):
                            st.session_state['view'] = f
                    else:
                        st.markdown("<p style='font-size:12px;color:#86868b;text-align:center;margin-top:10px;'>Ko hỗ trợ xem</p>", unsafe_allow_html=True)
                with c_d:
                    with open(f, "rb") as file_data:
                        st.download_button("⬇️ Tải", file_data, file_name=f, key=f"d_{f}")

# VIEW PDF (FIX TRẮNG MÀN HÌNH)
if st.session_state.get('view'):
    f_view = st.session_state['view']
    st.write("---")
    c_h1, c_h2 = st.columns([5, 1])
    with c_h1: st.markdown(f"### Đang xem: {f_view}")
    with c_h2: 
        if st.button("❌ Đóng"): 
            st.session_state['view'] = None
            st.rerun()
    
    with open(f_view, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000px" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)
