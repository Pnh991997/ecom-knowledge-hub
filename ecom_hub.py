import streamlit as st
import os

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

    /* Search bar & Filter */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 12px !important; border: 1px solid #D2D2D7 !important; padding: 12px !important; background-color: #FFFFFF;}
    [data-testid="stAppToolbar"], header { visibility: hidden !important; }
    
    /* === NÚT AI SUPPORT NỔI (THIẾT KẾ MỚI CHUẨN IOS) === */
    .floating-bot-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #1D1D1F !important;
        border-radius: 40px;
        padding: 8px 24px 8px 8px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        text-decoration: none;
        z-index: 99999;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 1px solid rgba(0,0,0,0.08);
    }
    .floating-bot-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.18);
    }
    .bot-icon {
        background: linear-gradient(135deg, #0071E3 0%, #47A1FF 100%);
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(0, 113, 227, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Nút nổi AI
st.markdown("""
    <a href="https://gemini.google.com/gem/1chGk0Edaxf4kuzU1FTkFBZN7S21UJcNP?usp=sharing" target="_blank" class="floating-bot-btn">
        <div class="bot-icon">🤖</div>
        <span>Bot_Ecom Vac</span>
    </a>
""", unsafe_allow_html=True)

# 2. DATABASE THÔNG MINH (Chính xác 100%)
file_metadata = [
    {"keys": ["tiềm năng", "tiem nang"], "sum": "Quản lý phiếu KHTN V2, tự động chia data cho Sale và thiết lập gọi lại.", "tags": "khtn lead auto phan cong chia data goi lai telesale", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["0đ", "0d"], "sum": "Quy trình tự động cập nhật phiếu KHTN khi CTV Ecom đẩy đơn cọc 0đ.", "tags": "0 dong ctv ve tinh day don coc online", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["báo giá", "bao gia"], "sum": "Tra cứu nhanh danh sách vắc xin theo nhóm bệnh và in báo giá.", "tags": "nguy co in an list danh sach bang gia", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["sổ tiêm chủng", "so tiem chung"], "sum": "Gợi ý phác đồ tiêm tiếp theo dựa trên lịch sử tiêm thực tế của khách.", "tags": "stc phac do goi y lich su mui tiep theo", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["gia đình", "gia dinh", "phòng vệ"], "sum": "Thiết lập nhóm gia đình phòng vệ, gộp tích lũy và đổi điểm.", "tags": "gdls1 nhom fsell f-sell f sell tich diem nguoi than", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["friend", "diem_gia_dinh"], "sum": "Hướng dẫn sử dụng điểm F-Sell Gia đình để giảm giá đơn hàng.", "tags": "gdls1 nhom fsell f-sell f sell tich diem nguoi than", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["brc", "tin nhắn"], "sum": "Xem lịch sử tin nhắn Broadcast gửi cho khách và đánh giá quan tâm.", "tags": "tin nhan zalo zns sms chatbot bot broadcast tong dai call center auto", "cat": "📞 CSKH & Call Center"},
    {"keys": ["chăm sóc", "cham soc", "đặc biệt"], "sum": "Theo dõi sức khỏe khách hàng sau tiêm vắc xin đặc biệt (SXH).", "tags": "csst goi dien hoi tham sxh dac biet", "cat": "📞 CSKH & Call Center"},
    {"keys": ["phản ứng", "phan ung", "pust"], "sum": "Tiếp nhận, tạo phiếu theo dõi phản ứng sau tiêm (PUST).", "tags": "tac dung phu soc phan ve trieu chung", "cat": "📞 CSKH & Call Center"},
    {"keys": ["xuất off", "xuat off"], "sum": "Công cụ tạo và duyệt phiếu Xuất Off cho các đơn hàng lỗi.", "tags": "tool don loi duyet tu choi huy don admin", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["trả hàng", "tra hang"], "sum": "Quy trình hoàn trả vắc xin và tính phí gia hạn, phí hoàn hủy.", "tags": "hoan tien phi gia han huy don", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["momo"], "sum": "Hướng dẫn khách quét mã thanh toán MoMo và luồng đẩy đơn tự động.", "tags": "thanh toan qrcode qr code vi dien tu online", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["tồn kho", "ton kho"], "sum": "Cảnh báo khi số lượng vắc xin không đủ trả mũi đã hẹn trong 3 ngày.", "tags": "het hang thieu hang tra mui 3 ngay canh bao", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["địa chỉ", "dia chi", "tcqg"], "sum": "Chuẩn hóa dữ liệu địa chỉ khách hàng theo cấu trúc chuẩn Nhà nước.", "tags": "3 cap 2 cap hanh chinh tcqg qg nang cap", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["trễ hẹn", "tre hen"], "sum": "Chính sách thu phí gia hạn hoặc vô hiệu hóa mũi tiêm khi trễ >31 ngày.", "tags": "phat thu phi gia han huy mui 31 ngay", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["đóng cửa", "dong cua"], "sum": "Luồng chặn đơn và gửi tin nhắn/voicebot dời lịch khi TTTC đóng cửa.", "tags": "sms d-5 d-2 voicebot bot auto goi tu dong doi lich", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["điểm thưởng", "diem thuong", "hot"], "sum": "Quy định cộng điểm Hx khi sale chốt đơn hàng HOT thành công.", "tags": "hx kpi thuong doanh thu hot", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["mẹ và bé", "me_va_be"], "sum": "Theo dõi phát triển, mọc răng của bé và tính năng AI kể truyện.", "tags": "app khach hang moc rang chieu cao can nang ai bot ke truyen", "cat": "👶 App Khách Hàng"},
    {"keys": ["b2b"], "sum": "Thiết lập, chỉnh sửa phiếu mua hàng dành riêng cho doanh nghiệp.", "tags": "pmh phieu mua hang doanh nghiep cong ty voucher b2b", "cat": "💎 Chính sách & Khuyến mãi"}
]

def get_file_info(file_name):
    fn_lower = file_name.lower()
    for data in file_metadata:
        for key in data["keys"]:
            if key in fn_lower:
                return data["sum"], data["tags"], data["cat"]
    return "Tài liệu hướng dẫn chi tiết quy trình vận hành trên hệ thống.", "tai lieu huong dan hdsd quy trinh", "📂 Tài liệu khác"

# HEADER (Sửa đúng Text yêu cầu)
st.markdown("<h1> Ecom Operations Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868B; font-size: 16px;'>Trung tâm tra cứu Hướng dẫn sử dụng & Quy trình vận hành Ecom.</p>", unsafe_allow_html=True)

# TABS
tab1, tab2 = st.tabs(["📚 Kho Tài Liệu (HDSD)", "💡 FAQ Vận Hành"])

with tab1:
    st.write("")
    # BỘ LỌC ĐÃ QUAY TRỞ LẠI
    c_search, c_filter = st.columns([2, 1])
    with c_search:
        search = st.text_input("🔍", placeholder="Nhập từ khóa liên quan (Ví dụ: bot, voicebot, f-sell, qrcode)...", label_visibility="collapsed")
    with c_filter:
        cat_list = ["Tất cả danh mục", "🎯 KHTN & Tạo Đơn", "💎 Chính sách & Khuyến mãi", "⚙️ Vận hành & Tồn kho", "📞 CSKH & Call Center", "👶 App Khách Hàng", "📂 Tài liệu khác"]
        sel_cat = st.selectbox("📂", cat_list, label_visibility="collapsed")
    
    try:
        files = [f for f in os.listdir(".") if f.endswith(('.pdf', '.pptx'))]
        files.sort()
    except:
        files = []

    if not files:
        st.warning("⚠️ Chưa có file tài liệu. Hãy upload lên GitHub!")
    else:
        display_files = []
        search_kw = search.lower()
        
        for f in files:
            summary, tags, cat = get_file_info(f)
            
            # Lọc theo nhóm
            if sel_cat != "Tất cả danh mục" and cat != sel_cat:
                continue
                
            # Lọc theo search
            if search_kw:
                if search_kw not in f.lower() and search_kw not in summary.lower() and search_kw not in tags:
                    continue
            
            display_files.append(f)

        if not display_files:
            st.info("Không tìm thấy tài liệu phù hợp.")
        else:
            cols = st.columns(3)
            for i, f in enumerate(display_files):
                with cols[i % 3]:
                    with st.container(border=True):
                        name = f.rsplit(".", 1)[0].replace("-", " ").replace("_", " ")
                        summary, _, _ = get_file_info(f)
                        
                        st.markdown(f"<div class='file-title'>{name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='file-summary'>{summary}</div>", unsafe_allow_html=True)
                        
                        with open(f, "rb") as file_data:
                            st.download_button("⬇️ Tải tài liệu", file_data, file_name=f, key=f"d_{f}")

with tab2:
    st.write("")
    st.markdown("### Các lỗi hệ thống thường gặp & Cách xử lý nhanh")
    with st.expander("1. Lỗi không áp dụng được Điểm F-Sell Gia đình?"):
        st.write("**Nguyên nhân:** Khách hàng chưa dùng hết điểm F-Sell cá nhân, hoặc người thân không có điểm sắp hết hạn trong 6 tháng.")
        st.write("**Cách xử lý:** Sale kiểm tra lại tab Điểm cá nhân, yêu cầu khách đổi hết điểm cá nhân trước mới được dùng điểm gia đình.")
    
    with st.expander("2. CTV Ecom đẩy đơn cọc 0đ nhưng phiếu KHTN không chuyển trạng thái?"):
        st.write("**Nguyên nhân:** Có thể CTV đẩy sai luồng thanh toán hoặc SĐT khách hàng không khớp với phiếu KHTN ban đầu.")
        st.write("**Cách xử lý:** Sale vào kiểm tra lại mã đơn hàng, nếu đúng lỗi do hệ thống thì báo kỹ thuật.")
