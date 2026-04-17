import streamlit as st

# 1. CẤU HÌNH TRANG (BẮT BUỘC NẰM DÒNG ĐẦU TIÊN)
st.set_page_config(page_title="Ecom Knowledge Hub", layout="wide", initial_sidebar_state="expanded")

# CSS PHONG CÁCH TỐI GIẢN
st.markdown("""
    <style>
    .stApp { background-color: #f5f5f7; font-family: "Helvetica Neue", Arial, sans-serif; }
    .apple-card {
        background-color: #ffffff; padding: 24px; border-radius: 18px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04); margin-bottom: 20px; border: 1px solid #e5e5e7;
    }
    .apple-card h3 { color: #1d1d1f; font-size: 20px; font-weight: 600; margin-top: 0; margin-bottom: 8px;}
    .apple-card p { color: #515154; font-size: 15px; line-height: 1.5; margin-bottom: 0;}
    .stTextInput input { border-radius: 12px !important; border: 1px solid #d2d2d7 !important; padding: 12px 16px !important; }
    [data-testid="stAppToolbar"] { visibility: hidden !important; }
    button[data-testid="stSidebarCollapse"] { visibility: visible !important; color: #1d1d1f !important; }
    footer { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# 2. CƠ SỞ DỮ LIỆU
hdsd_data = {
    "Khách Hàng Tiềm Năng": {
        "Phân công tự động (V2)": "Hệ thống tự động chia data cho Sale khi bấm check-in dựa trên ca làm việc Leader thiết lập. Chặn check-in nếu không có ca.",
        "Đơn vệ tinh 0đ": "Tự động tạo và cập nhật phiếu KHTN thành 'Đã hẹn thành công' khi CTV đẩy đơn cọc thành công mà chưa thanh toán.",
        "Thiết lập liên hệ lại": "Quy tắc tự động nhảy trạng thái 'Liên hệ lại' sau 15 phút nếu KH Không nghe máy lần 1. Leader có thể tùy chỉnh thời gian này."
    },
    "Tư Vấn & Tạo Đơn": {
        "Báo giá theo Nguy cơ/Nhóm bệnh": "Hỗ trợ xem nhanh danh sách vắc xin theo nhóm bệnh, in báo giá trực tiếp từ Sổ tiêm chủng hoặc màn hình tạo đơn ẩn danh.",
        "Tư vấn qua Sổ tiêm chủng V2": "Dựa trên lịch sử tiêm, hệ thống gợi ý phác đồ tiếp theo. Cho phép thêm trực tiếp vắc xin vào giỏ hàng từ giao diện sổ tiêm.",
        "Gói Gia Đình Phòng Vệ (Gia Đình Là Số 1)": "Thiết lập nhóm Gia đình, gộp chi tiêu tích lũy. Thao tác: Tạo mới, Thêm/Xóa thành viên, Đổi chủ hộ, Tư vấn đơn nhóm và Vô hiệu hóa.",
        "Điểm Gia Đình (Friend Sell)": "Sử dụng điểm sắp hết hạn của người thân. Ưu tiên: Trừ hết điểm cá nhân trước, sau đó trừ điểm gia đình theo thứ tự ngày hết hạn."
    },
    "Chăm Sóc & Call Center": {
        "Hiển thị tin nhắn BRC": "Màn hình Call Center hiển thị lịch sử gửi Broadcast. Nhận diện khách hàng có quan tâm tin nhắn hay không để sale bám sát kịch bản.",
        "Chăm sóc sau tiêm (SXH/VX Đặc biệt)": "Bác sĩ thiết lập danh sách Vắc xin đặc biệt. Sale Ecom gọi CSKH theo các mốc: Lần đầu, Lần 2, Lần cuối và cập nhật trạng thái xử lý.",
        "Xử lý Phản ứng sau tiêm (PUST)": "BS Ecom/Shop tiếp nhận, tạo phiếu theo dõi và cập nhật kết quả xử lý. Lưu vết toàn bộ triệu chứng để hỗ trợ mũi tiêm sau."
    },
    "Quản Lý Đơn & Xuất Off": {
        "Tool Xuất Off ECOM": "Quy trình xử lý đơn lỗi: Tạo phiếu -> Duyệt/Từ chối lần 1 -> Duyệt/Từ chối lần 2. Theo dõi minh bạch trạng thái Xuất off.",
        "Quy trình Trả Hàng": "TTP/Trưởng nhóm tiếp nhận trả hàng các vắc xin chưa tiêm. Hệ thống tự động tính Phí trả hàng, Phí gia hạn, Phí hoàn hủy (nếu có).",
        "Phiếu mua hàng B2B": "Thiết lập, chỉnh sửa, ngưng hiệu lực hoặc kích hoạt lại PMH dành riêng cho khách hàng doanh nghiệp hoặc đối tác.",
        "Xử lý mũi tiêm trễ hẹn": "Mũi trễ hẹn >31 ngày (với phác đồ <=91 ngày) sẽ bị thu phí gia hạn. Có thể xem danh sách và tạo đơn thu phí trực tiếp."
    },
    "Vận Hành Hệ Thống": {
        "Cảnh báo Tồn Kho V2": "Tự động quét số mũi hẹn đã thanh toán trong 3 ngày tới. Cảnh báo Sale nếu tồn kho nhỏ hơn số mũi cần trả khách để tránh overbook.",
        "Luồng xử lý khi TTTC Đóng Cửa": "Chặn tạo đơn/lịch hẹn vào ngày TTTC đóng. Tự động gửi SMS D-5, D-2 và kịch bản Voicebot dời lịch cho khách hàng.",
        "Chuẩn hóa Địa chỉ & TCQG": "Cập nhật tìm kiếm theo cấu trúc địa chỉ 2 cấp/3 cấp chuẩn Nhà Nước. Bắt buộc 4 trường thông tin mới khi TCQG nâng cấp.",
        "Điểm thưởng bán hàng (Hàng HOT)": "Hiển thị điểm Hx (VD: H5 = 5.000đ) trên Giỏ hàng. Tự động cộng/trừ điểm thưởng cho nhân viên khi chốt đơn/trả hàng thành công."
    },
    "App Khách Hàng (Mẹ & Bé)": {
        "Cẩm nang phát triển": "Theo dõi xu hướng chiều cao, cân nặng, kiểm tra kỹ năng phát triển của bé theo từng tháng tuổi.",
        "Đếm răng & Nhắc lịch": "Ghi nhận mốc mọc răng, đếm số răng sữa. Tích hợp AI tạo truyện, kể chuyện bằng giọng đọc của chính người thân."
    }
}

# 3. GIAO DIỆN CHÍNH
st.title("Ecom Knowledge Hub")
st.markdown("<p style='color: #86868b; font-size: 18px; margin-bottom: 30px;'>Trung tâm tra cứu Hướng dẫn sử dụng & Quy trình vận hành Ecom.</p>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Bạn cần hỗ trợ tính năng nào?", placeholder="Ví dụ: Xuất off, tồn kho, đơn vệ tinh, điểm gia đình...")

if search_query:
    st.markdown(f"**Kết quả tìm kiếm cho:** `{search_query}`")
    found = False
    for category, features in hdsd_data.items():
        for feat_name, feat_content in features.items():
            if search_query.lower() in feat_name.lower() or search_query.lower() in feat_content.lower():
                st.markdown(f"""
                <div class="apple-card">
                    <div style="font-size: 12px; font-weight: bold; color: #0066cc; margin-bottom: 4px; text-transform: uppercase;">{category}</div>
                    <h3>{feat_name}</h3>
                    <p>{feat_content}</p>
                </div>
                """, unsafe_allow_html=True)
                found = True
    if not found:
        st.warning("Không tìm thấy kết quả nào. Vui lòng thử từ khóa khác ngắn gọn hơn!")

else:
    with st.sidebar:
        st.markdown("## 📂 Danh mục tính năng")
        selected_category = st.radio("Chọn nhóm Màn hình:", list(hdsd_data.keys()))

    st.markdown(f"<h2 style='font-size: 24px; color: #1d1d1f; margin-top: 20px;'>{selected_category}</h2>", unsafe_allow_html=True)
    
    features_in_category = hdsd_data[selected_category]
    for feat_name, feat_content in features_in_category.items():
        st.markdown(f"""
        <div class="apple-card">
            <h3>✨ {feat_name}</h3>
            <p>{feat_content}</p>
        </div>
        """, unsafe_allow_html=True)
