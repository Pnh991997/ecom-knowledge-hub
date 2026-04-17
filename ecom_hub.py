import streamlit as st
import os
import unicodedata

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title=" Ecom Operations Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; }
    .stApp { background-color: #F5F5F7; font-family: "SF Pro Display", -apple-system, sans-serif; }
    
    /* Tabs chuẩn Apple */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #E8E8ED; padding: 4px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px !important; padding: 8px 16px !important; color: #1D1D1F !important; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important; }

    /* Card tài liệu */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important; border-radius: 16px !important;
        border: 1px solid rgba(0,0,0,0.05) !important; box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        padding: 20px !important; height: 100% !important; transition: all 0.2s;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important; border: 1px solid #0071E3 !important; }

    /* Typo */
    h1 { color: #1D1D1F; font-size: 32px; font-weight: 700; margin-bottom: 0;}
    .file-title { color: #1D1D1F; font-size: 17px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
    .file-summary { color: #86868B; font-size: 13.5px; line-height: 1.4; margin-bottom: 15px; height: 58px; overflow: hidden; }

    /* Nút tải duy nhất */
    .stDownloadButton>button { background-color: #0071E3 !important; color: #FFFFFF !important; border-radius: 10px !important; font-weight: 600 !important; width: 100%; border: none !important; }
    .stDownloadButton>button:hover { background-color: #0077ED !important; }

    /* Search bar */
    .stTextInput input { border-radius: 12px !important; border: 1px solid #D2D2D7 !important; padding: 12px !important; }
    [data-testid="stAppToolbar"], header { visibility: hidden !important; }
    
    /* === NÚT AI SUPPORT NỔI (FLOATING BUTTON) === */
    .floating-bot-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #1a73e8 0%, #0071e3 100%);
        color: #ffffff !important;
        border-radius: 50px;
        padding: 14px 24px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 8px 24px rgba(26, 115, 232, 0.4);
        text-decoration: none;
        z-index: 99999;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 2px solid rgba(255,255,255,0.2);
    }
    .floating-bot-btn:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 28px rgba(26, 115, 232, 0.6);
        background: linear-gradient(135deg, #1557b0 0%, #005bb5 100%);
    }
    /* Icon nhấp nháy cho xịn */
    .bot-icon { animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.15); } 100% { transform: scale(1); } }
    </style>
""", unsafe_allow_html=True)

# Gắn mã HTML hiển thị nút bong bóng
st.markdown("""
    <a href="https://gemini.google.com/gem/1chGk0Edaxf4kuzU1FTkFBZN7S21UJcNP?usp=sharing" target="_blank" class="floating-bot-btn">
        <span class="bot-icon">✨</span> Hỏi Trợ lý AI
    </a>
""", unsafe_allow_html=True)

# 2. HÀM XỬ LÝ TÌM KIẾM TIẾNG VIỆT KHÔNG DẤU
def remove_accents(input_str):
    if not input_str: return ""
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# 3. DATABASE AI TÓM TẮT
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
    "điểm thưởng": "Quy định cộng điểm Hx khi sale chốt đơn hàng HOT thành công.",
    "mẹ và bé": "Theo dõi xu hướng phát triển, mọc răng của bé và tính năng AI kể truyện."
}

def get_summary(file_name):
    for key, val in summaries.items():
        if remove_accents(key) in remove_accents(file_name): return val
    return "Tài liệu hướng dẫn chi tiết về các tính năng và quy trình vận hành trên hệ thống."

# HEADER
st.markdown("<h1> Ecom Operations Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868B; font-size: 16px;'>Trung tâm Tri thức & Hỗ trợ Vận hành Hệ thống FPT Long Châu.</p>", unsafe_allow_html=True)

# 2 TABS CHÍNH
tab1, tab2 = st.tabs(["📚 Kho Tài Liệu (HDSD)", "💡 FAQ Vận Hành"])

# ================= TAB 1: KHO TÀI LIỆU =================
with tab1:
    st.write("")
    search = st.text_input("🔍", placeholder="Nhập từ khóa tìm kiếm (Ví dụ: gia dinh, momo, xuat off)...", label_visibility="collapsed")
    
    try:
        files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
        files.sort()
    except:
        files = []

    if not files:
        st.warning("⚠️ Chưa có file tài liệu. Hãy upload lên GitHub!")
    else:
        display_files = []
        search_kw = remove_accents(search)
        
        for f in files:
            name_kw = remove_accents(f)
            summary_kw = remove_accents(get_summary(f))
            if search_kw in name_kw or search_kw in summary_kw:
                display_files.append(f)

        if not display_files:
            st.info("Không tìm thấy tài liệu phù hợp.")
        else:
            cols = st.columns(3)
            for i, f in enumerate(display_files):
                with cols[i % 3]:
                    with st.container(border=True):
                        name = f.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
                        summary = get_summary(f)
                        
                        st.markdown(f"<div class='file-title'>{name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='file-summary'>{summary}</div>", unsafe_allow_html=True)
                        
                        with open(f, "rb") as file_data:
                            st.download_button("⬇️ Tải tài liệu", file_data, file_name=f, key=f"d_{f}")

# ================= TAB 2: FAQ VẬN HÀNH =================
with tab2:
    st.write("")
    st.markdown("### Các lỗi hệ thống thường gặp & Cách xử lý nhanh")
    with st.expander("1. Lỗi không áp dụng được Điểm F-Sell Gia đình?"):
        st.write("**Nguyên nhân:** Khách hàng chưa dùng hết điểm F-Sell cá nhân, hoặc người thân không có điểm sắp hết hạn trong 6 tháng.")
        st.write("**Cách xử lý:** Sale kiểm tra lại tab Điểm cá nhân, yêu cầu khách đổi hết điểm cá nhân trước mới được dùng điểm gia đình.")
    
    with st.expander("2. CTV Ecom đẩy đơn cọc 0đ nhưng phiếu KHTN không chuyển trạng thái?"):
        st.write("**Nguyên nhân:** Có thể CTV đẩy sai luồng thanh toán hoặc SĐT khách hàng không khớp với phiếu KHTN ban đầu.")
        st.write("**Cách xử lý:** Sale vào kiểm tra lại mã đơn hàng, nếu đúng lỗi do hệ thống thì chụp màn hình gửi cho bộ phận Vận hành.")
