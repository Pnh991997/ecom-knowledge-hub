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
    [data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important; border: 1px solid #1D1D1F !important; }

    /* Typo */
    h1 { color: #1D1D1F; font-size: 32px; font-weight: 700; margin-bottom: 0;}
    .file-title { color: #1D1D1F; font-size: 17px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
    .file-summary { color: #86868B; font-size: 13.5px; line-height: 1.4; margin-bottom: 15px; height: 58px; overflow: hidden; }
    
    /* Chỉnh nhãn tiêu đề cho Search & Filter */
    .custom-label { font-size: 15px; font-weight: 600; color: #1D1D1F; margin-bottom: 8px; display: block; }

    /* Nút tải */
    .stDownloadButton>button { background-color: #1D1D1F !important; color: #FFFFFF !important; border-radius: 10px !important; font-weight: 600 !important; width: 100%; border: none !important; }
    .stDownloadButton>button:hover { background-color: #434344 !important; }

    /* Search bar & Filter */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 12px !important; border: 1px solid #D2D2D7 !important; padding: 12px !important; background-color: #FFFFFF;}
    [data-testid="stAppToolbar"], header { visibility: hidden !important; }
    
    /* === NÚT AI NỔI === */
    .floating-bot-btn {
        position: fixed; bottom: 30px; right: 30px; background-color: #1D1D1F; color: #FFFFFF !important;
        border-radius: 30px; padding: 12px 24px; font-size: 15px; font-weight: 500;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2); text-decoration: none; z-index: 99999;
        display: flex; align-items: center; gap: 8px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .floating-bot-btn:hover { transform: scale(1.05); background-color: #434344; box-shadow: 0 12px 30px rgba(0,0,0,0.25); }
    .bot-icon-svg { width: 18px; height: 18px; fill: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# Nút nổi AI
st.markdown("""
    <a href="https://gemini.google.com/gem/1chGk0Edaxf4kuzU1FTkFBZN7S21UJcNP?usp=sharing" target="_blank" class="floating-bot-btn">
        <svg class="bot-icon-svg" viewBox="0 0 24 24">
            <path d="M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25L19 15z"/>
        </svg>
        Bot_Ecom Vac
    </a>
""", unsafe_allow_html=True)

# 2. HÀM XÓA DẤU (ĐÃ FIX TRIỆT ĐỂ CHỮ 'Đ')
def remove_accents(input_str):
    if not input_str: return ""
    s = str(input_str).replace("đ", "d").replace("Đ", "D")
    nfkd_form = unicodedata.normalize('NFKD', s)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# 3. DATABASE THÔNG MINH (Bổ sung thêm từ khóa để Quét chuẩn 100%)
file_metadata = [
    {"keys": ["tiềm năng", "tiem nang", "khtn"], "sum": "Quản lý phiếu KHTN V2, tự động chia data cho Sale và thiết lập gọi lại.", "tags": "khtn lead auto phan cong chia data goi lai telesale", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["0đ", "0d", "vệ tinh"], "sum": "Quy trình tự động cập nhật phiếu KHTN khi CTV Ecom đẩy đơn cọc 0đ.", "tags": "0 dong ctv ve tinh day don coc online", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["báo giá", "bao gia"], "sum": "Tra cứu nhanh danh sách vắc xin theo nhóm bệnh và in báo giá.", "tags": "nguy co in an list danh sach bang gia", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["sổ tiêm chủng", "so tiem chung"], "sum": "Gợi ý phác đồ tiêm tiếp theo dựa trên lịch sử tiêm thực tế của khách.", "tags": "stc phac do goi y lich su mui tiep theo", "cat": "🎯 KHTN & Tạo Đơn"},
    {"keys": ["gia đình", "gia dinh", "phòng vệ"], "sum": "Thiết lập nhóm gia đình phòng vệ, gộp tích lũy và đổi điểm.", "tags": "gdls1 nhom fsell f-sell f sell tich diem nguoi than", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["friend", "friendsell"], "sum": "Hướng dẫn sử dụng điểm F-Sell Gia đình để giảm giá đơn hàng.", "tags": "gdls1 nhom fsell f-sell f sell tich diem nguoi than", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["brc", "tin nhắn", "tin nhan"], "sum": "Xem lịch sử tin nhắn Broadcast gửi cho khách và đánh giá quan tâm.", "tags": "tin nhan zalo zns sms chatbot bot broadcast tong dai call center auto", "cat": "📞 CSKH & Call Center"},
    {"keys": ["chăm sóc", "cham soc", "đặc biệt", "sau tiêm"], "sum": "Theo dõi sức khỏe khách hàng sau tiêm vắc xin đặc biệt (SXH).", "tags": "csst goi dien hoi tham sxh dac biet sau tiem", "cat": "📞 CSKH & Call Center"},
    {"keys": ["phản ứng", "phan ung", "pust", "tiếp nhận", "tiep nhan"], "sum": "Tiếp nhận, tạo phiếu theo dõi phản ứng sau tiêm (PUST).", "tags": "tac dung phu soc phan ve trieu chung", "cat": "📞 CSKH & Call Center"},
    {"keys": ["xuất off", "xuat off"], "sum": "Công cụ tạo và duyệt phiếu Xuất Off cho các đơn hàng lỗi.", "tags": "tool don loi duyet tu choi huy don admin", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["trả hàng", "tra hang"], "sum": "Quy trình hoàn trả vắc xin và tính phí gia hạn, phí hoàn hủy.", "tags": "hoan tien phi gia han huy don", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["momo"], "sum": "Hướng dẫn khách quét mã thanh toán MoMo và luồng đẩy đơn tự động.", "tags": "thanh toan qrcode qr code vi dien tu online", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["tồn kho", "ton kho"], "sum": "Cảnh báo khi số lượng vắc xin không đủ trả mũi đã hẹn trong 3 ngày.", "tags": "het hang thieu hang tra mui 3 ngay canh bao", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["địa chỉ", "dia chi", "tcqg", "nâng cấp"], "sum": "Chuẩn hóa dữ liệu địa chỉ khách hàng theo cấu trúc chuẩn Nhà nước.", "tags": "3 cap 2 cap hanh chinh tcqg qg nang cap", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["trễ hẹn", "tre hen"], "sum": "Chính sách thu phí gia hạn hoặc vô hiệu hóa mũi tiêm khi trễ >31 ngày.", "tags": "phat thu phi gia han huy mui 31 ngay", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["đóng cửa", "dong cua", "tttc"], "sum": "Luồng chặn đơn và gửi tin nhắn/voicebot dời lịch khi TTTC đóng cửa.", "tags": "sms d-5 d-2 voicebot bot auto goi tu dong doi lich", "cat": "⚙️ Vận hành & Tồn kho"},
    {"keys": ["điểm thưởng", "diem thuong", "hot"], "sum": "Quy định cộng điểm Hx khi sale chốt đơn hàng HOT thành công.", "tags": "hx kpi thuong doanh thu hot", "cat": "💎 Chính sách & Khuyến mãi"},
    {"keys": ["mẹ và bé", "me_va_be", "me va be"], "sum": "Theo dõi phát triển, mọc răng của bé và tính năng AI kể truyện.", "tags": "app khach hang moc rang chieu cao can nang ai bot ke truyen", "cat": "👶 App Khách Hàng"},
    {"keys": ["b2b"], "sum": "Thiết lập, chỉnh sửa phiếu mua hàng dành riêng cho doanh nghiệp.", "tags": "pmh phieu mua hang doanh nghiep cong ty voucher b2b", "cat": "💎 Chính sách & Khuyến mãi"}
]

def get_file_info(file_name):
    # Thay thế các ký tự gạch nối để chuẩn hóa tên file trước khi kiểm tra
    clean_name = file_name.replace("-", " ").replace("_", " ").lower()
    fn_lower = remove_accents(clean_name)
    
    for data in file_metadata:
        for key in data["keys"]:
            # Quét trên cả chuỗi đã xóa dấu và chuỗi gốc
            if remove_accents(key) in fn_lower or key.lower() in clean_name:
                return data["sum"], data["tags"], data["cat"]
    return "Tài liệu hướng dẫn chi tiết quy trình vận hành trên hệ thống.", "tai lieu huong dan hdsd quy trinh", "📂 Tài liệu khác"

# HEADER
st.markdown("<h1> Ecom Operations Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868B; font-size: 16px;'>Trung tâm tra cứu Hướng dẫn sử dụng & Quy trình vận hành Ecom.</p>", unsafe_allow_html=True)

# TABS
tab1, tab2 = st.tabs(["📚 Kho Tài Liệu (HDSD)", "💡 FAQ Vận Hành"])

with tab1:
    st.write("")
    # BỘ LỌC VÀ SEARCH (SỬ DỤNG MARKDOWN ĐỂ ÉP HIỂN THỊ LABEL TÊN)
    c_search, c_filter = st.columns([2, 1])
    with c_search:
        st.markdown("<span class='custom-label'>🔍 Tìm kiếm tài liệu</span>", unsafe_allow_html=True)
        search = st.text_input("Search", placeholder="Nhập từ khóa và nhấn Enter (Ví dụ: gia dinh, bot, pust)...", label_visibility="collapsed")
    with c_filter:
        st.markdown("<span class='custom-label'>📂 Lọc theo danh mục</span>", unsafe_allow_html=True)
        cat_list = ["Tất cả danh mục", "🎯 KHTN & Tạo Đơn", "💎 Chính sách & Khuyến mãi", "⚙️ Vận hành & Tồn kho", "📞 CSKH & Call Center", "👶 App Khách Hàng", "📂 Tài liệu khác"]
        sel_cat = st.selectbox("Filter", cat_list, label_visibility="collapsed")
    
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
            summary, tags, cat = get_file_info(f)
            
            # Lọc theo nhóm
            if sel_cat != "Tất cả danh mục" and cat != sel_cat:
                continue
                
            # Lọc theo search (Quét tiếng Việt không dấu)
            if search_kw:
                f_norm = remove_accents(f)
                sum_norm = remove_accents(summary)
                tag_norm = remove_accents(tags)
                
                if search_kw not in f_norm and search_kw not in sum_norm and search_kw not in tag_norm:
                    continue
            
            display_files.append(f)

        if not display_files:
            st.info("Không tìm thấy tài liệu phù hợp. Bột thử gõ từ khóa khác xem sao nhé!")
        else:
            cols = st.columns(3)
            for i, f in enumerate(display_files):
                with cols[i % 3]:
                    with st.container(border=True):
                        # Cắt bỏ phần đuôi mở rộng khi hiển thị tên
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
