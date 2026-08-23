# ============================================================
# CPI TRANSPORT FORECASTING DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CPI Transport Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
========================================================= */

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background: #edf6f6;
}

.block-container {
    max-width: 100% !important;
    padding-top: 1.2rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    padding-bottom: 2.5rem !important;
}

/* Ẩn toolbar mặc định */
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    width: 84px !important;
    min-width: 84px !important;
    max-width: 84px !important;

    background: #262631 !important;

    border-right: none !important;
}

section[data-testid="stSidebar"] > div {
    width: 84px !important;
    min-width: 84px !important;
    max-width: 84px !important;
}

section[data-testid="stSidebar"] .block-container {
    padding:
        18px 8px 15px 8px !important;
}

/* Ẩn nút collapse */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}


/* =========================================================
   LOGO TRONG SIDEBAR
========================================================= */

.sidebar-logo {
    width: 50px;
    height: 50px;

    margin: 4px auto 22px auto;

    border-radius: 50%;

    background: #ff7e67;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 15px;
    font-weight: 800;

    color: white;

    box-shadow:
        0 7px 20px rgba(255,126,103,.30);
}

.sidebar-line {
    height: 1px;
    width: 42px;

    margin: 0 auto 16px auto;

    background: rgba(255,255,255,.10);
}


/* =========================================================
   SIDEBAR BUTTON
========================================================= */

section[data-testid="stSidebar"]
div[data-testid="stButton"] {

    display: flex;
    justify-content: center;

    width: 100%;

    margin-bottom: 6px;
}

section[data-testid="stSidebar"]
div[data-testid="stButton"] button {

    width: 56px !important;
    height: 54px !important;

    min-width: 56px !important;
    min-height: 54px !important;

    padding: 0 !important;

    display: flex;
    justify-content: center;
    align-items: center;

    border-radius: 10px !important;

    border: none !important;

    box-shadow: none !important;

    transition: all .18s ease;
}

/* Menu chưa chọn */
section[data-testid="stSidebar"]
button[kind="secondary"] {

    background: transparent !important;

    color: #a4a5b1 !important;
}

/* Menu đang chọn */
section[data-testid="stSidebar"]
button[kind="primary"] {

    background: #353541 !important;

    color: #ff7e67 !important;
}

/* Hover */
section[data-testid="stSidebar"]
button:hover {

    background: #353541 !important;

    color: #ff7e67 !important;

    transform: translateY(-1px);
}

/* Material icon */
section[data-testid="stSidebar"]
span.material-symbols-rounded {

    font-size: 27px !important;
}

/* Ẩn chữ của button */
section[data-testid="stSidebar"]
div[data-testid="stButton"] p {

    font-size: 0 !important;
}


/* =========================================================
   TOP BAR
========================================================= */

.topbar {
    width: 100%;

    background: white;

    min-height: 74px;

    border-radius: 10px;

    padding: 13px 22px;

    box-sizing: border-box;

    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 25px;

    border: 1px solid #e9eeee;

    box-shadow:
        0 2px 8px rgba(39, 48, 66, .035);
}

.brand-area {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-mark {
    width: 43px;
    height: 43px;

    background: #292934;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    color: #ff7e67;

    font-weight: 900;
    font-size: 16px;
}

.brand-name {
    color: #292934;

    font-size: 17px;

    font-weight: 800;

    letter-spacing: .2px;
}

.brand-sub {
    color: #a0a2aa;

    font-size: 10px;

    margin-top: 3px;

    letter-spacing: 1.2px;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.top-chip {
    border-radius: 22px;

    background: #f2f8f8;

    padding: 9px 15px;

    color: #626874;

    font-size: 12px;

    font-weight: 600;
}

.top-chip-accent {
    background: #fff0ec;

    color: #f17057;
}


/* =========================================================
   PAGE HEADER
========================================================= */

.page-head {
    display: flex;

    align-items: flex-end;

    justify-content: space-between;

    margin-bottom: 20px;
}

.breadcrumb {
    font-size: 11px;

    font-weight: 600;

    color: #9297a0;

    text-transform: uppercase;

    letter-spacing: .7px;

    margin-bottom: 7px;
}

.page-title {
    font-size: 29px;

    line-height: 1;

    font-weight: 850;

    color: #292934;

    letter-spacing: -.5px;
}

.page-description {
    color: #8c9199;

    font-size: 12px;

    margin-top: 8px;
}


/* =========================================================
   KPI GRID
========================================================= */

.kpi-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0,1fr));

    gap: 16px;

    margin-bottom: 18px;
}

.kpi-card {

    min-height: 126px;

    background: white;

    border-radius: 9px;

    padding: 18px 19px;

    box-sizing: border-box;

    border: 1px solid #e7eded;

    box-shadow:
        0 2px 8px rgba(39,48,66,.035);
}

.kpi-top {

    display: flex;

    align-items: center;

    justify-content: space-between;
}

.kpi-label {

    color: #454852;

    font-size: 11px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: .5px;
}

.kpi-icon {

    width: 36px;
    height: 36px;

    border-radius: 50%;

    background: #292934;

    color: white;

    display: flex;

    align-items: center;

    justify-content: center;
}

.kpi-icon .material-symbols-rounded {

    font-size: 19px;
}

.kpi-value {

    color: #292934;

    font-size: 29px;

    line-height: 1;

    font-weight: 850;

    margin-top: 17px;
}

.kpi-note {

    color: #9a9fa7;

    font-size: 10px;

    margin-top: 9px;
}

.green-text {
    color: #64bd82;

    font-weight: 700;
}

.orange-text {
    color: #ff7e67;

    font-weight: 700;
}


/* =========================================================
   SECTION TITLE
========================================================= */

.section-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-top: 8px;

    margin-bottom: 11px;
}

.section-title {

    color: #292934;

    font-size: 15px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: .4px;
}

.section-note {

    color: #989da4;

    font-size: 11px;
}


/* =========================================================
   WHITE CONTAINERS
========================================================= */

[data-testid="stVerticalBlockBorderWrapper"] {

    background: white !important;

    border: 1px solid #e5ebeb !important;

    border-radius: 10px !important;

    box-shadow:
        0 2px 8px rgba(39,48,66,.035) !important;
}

[data-testid="stVerticalBlockBorderWrapper"]
> div {

    padding: 5px !important;
}


/* =========================================================
   DATA SOURCE STATUS
========================================================= */

.status-grid {

    display: grid;

    grid-template-columns:
        repeat(3, minmax(0,1fr));

    gap: 12px;
}

.status-card {

    min-height: 76px;

    background: white;

    border: 1px solid #e6ecec;

    border-radius: 8px;

    padding: 14px 16px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    box-sizing: border-box;
}

.status-name {

    color: #353741;

    font-size: 13px;

    font-weight: 750;
}

.status-sub {

    color: #a0a4ab;

    font-size: 10px;

    margin-top: 4px;
}

.status-done {

    background: #eaf8ee;

    color: #55a870;

    border-radius: 20px;

    padding: 6px 10px;

    font-size: 10px;

    font-weight: 700;
}

.status-wait {

    background: #fff0ec;

    color: #f27861;

    border-radius: 20px;

    padding: 6px 10px;

    font-size: 10px;

    font-weight: 700;
}


/* =========================================================
   STREAMLIT INPUT
========================================================= */

div[data-baseweb="select"] > div {

    background: white !important;

    border-radius: 8px !important;

    border-color: #e5e9ec !important;
}

div[data-baseweb="input"] > div {

    background: white !important;

    border-radius: 8px !important;
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {

    background: white;

    border-radius: 9px;

    overflow: hidden;

    border: 1px solid #e5ebeb;
}


/* =========================================================
   METRIC
========================================================= */

[data-testid="stMetric"] {

    min-height: 112px;

    padding: 18px !important;

    background: white;

    border-radius: 9px;

    border: 1px solid #e5ebeb;

    box-shadow:
        0 2px 8px rgba(39,48,66,.035);
}

[data-testid="stMetricLabel"] {

    color: #777d86 !important;
}

[data-testid="stMetricValue"] {

    color: #292934 !important;

    font-size: 25px !important;

    font-weight: 800 !important;
}


/* =========================================================
   PRIMARY BUTTON
========================================================= */

button[kind="primary"] {

    background: #ff7e67 !important;

    border: none !important;

    color: white !important;

    border-radius: 8px !important;
}

button[kind="primary"]:hover {

    background: #f06f58 !important;
}


/* =========================================================
   INFO / WARNING
========================================================= */

[data-testid="stAlert"] {

    border-radius: 8px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1000px) {

    .kpi-grid {
        grid-template-columns:
            repeat(2, minmax(0,1fr));
    }

    .status-grid {
        grid-template-columns:
            repeat(2, minmax(0,1fr));
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
INTERIM_DIR = BASE_DIR / "data" / "interim"


# ============================================================
# 4. FILE CANDIDATES
#
# Nếu tên file của bạn khác thì chỉ cần thêm tên file vào
# danh sách tương ứng dưới đây.
# ============================================================

FILE_CANDIDATES = {

    "CPI giao thông": [
        "cpi_transport_monthly.csv",
        "cpi_transport.csv",
        "cpi_monthly.csv",
        "cpi_giao_thong_monthly.csv",
    ],

    "WTI": [
        "wti_crude_oil_monthly.csv",
        "wti_monthly.csv",
    ],

    "Brent": [
        "brent_crude_oil_monthly.csv",
        "brent_monthly.csv",
    ],

    "USD/VND": [
        "usd_vnd_monthly.csv",
        "usd_vnd.csv",
        "usd_vnd_exchange_rate_monthly.csv",
    ],
}


# ============================================================
# 5. DATA FUNCTIONS
# ============================================================

def find_data_file(source):

    candidates = FILE_CANDIDATES.get(source, [])

    # Tìm đúng tên trước
    for file_name in candidates:

        path = INTERIM_DIR / file_name

        if path.exists():
            return path

    # Nếu khác tên thì thử tìm theo keyword
    if INTERIM_DIR.exists():

        csv_files = list(INTERIM_DIR.glob("*.csv"))

        for path in csv_files:

            name = path.name.lower()

            if source == "WTI" and "wti" in name:
                return path

            if source == "Brent" and "brent" in name:
                return path

            if (
                source == "USD/VND"
                and "usd" in name
                and "vnd" in name
            ):
                return path

            if (
                source == "CPI giao thông"
                and "cpi" in name
            ):
                return path

    return None


@st.cache_data
def load_csv(path):

    try:

        return pd.read_csv(
            path,
            encoding="utf-8-sig",
        )

    except UnicodeDecodeError:

        return pd.read_csv(path)


def get_date_column(df):

    preferred = [
        "Date",
        "date",
        "MonthYear",
        "month_year",
        "Month",
        "month",
    ]

    # Tìm tên chính xác
    for col in preferred:

        if col in df.columns:
            return col

    # Tìm cột có chữ date/month
    for col in df.columns:

        lower = str(col).lower()

        if (
            "date" in lower
            or "month" in lower
            or "time" in lower
        ):
            return col

    return None


def get_numeric_columns(df):

    return df.select_dtypes(
        include="number"
    ).columns.tolist()


def get_default_value_column(df):

    numeric_cols = get_numeric_columns(df)

    if not numeric_cols:
        return None

    # Tránh chọn cột index / year
    filtered = []

    for col in numeric_cols:

        name = str(col).lower()

        if name not in [
            "index",
            "unnamed: 0",
            "year",
        ]:
            filtered.append(col)

    if filtered:
        return filtered[-1]

    return numeric_cols[-1]


def prepare_time_series(df, value_col):

    date_col = get_date_column(df)

    if date_col is None:

        return df[[value_col]].copy()

    chart_df = df[
        [date_col, value_col]
    ].copy()

    chart_df[date_col] = pd.to_datetime(
        chart_df[date_col],
        errors="coerce",
    )

    chart_df = chart_df.dropna(
        subset=[date_col]
    )

    chart_df = chart_df.sort_values(
        date_col
    )

    chart_df = chart_df.set_index(
        date_col
    )

    return chart_df


# ============================================================
# 6. SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "Tổng quan"


# ============================================================
# 7. NAVIGATION
# ============================================================

NAVIGATION = [

    (
        "Tổng quan",
        ":material/home:",
        "Tổng quan",
    ),

    (
        "Dữ liệu",
        ":material/database:",
        "Dữ liệu",
    ),

    (
        "Phân tích dữ liệu",
        ":material/analytics:",
        "Phân tích dữ liệu",
    ),

    (
        "Cấu hình mô hình",
        ":material/tune:",
        "Cấu hình mô hình",
    ),

    (
        "Huấn luyện & Đánh giá",
        ":material/model_training:",
        "Huấn luyện & Đánh giá",
    ),

    (
        "Ensemble & So sánh",
        ":material/account_tree:",
        "Ensemble & So sánh",
    ),

    (
        "Kết quả dự báo",
        ":material/trending_up:",
        "Kết quả dự báo",
    ),
]


with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">
            CPI
        </div>

        <div class="sidebar-line"></div>
        """,
        unsafe_allow_html=True,
    )

    for page_name, icon, tooltip in NAVIGATION:

        active = (
            st.session_state.page
            == page_name
        )

        if st.button(
            " ",
            key=f"nav_{page_name}",
            icon=icon,
            help=tooltip,
            type=(
                "primary"
                if active
                else "secondary"
            ),
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()


page = st.session_state.page


# ============================================================
# 8. TOP BAR
# ============================================================

st.html(
    """
<div class="topbar">

    <div class="brand-area">

        <div class="brand-mark">
            C
        </div>

        <div>

            <div class="brand-name">
                CPI TRANSPORT
            </div>

            <div class="brand-sub">
                FORECASTING DASHBOARD
            </div>

        </div>

    </div>

    <div class="topbar-right">

        <div class="top-chip">
            Tần suất · Tháng
        </div>

        <div class="top-chip top-chip-accent">
            Việt Nam · 2012–2024
        </div>

    </div>

</div>
"""
)


# ============================================================
# 9. PAGE HEADER FUNCTION
# ============================================================

def page_header(
    title,
    description,
):

    st.html(
        f"""
<div class="page-head">

    <div>

        <div class="breadcrumb">
            HOME &nbsp; / &nbsp; DASHBOARD
        </div>

        <div class="page-title">
            {title}
        </div>

        <div class="page-description">
            {description}
        </div>

    </div>

</div>
"""
    )


# ============================================================
# 10. KPI FUNCTION
# ============================================================

def overview_kpis():

    cpi_path = find_data_file(
        "CPI giao thông"
    )

    observation_count = "156"

    if cpi_path is not None:

        try:

            cpi_temp = load_csv(
                cpi_path
            )

            observation_count = str(
                len(cpi_temp)
            )

        except Exception:
            pass

    st.html(
        f"""
<div class="kpi-grid">

    <div class="kpi-card">

        <div class="kpi-top">

            <div class="kpi-label">
                Phạm vi dữ liệu
            </div>

            <div class="kpi-icon">
                <span class="material-symbols-rounded">
                    calendar_month
                </span>
            </div>

        </div>

        <div class="kpi-value">
            2012–2024
        </div>

        <div class="kpi-note">
            <span class="green-text">
                13 năm
            </span>
            dữ liệu lịch sử
        </div>

    </div>


    <div class="kpi-card">

        <div class="kpi-top">

            <div class="kpi-label">
                Số quan sát
            </div>

            <div class="kpi-icon">
                <span class="material-symbols-rounded">
                    table_rows
                </span>
            </div>

        </div>

        <div class="kpi-value">
            {observation_count}
        </div>

        <div class="kpi-note">
            Quan sát theo tháng
        </div>

    </div>


    <div class="kpi-card">

        <div class="kpi-top">

            <div class="kpi-label">
                Biến mục tiêu
            </div>

            <div class="kpi-icon">
                <span class="material-symbols-rounded">
                    monitoring
                </span>
            </div>

        </div>

        <div class="kpi-value">
            CPI
        </div>

        <div class="kpi-note">
            Nhóm
            <span class="orange-text">
                Giao thông
            </span>
        </div>

    </div>


    <div class="kpi-card">

        <div class="kpi-top">

            <div class="kpi-label">
                Nguồn dữ liệu
            </div>

            <div class="kpi-icon">
                <span class="material-symbols-rounded">
                    database
                </span>
            </div>

        </div>

        <div class="kpi-value">
            6
        </div>

        <div class="kpi-note">
            4 hoàn thiện · 2 đang cập nhật
        </div>

    </div>

</div>
"""
    )


# ============================================================
# 11. PAGE — TỔNG QUAN
# ============================================================

if page == "Tổng quan":

    page_header(
        "Tổng quan",
        "Theo dõi dữ liệu và tình trạng hệ thống dự báo CPI giao thông.",
    )

    overview_kpis()


    # --------------------------------------------------------
    # CPI CHART
    # --------------------------------------------------------

    st.html(
        """
<div class="section-header">

    <div class="section-title">
        CPI Giao thông 2012–2024
    </div>

    <div class="section-note">
        Chuỗi thời gian theo tháng
    </div>

</div>
"""
    )

    with st.container(
        border=True
    ):

        cpi_path = find_data_file(
            "CPI giao thông"
        )

        if cpi_path is None:

            st.info(
                "Chưa xác định được tên file CPI trong data/interim."
            )

        else:

            cpi_df = load_csv(
                cpi_path
            )

            cpi_value = (
                get_default_value_column(
                    cpi_df
                )
            )

            if cpi_value is None:

                st.warning(
                    "Chưa tìm thấy cột số trong file CPI."
                )

            else:

                cpi_chart = (
                    prepare_time_series(
                        cpi_df,
                        cpi_value,
                    )
                )

                st.line_chart(
                    cpi_chart,
                    height=330,
                    use_container_width=True,
                )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    st.html(
        """
<div class="section-header">

    <div class="section-title">
        Nguồn dữ liệu
    </div>

    <div class="section-note">
        Trạng thái xử lý hiện tại
    </div>

</div>
"""
    )

    st.html(
        """
<div class="status-grid">

    <div class="status-card">

        <div>
            <div class="status-name">
                CPI giao thông
            </div>

            <div class="status-sub">
                Biến mục tiêu
            </div>
        </div>

        <div class="status-done">
            Đã xử lý
        </div>

    </div>


    <div class="status-card">

        <div>
            <div class="status-name">
                WTI
            </div>

            <div class="status-sub">
                Giá dầu thế giới
            </div>
        </div>

        <div class="status-done">
            Đã xử lý
        </div>

    </div>


    <div class="status-card">

        <div>
            <div class="status-name">
                Brent
            </div>

            <div class="status-sub">
                Giá dầu thế giới
            </div>
        </div>

        <div class="status-done">
            Đã xử lý
        </div>

    </div>


    <div class="status-card">

        <div>
            <div class="status-name">
                USD/VND
            </div>

            <div class="status-sub">
                Tỷ giá
            </div>
        </div>

        <div class="status-done">
            Đã xử lý
        </div>

    </div>


    <div class="status-card">

        <div>
            <div class="status-name">
                RON95
            </div>

            <div class="status-sub">
                Giá xăng trong nước
            </div>
        </div>

        <div class="status-wait">
            Đang cập nhật
        </div>

    </div>


    <div class="status-card">

        <div>
            <div class="status-name">
                Diesel
            </div>

            <div class="status-sub">
                Giá dầu trong nước
            </div>
        </div>

        <div class="status-wait">
            Đang cập nhật
        </div>

    </div>

</div>
"""
    )


# ============================================================
# 12. PAGE — DỮ LIỆU
# ============================================================

elif page == "Dữ liệu":

    page_header(
        "Dữ liệu",
        "Kiểm tra cấu trúc và chất lượng từng nguồn dữ liệu.",
    )

    source = st.selectbox(
        "Nguồn dữ liệu",
        [
            "CPI giao thông",
            "WTI",
            "Brent",
            "USD/VND",
            "RON95",
            "Diesel",
        ],
    )


    if source in [
        "RON95",
        "Diesel",
    ]:

        st.warning(
            f"{source} đang trong quá trình thu thập và xử lý."
        )

    else:

        path = find_data_file(
            source
        )

        if path is None:

            st.error(
                f"Chưa tìm thấy file {source} trong data/interim."
            )

        else:

            df = load_csv(
                path
            )

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            c1.metric(
                "Số dòng",
                len(df),
            )

            c2.metric(
                "Số cột",
                df.shape[1],
            )

            c3.metric(
                "Missing",
                int(
                    df.isna()
                    .sum()
                    .sum()
                ),
            )

            c4.metric(
                "Duplicate",
                int(
                    df.duplicated()
                    .sum()
                ),
            )

            st.html(
                """
<div class="section-header">

    <div class="section-title">
        Bảng dữ liệu
    </div>

    <div class="section-note">
        Dữ liệu sau xử lý
    </div>

</div>
"""
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=470,
            )


# ============================================================
# 13. PAGE — PHÂN TÍCH
# ============================================================

elif page == "Phân tích dữ liệu":

    page_header(
        "Phân tích dữ liệu",
        "Khám phá xu hướng và đặc điểm của các chuỗi thời gian.",
    )

    source = st.selectbox(
        "Chọn chuỗi dữ liệu",
        [
            "CPI giao thông",
            "WTI",
            "Brent",
            "USD/VND",
        ],
    )

    path = find_data_file(
        source
    )

    if path is None:

        st.warning(
            f"Chưa tìm thấy file {source}."
        )

    else:

        df = load_csv(
            path
        )

        numeric_cols = (
            get_numeric_columns(df)
        )

        if len(numeric_cols) == 0:

            st.warning(
                "Không tìm thấy cột số để phân tích."
            )

        else:

            default_col = (
                get_default_value_column(df)
            )

            default_index = (
                numeric_cols.index(
                    default_col
                )
                if default_col in numeric_cols
                else 0
            )

            value_col = st.selectbox(
                "Biến hiển thị",
                numeric_cols,
                index=default_index,
            )


            st.html(
                """
<div class="section-header">

    <div class="section-title">
        Chuỗi thời gian
    </div>

    <div class="section-note">
        Diễn biến theo thời gian
    </div>

</div>
"""
            )

            with st.container(
                border=True
            ):

                chart_df = (
                    prepare_time_series(
                        df,
                        value_col,
                    )
                )

                st.line_chart(
                    chart_df,
                    height=350,
                    use_container_width=True,
                )


            st.html(
                """
<div class="section-header">

    <div class="section-title">
        Thống kê mô tả
    </div>

</div>
"""
            )

            describe_df = (
                df[numeric_cols]
                .describe()
                .T
            )

            st.dataframe(
                describe_df,
                use_container_width=True,
            )


    st.info(
        "Khi bộ dữ liệu tích hợp hoàn chỉnh, trang này sẽ bổ sung Correlation, VIF, ACF/PACF và phân tích các biến đặc trưng."
    )


# ============================================================
# 14. PAGE — CẤU HÌNH MÔ HÌNH
# ============================================================

elif page == "Cấu hình mô hình":

    page_header(
        "Cấu hình mô hình",
        "Lựa chọn mô hình, biến đầu vào và tham số huấn luyện.",
    )

    model = st.selectbox(
        "Chọn mô hình",
        [
            "Naive",
            "ElasticNet",
            "Random Forest",
            "ARIMAX",
        ],
    )


    available_features = [

        "CPI_Lag1",

        "WTI_Pct",

        "Brent_Pct",

        "USDVND_Pct",

        "Dummy_Tet",

        "Dummy_Covid",
    ]


    if model == "Naive":

        with st.container(
            border=True
        ):

            st.subheader(
                "Naive Model"
            )

            st.write(
                "Dự báo CPI tháng hiện tại bằng CPI của tháng liền trước."
            )

            st.code(
                "ŷ(t) = y(t-1)"
            )


    elif model == "ElasticNet":

        st.multiselect(
            "Biến đầu vào",
            available_features,
            default=available_features,
        )

        mode = st.radio(
            "Phương pháp chọn tham số",
            [
                "Tự động Grid Search",
                "Nhập thủ công",
            ],
            horizontal=True,
        )

        if mode == "Nhập thủ công":

            c1, c2 = st.columns(2)

            c1.number_input(
                "Alpha",
                min_value=0.0001,
                value=0.1,
            )

            c2.slider(
                "L1 Ratio",
                0.0,
                1.0,
                0.5,
            )


    elif model == "Random Forest":

        st.multiselect(
            "Biến đầu vào",
            available_features,
            default=available_features,
        )

        mode = st.radio(
            "Phương pháp chọn tham số",
            [
                "Tự động",
                "Nhập thủ công",
            ],
            horizontal=True,
        )

        if mode == "Nhập thủ công":

            c1, c2 = st.columns(2)

            c1.number_input(
                "n_estimators",
                min_value=10,
                value=100,
                step=10,
            )

            c2.number_input(
                "max_depth",
                min_value=1,
                value=5,
            )

            c3, c4 = st.columns(2)

            c3.number_input(
                "min_samples_split",
                min_value=2,
                value=2,
            )

            c4.number_input(
                "min_samples_leaf",
                min_value=1,
                value=1,
            )


    elif model == "ARIMAX":

        st.multiselect(
            "Biến ngoại sinh",
            [
                "WTI_Pct",
                "Brent_Pct",
                "USDVND_Pct",
                "Dummy_Tet",
                "Dummy_Covid",
            ],
            default=[
                "WTI_Pct",
                "Brent_Pct",
                "USDVND_Pct",
            ],
        )

        mode = st.radio(
            "Cấu hình tham số",
            [
                "Tự động",
                "Thủ công",
            ],
            horizontal=True,
        )

        if mode == "Thủ công":

            c1, c2, c3 = (
                st.columns(3)
            )

            c1.number_input(
                "p",
                min_value=0,
                value=1,
            )

            c2.number_input(
                "d",
                min_value=0,
                value=0,
            )

            c3.number_input(
                "q",
                min_value=0,
                value=1,
            )


    st.write("")

    if st.button(
        "Huấn luyện mô hình",
        icon=":material/play_arrow:",
        type="primary",
    ):

        st.info(
            "Phần huấn luyện thật sẽ được kết nối sau khi hoàn thiện bộ dữ liệu tích hợp."
        )


# ============================================================
# 15. PAGE — HUẤN LUYỆN
# ============================================================

elif page == "Huấn luyện & Đánh giá":

    page_header(
        "Huấn luyện & Đánh giá",
        "Theo dõi quy trình validation và hiệu quả của từng mô hình.",
    )


    c1, c2, c3, c4, c5 = (
        st.columns(5)
    )

    c1.metric(
        "RMSE",
        "—",
    )

    c2.metric(
        "MAE",
        "—",
    )

    c3.metric(
        "R²",
        "—",
    )

    c4.metric(
        "MAPE",
        "—",
    )

    c5.metric(
        "DA",
        "—",
    )


    st.html(
        """
<div class="section-header">

    <div class="section-title">
        Quy trình đánh giá
    </div>

</div>
"""
    )

    with st.container(
        border=True
    ):

        st.markdown(
            """
### Training / Development

**2012–2021**

→ Expanding-window Validation

→ Lựa chọn cấu hình tốt nhất

→ Đánh giá ngoài mẫu

### Test

**2022–2024**
"""
        )


# ============================================================
# 16. PAGE — ENSEMBLE
# ============================================================

elif page == "Ensemble & So sánh":

    page_header(
        "Ensemble & So sánh",
        "Kết hợp và đối chiếu hiệu quả giữa các mô hình dự báo.",
    )


    models = st.multiselect(
        "Chọn mô hình phối hợp",
        [
            "ElasticNet",
            "Random Forest",
            "ARIMAX",
        ],
    )


    method = st.radio(
        "Phương pháp trọng số",
        [
            "Trọng số bằng nhau",
            "Tự động theo RMSE Validation",
            "Người dùng tùy chỉnh",
        ],
    )


    if len(models) < 2:

        st.warning(
            "Chọn ít nhất 2 mô hình để tạo Ensemble."
        )

    else:

        st.success(
            "Đã đủ mô hình để tạo Ensemble."
        )


    st.html(
        """
<div class="section-header">

    <div class="section-title">
        So sánh mô hình
    </div>

</div>
"""
    )


    comparison_df = pd.DataFrame(
        {
            "Mô hình": [
                "Naive",
                "ElasticNet",
                "Random Forest",
                "ARIMAX",
                "Ensemble",
            ],

            "RMSE": [
                "—",
                "—",
                "—",
                "—",
                "—",
            ],

            "MAE": [
                "—",
                "—",
                "—",
                "—",
                "—",
            ],

            "R²": [
                "—",
                "—",
                "—",
                "—",
                "—",
            ],

            "MAPE": [
                "—",
                "—",
                "—",
                "—",
                "—",
            ],

            "DA": [
                "—",
                "—",
                "—",
                "—",
                "—",
            ],
        }
    )


    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# 17. PAGE — KẾT QUẢ
# ============================================================

elif page == "Kết quả dự báo":

    page_header(
        "Kết quả dự báo",
        "Hiển thị mô hình được lựa chọn và kết quả dự báo ngoài mẫu.",
    )


    selected_model = st.selectbox(
        "Mô hình",
        [
            "Chưa có kết quả",
            "Naive",
            "ElasticNet",
            "Random Forest",
            "ARIMAX",
            "Ensemble",
        ],
    )


    c1, c2, c3, c4, c5 = (
        st.columns(5)
    )

    c1.metric(
        "RMSE",
        "—",
    )

    c2.metric(
        "MAE",
        "—",
    )

    c3.metric(
        "R²",
        "—",
    )

    c4.metric(
        "MAPE",
        "—",
    )

    c5.metric(
        "DA",
        "—",
    )


    st.html(
        """
<div class="section-header">

    <div class="section-title">
        Actual vs Predicted
    </div>

    <div class="section-note">
        Test 2022–2024
    </div>

</div>
"""
    )


    with st.container(
        border=True
    ):

        st.write("")

        st.info(
            "Biểu đồ Actual vs Predicted sẽ được hiển thị tại đây sau khi huấn luyện mô hình."
        )

        st.write("")