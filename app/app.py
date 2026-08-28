# ============================================================
# CPI TRANSPORT FORECASTING DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
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
   SIDEBAR TOP SPACING
========================================================= */

.sidebar-spacer {
    height: 14px;
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
    min-height: 58px;
    border-radius: 10px;
    padding: 10px 18px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-bottom: 24px;
    border: 1px solid #e9eeee;
    box-shadow: 0 2px 8px rgba(39, 48, 66, .035);
}

.topbar-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    flex-wrap: wrap;
}

.top-chip {
    border-radius: 22px;
    background: #f2f8f8;
    padding: 8px 14px;
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
   OVERVIEW SUMMARY
========================================================= */

.overview-summary-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 22px;
}

.overview-summary-card {
    min-height: 122px;
    background: white;
    border-radius: 10px;
    padding: 20px 22px;
    box-sizing: border-box;
    border: 1px solid #e7eded;
    box-shadow: 0 2px 8px rgba(39,48,66,.035);
}

.overview-summary-label {
    color: #777d86;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .6px;
}

.overview-summary-value {
    color: #292934;
    font-size: 31px;
    line-height: 1;
    font-weight: 850;
    margin-top: 15px;
}

.overview-summary-note {
    color: #979ca4;
    font-size: 11px;
    margin-top: 10px;
}

.overview-summary-note strong {
    color: #5c616a;
    font-weight: 750;
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

    .overview-summary-grid {
        grid-template-columns: 1fr;
    }

    .topbar {
        justify-content: flex-start;
    }

    .topbar-right {
        justify-content: flex-start;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. PROJECT PATH
# ============================================================

APP_DIR = Path(__file__).resolve().parent

# Hỗ trợ cả khi file nằm trong /app hoặc ở thư mục gốc project
if (APP_DIR.parent / "data").exists():
    PROJECT_ROOT = APP_DIR.parent
else:
    PROJECT_ROOT = APP_DIR

DATA_DIR = PROJECT_ROOT / "data"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"


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

    "RON95": [
        "fuel_prices_monthly.csv",
    ],

    "Diesel": [
        "fuel_prices_monthly.csv",
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

            if source in ["RON95", "Diesel"] and "fuel" in name:
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
# 6. MODEL OUTPUTS
# ============================================================

@st.cache_data
def load_processed_outputs():
    outputs = {}

    paths = {
        "model_dataset": PROCESSED_DIR / "model_dataset.csv",
        "feature_dataset": PROCESSED_DIR / "feature_dataset.csv",
        "predictions": PROCESSED_DIR / "model_predictions.csv",
        "metrics": PROCESSED_DIR / "model_evaluation_metrics.csv",
    }

    for key, path in paths.items():
        if path.exists():
            df = pd.read_csv(path, encoding="utf-8-sig")

            if "MonthYear" in df.columns:
                df["MonthYear"] = pd.to_datetime(
                    df["MonthYear"].astype(str),
                    errors="coerce",
                )

            outputs[key] = df
        else:
            outputs[key] = None

    return outputs


OUTPUTS = load_processed_outputs()
MODEL_DATA = OUTPUTS["model_dataset"]
FEATURE_DATA = OUTPUTS["feature_dataset"]
PREDICTIONS = OUTPUTS["predictions"]
METRICS = OUTPUTS["metrics"]


VALIDATION_RMSE = {
    "Naive": 3.0927,
    "ElasticNet": 2.1856,
    "ARIMAX": 2.2829,
    "Ensemble": 2.1935,
}

_inv_elastic = 1 / VALIDATION_RMSE["ElasticNet"]
_inv_arimax = 1 / VALIDATION_RMSE["ARIMAX"]
ENSEMBLE_WEIGHT_ELASTIC = _inv_elastic / (_inv_elastic + _inv_arimax)
ENSEMBLE_WEIGHT_ARIMAX = _inv_arimax / (_inv_elastic + _inv_arimax)


# ============================================================
# 7. SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "Tổng quan"

if "overview_series" not in st.session_state:

    st.session_state.overview_series = "CPI giao thông"


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
        <div class="sidebar-spacer"></div>
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

    <div class="topbar-right">
        <div class="top-chip">Tần suất · Tháng</div>
        <div class="top-chip">Development · 2012–2021</div>
        <div class="top-chip top-chip-accent">Test · 2022–2024</div>
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
            HOME &nbsp; / &nbsp; {title.upper()}
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
# 10. OVERVIEW SUMMARY + DATA SWITCHER
# ============================================================

def overview_kpis():

    observation_count = 156

    if MODEL_DATA is not None:
        observation_count = len(MODEL_DATA)

    st.html(
        f"""
<div class="overview-summary-grid">

    <div class="overview-summary-card">
        <div class="overview-summary-label">Phạm vi dữ liệu</div>
        <div class="overview-summary-value">2012–2024</div>
        <div class="overview-summary-note">
            <strong>13 năm</strong> dữ liệu theo tháng phục vụ phân tích và dự báo
        </div>
    </div>

    <div class="overview-summary-card">
        <div class="overview-summary-label">Số quan sát</div>
        <div class="overview-summary-value">{observation_count}</div>
        <div class="overview-summary-note">
            <strong>120 tháng Development</strong> · 36 tháng Test
        </div>
    </div>

</div>
"""
    )


OVERVIEW_SERIES = {
    "CPI giao thông": {
        "column": "CPI",
        "button": "CPI",
        "title": "CPI Giao thông 2012–2024",
        "note": "Biến mục tiêu · % thay đổi theo tháng",
    },
    "RON95": {
        "column": "RON95",
        "button": "RON95",
        "title": "Giá xăng RON95 2012–2024",
        "note": "Giá xăng trong nước · dữ liệu theo tháng",
    },
    "Diesel": {
        "column": "Diesel",
        "button": "Diesel",
        "title": "Giá dầu Diesel 2012–2024",
        "note": "Giá dầu trong nước · dữ liệu theo tháng",
    },
    "Brent": {
        "column": "Brent",
        "button": "Brent",
        "title": "Giá dầu Brent 2012–2024",
        "note": "Giá dầu thế giới · dữ liệu theo tháng",
    },
    "WTI": {
        "column": "WTI",
        "button": "WTI",
        "title": "Giá dầu WTI 2012–2024",
        "note": "Giá dầu thế giới · dữ liệu theo tháng",
    },
    "USD/VND": {
        "column": "USD_VND",
        "button": "USD/VND",
        "title": "Tỷ giá USD/VND 2012–2024",
        "note": "Tỷ giá hối đoái · dữ liệu theo tháng",
    },
}


def overview_series_chart():

    st.html(
        """
<div class="section-header">
    <div class="section-title">Khám phá dữ liệu</div>
    <div class="section-note">Chọn biến để hiển thị chuỗi thời gian</div>
</div>
"""
    )

    series_names = list(OVERVIEW_SERIES.keys())
    button_cols = st.columns(len(series_names), gap="small")

    for i, series_name in enumerate(series_names):
        config = OVERVIEW_SERIES[series_name]
        active = st.session_state.overview_series == series_name

        with button_cols[i]:
            if st.button(
                config["button"],
                key=f"overview_series_{config['column']}",
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                st.session_state.overview_series = series_name
                st.rerun()

    selected_name = st.session_state.overview_series
    selected = OVERVIEW_SERIES[selected_name]
    value_col = selected["column"]

    st.html(
        f"""
<div class="section-header" style="margin-top: 18px;">
    <div class="section-title">{selected['title']}</div>
    <div class="section-note">{selected['note']}</div>
</div>
"""
    )

    with st.container(border=True):

        if MODEL_DATA is None:
            st.info("Chưa tìm thấy data/processed/model_dataset.csv")
            return

        if value_col not in MODEL_DATA.columns:
            st.warning(
                f"Không tìm thấy cột '{value_col}' trong model_dataset.csv. "
                "Kiểm tra lại tên cột trong dữ liệu đã xử lý."
            )
            return

        chart_df = (
            MODEL_DATA[["MonthYear", value_col]]
            .dropna()
            .copy()
            .set_index("MonthYear")
        )

        chart_df = chart_df.rename(columns={value_col: selected_name})

        st.line_chart(
            chart_df,
            height=360,
            use_container_width=True,
        )


# ============================================================
# 11. PAGE — TỔNG QUAN
# ============================================================

if page == "Tổng quan":

    page_header(
        "Tổng quan",
        "Theo dõi phạm vi dữ liệu và trực quan hóa các biến chính của bài toán dự báo CPI giao thông.",
    )

    overview_kpis()
    overview_series_chart()


# ============================================================
# 12. PAGE — DỮ LIỆU
# ============================================================

elif page == "Dữ liệu":

    page_header(
        "Dữ liệu",
        "Kiểm tra cấu trúc, chất lượng và phạm vi thời gian của từng nguồn dữ liệu sau xử lý.",
    )

    source = st.selectbox(
        "Nguồn dữ liệu",
        [
            "CPI giao thông",
            "RON95",
            "Diesel",
            "WTI",
            "Brent",
            "USD/VND",
        ],
    )

    path = find_data_file(source)

    if path is None:
        st.error(f"Chưa tìm thấy file {source} trong data/interim.")
    else:
        df = load_csv(path)

        if source == "RON95" and "RON95" in df.columns:
            keep = [c for c in ["MonthYear", "RON95"] if c in df.columns]
            df = df[keep].copy()
        elif source == "Diesel" and "Diesel" in df.columns:
            keep = [c for c in ["MonthYear", "Diesel"] if c in df.columns]
            df = df[keep].copy()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Số dòng", len(df))
        c2.metric("Số cột", df.shape[1])
        c3.metric("Missing", int(df.isna().sum().sum()))
        c4.metric("Duplicate", int(df.duplicated().sum()))

        numeric_cols = get_numeric_columns(df)
        value_col = get_default_value_column(df)

        if value_col is not None:
            st.html(
                """
<div class="section-header">
    <div class="section-title">Diễn biến dữ liệu</div>
    <div class="section-note">Chuỗi sau xử lý</div>
</div>
"""
            )

            with st.container(border=True):
                chart_df = prepare_time_series(df, value_col)
                st.line_chart(chart_df, height=300, use_container_width=True)

        st.html(
            """
<div class="section-header">
    <div class="section-title">Bảng dữ liệu</div>
    <div class="section-note">Dữ liệu sau xử lý</div>
</div>
"""
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=430,
        )


# ============================================================
# 13. PAGE — PHÂN TÍCH
# ============================================================

elif page == "Phân tích dữ liệu":

    page_header(
        "Phân tích dữ liệu",
        "Khám phá xu hướng, thống kê mô tả và mối quan hệ giữa CPI với các yếu tố giải thích.",
    )

    if MODEL_DATA is None:
        st.error("Chưa tìm thấy data/processed/model_dataset.csv")
    else:
        analysis_df = MODEL_DATA.copy()

        tab1, tab2, tab3 = st.tabs([
            "Chuỗi thời gian",
            "Tết & Covid",
            "Tương quan",
        ])

        with tab1:
            source = st.selectbox(
                "Chọn biến",
                ["CPI", "RON95", "Diesel", "Brent", "WTI", "USD_VND"],
                key="analysis_source",
            )

            series = analysis_df[source].dropna()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Trung bình", f"{series.mean():.2f}")
            c2.metric("Độ lệch chuẩn", f"{series.std():.2f}")
            c3.metric("Nhỏ nhất", f"{series.min():.2f}")
            c4.metric("Lớn nhất", f"{series.max():.2f}")

            with st.container(border=True):
                plot_df = analysis_df[["MonthYear", source]].dropna().set_index("MonthYear")
                st.line_chart(plot_df, height=340, use_container_width=True)

        with tab2:
            left, right = st.columns(2)

            with left:
                st.subheader("Tết Nguyên đán")
                tet_summary = (
                    analysis_df.groupby("Dummy_Tet")["CPI"]
                    .agg(["count", "mean", "std", "min", "max"])
                    .round(2)
                )
                tet_summary.index = ["Không Tết", "Tết"]
                st.dataframe(tet_summary, use_container_width=True)

            with right:
                st.subheader("Covid-19")
                covid_summary = (
                    analysis_df.groupby("Dummy_Covid")["CPI"]
                    .agg(["count", "mean", "std", "min", "max"])
                    .round(2)
                )
                covid_summary.index = ["Ngoài Covid", "Covid"]
                st.dataframe(covid_summary, use_container_width=True)

            st.info(
                "Tết có CPI trung bình cao hơn nhóm không Tết; giai đoạn Covid thể hiện mức độ biến động lớn hơn. "
                "Đây là kết quả mô tả và không khẳng định quan hệ nhân quả."
            )

        with tab3:
            corr_df = analysis_df.copy()

            for col in ["RON95", "Diesel", "Brent", "WTI", "USD_VND"]:
                corr_df[f"{col}_change"] = corr_df[col].pct_change(fill_method=None) * 100

            corr_cols = [
                "CPI",
                "RON95_change",
                "Diesel_change",
                "Brent_change",
                "WTI_change",
                "USD_VND_change",
            ]

            corr = corr_df[corr_cols].corr().round(2)
            st.dataframe(
                corr.style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1).format("{:.2f}"),
                use_container_width=True,
            )

            st.caption(
                "Các biến giá được chuyển sang % thay đổi theo tháng để phù hợp với CPI dạng % MoM."
            )


# ============================================================
# 14. PAGE — CẤU HÌNH MÔ HÌNH
# ============================================================

elif page == "Cấu hình mô hình":

    page_header(
        "Cấu hình mô hình",
        "Theo dõi các cấu hình đã được lựa chọn trong Development 2012–2021 bằng Expanding-window Validation.",
    )

    model = st.selectbox(
        "Chọn mô hình",
        ["Naive", "ElasticNet", "ARIMAX", "Ensemble"],
    )

    if model == "Naive":
        with st.container(border=True):
            st.subheader("Naive Model")
            st.write("Dự báo CPI tháng hiện tại bằng CPI của tháng liền trước.")
            st.code("ŷ(t) = y(t-1)")
            st.metric("Validation RMSE", f"{VALIDATION_RMSE['Naive']:.4f}")

    elif model == "ElasticNet":
        c1, c2, c3 = st.columns(3)
        c1.metric("Alpha", "0.1")
        c2.metric("L1 Ratio", "0.9")
        c3.metric("Validation RMSE", f"{VALIDATION_RMSE['ElasticNet']:.4f}")

        st.info(
            "ElasticNet sử dụng 15 feature đã xây dựng: CPI lag, biến động giá lag 1, MA3, Dummy Tết/Covid, "
            "Month sin/cos và Brent-WTI Spread lag 1. StandardScaler chỉ fit trên Train của từng fold."
        )

        if FEATURE_DATA is not None:
            feature_cols = [c for c in FEATURE_DATA.columns if c not in ["MonthYear", "CPI"]]
            st.multiselect(
                "Feature đang sử dụng",
                feature_cols,
                default=feature_cols,
                disabled=True,
            )

    elif model == "ARIMAX":
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("p", "1")
        c2.metric("d", "0")
        c3.metric("q", "2")
        c4.metric("Validation RMSE", f"{VALIDATION_RMSE['ARIMAX']:.4f}")

        st.multiselect(
            "Biến ngoại sinh đã chọn",
            [
                "RON95_change_lag1",
                "Diesel_change_lag1",
                "Brent_change_lag1",
                "USD_VND_change_lag1",
            ],
            default=[
                "RON95_change_lag1",
                "Diesel_change_lag1",
                "Brent_change_lag1",
                "USD_VND_change_lag1",
            ],
            disabled=True,
        )

        st.caption(
            "Bộ exogenous được chọn bằng AIC/BIC; cấu hình (1,0,2) được chốt theo RMSE Expanding-window Validation."
        )

    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("ElasticNet weight", f"{ENSEMBLE_WEIGHT_ELASTIC:.3f}")
        c2.metric("ARIMAX weight", f"{ENSEMBLE_WEIGHT_ARIMAX:.3f}")
        c3.metric("Validation RMSE", f"{VALIDATION_RMSE['Ensemble']:.4f}")

        st.info(
            "Trọng số Ensemble được tính theo nghịch đảo RMSE Validation và được cố định trước khi đánh giá Test."
        )


# ============================================================
# 15. PAGE — HUẤN LUYỆN
# ============================================================

elif page == "Huấn luyện & Đánh giá":

    page_header(
        "Huấn luyện & Đánh giá",
        "Development 2012–2021 dùng Expanding-window Validation; Test 2022–2024 chỉ dùng cho đánh giá cuối cùng.",
    )

    st.html(
        """
<div class="section-header">
    <div class="section-title">Quy trình đánh giá</div>
    <div class="section-note">Không random split</div>
</div>
"""
    )

    with st.container(border=True):
        st.markdown(
            """
**Development: 01/2012 – 12/2021**  
→ 120 tháng  
→ Expanding-window Validation từ 01/2018 đến 12/2021  
→ **48 folds**  
→ chọn hyperparameter ElasticNet, cấu hình ARIMAX và trọng số Ensemble  

**Test: 01/2022 – 12/2024**  
→ 36 tháng  
→ không dùng để tune mô hình
"""
        )

    st.html(
        """
<div class="section-header">
    <div class="section-title">Validation RMSE</div>
    <div class="section-note">Development 2012–2021</div>
</div>
"""
    )

    val_df = pd.DataFrame({
        "Model": list(VALIDATION_RMSE.keys()),
        "RMSE": list(VALIDATION_RMSE.values()),
    }).sort_values("RMSE")

    st.dataframe(
        val_df.style.format({"RMSE": "{:.4f}"}),
        use_container_width=True,
        hide_index=True,
    )

    st.html(
        """
<div class="section-header">
    <div class="section-title">Đánh giá Test</div>
    <div class="section-note">2022–2024</div>
</div>
"""
    )

    if METRICS is None:
        st.info("Chưa tìm thấy model_evaluation_metrics.csv")
    else:
        st.dataframe(
            METRICS.sort_values("RMSE").style.format({
                "R2": "{:.4f}",
                "MAE": "{:.4f}",
                "RMSE": "{:.4f}",
                "MAPE (%)": "{:.2f}%",
                "DA (%)": "{:.2f}%",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.warning(
            "MAPE rất cao vì CPI có nhiều giá trị gần 0 hoặc âm; nên ưu tiên RMSE/MAE và dùng DA như chỉ số bổ sung."
        )


# ============================================================
# 16. PAGE — ENSEMBLE
# ============================================================

elif page == "Ensemble & So sánh":

    page_header(
        "Ensemble & So sánh",
        "Kết hợp ElasticNet và ARIMAX theo trọng số nghịch đảo RMSE Validation, sau đó so sánh hiệu quả trên Test.",
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("ElasticNet weight", f"{ENSEMBLE_WEIGHT_ELASTIC:.3f}")
    c2.metric("ARIMAX weight", f"{ENSEMBLE_WEIGHT_ARIMAX:.3f}")
    c3.metric("Validation RMSE", f"{VALIDATION_RMSE['Ensemble']:.4f}")

    st.caption(
        "Ensemble = w₁ × ElasticNet + w₂ × ARIMAX. Trọng số được tính từ Development và không tính lại bằng Test."
    )

    st.html(
        """
<div class="section-header">
    <div class="section-title">So sánh mô hình</div>
    <div class="section-note">Test 2022–2024</div>
</div>
"""
    )

    if METRICS is None:
        st.info("Chưa tìm thấy model_evaluation_metrics.csv")
    else:
        st.dataframe(
            METRICS.sort_values("RMSE").style.format({
                "R2": "{:.4f}",
                "MAE": "{:.4f}",
                "RMSE": "{:.4f}",
                "MAPE (%)": "{:.2f}%",
                "DA (%)": "{:.2f}%",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "Ensemble có RMSE thấp nhất trên Test, nhưng chỉ nhỉnh hơn ElasticNet rất nhỏ; vì vậy không nên diễn giải là vượt trội toàn diện."
        )


# ============================================================
# 17. PAGE — KẾT QUẢ
# ============================================================

elif page == "Kết quả dự báo":

    page_header(
        "Kết quả dự báo",
        "Hiển thị CPI thực tế và dự báo ngoài mẫu của từng mô hình trên Test 2022–2024.",
    )

    if PREDICTIONS is None or METRICS is None:
        st.error("Thiếu model_predictions.csv hoặc model_evaluation_metrics.csv trong data/processed.")
    else:
        model_map = {
            "Naive": "Naive_Pred",
            "ElasticNet": "ElasticNet_Pred",
            "ARIMAX": "ARIMAX_Pred",
            "Ensemble": "Ensemble_Pred",
        }

        best_model = METRICS.sort_values("RMSE").iloc[0]["Model"]

        selected_model = st.selectbox(
            "Mô hình",
            list(model_map.keys()),
            index=list(model_map.keys()).index(best_model) if best_model in model_map else 0,
        )

        row = METRICS.loc[METRICS["Model"] == selected_model].iloc[0]

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("RMSE", f"{row['RMSE']:.4f}")
        c2.metric("MAE", f"{row['MAE']:.4f}")
        c3.metric("R²", f"{row['R2']:.4f}")
        c4.metric("MAPE", f"{row['MAPE (%)']:.2f}%")
        c5.metric("DA", f"{row['DA (%)']:.2f}%")

        pred_col = model_map[selected_model]

        st.html(
            f"""
<div class="section-header">
    <div class="section-title">Actual vs Predicted</div>
    <div class="section-note">{selected_model} · Test 2022–2024</div>
</div>
"""
        )

        chart_df = PREDICTIONS[["MonthYear", "Actual", pred_col]].copy()
        chart_df = chart_df.rename(columns={"Actual": "Thực tế", pred_col: selected_model})
        chart_df = chart_df.set_index("MonthYear")

        with st.container(border=True):
            st.line_chart(chart_df, height=370, use_container_width=True)

        detail_df = PREDICTIONS[["MonthYear", "Actual", pred_col]].copy()
        detail_df["Error"] = detail_df["Actual"] - detail_df[pred_col]
        detail_df["Abs_Error"] = detail_df["Error"].abs()
        detail_df = detail_df.rename(columns={
            "Actual": "Thực tế",
            pred_col: "Dự báo",
            "Error": "Sai số",
            "Abs_Error": "|Sai số|",
        })

        st.html(
            """
<div class="section-header">
    <div class="section-title">Chi tiết theo tháng</div>
    <div class="section-note">36 tháng Test</div>
</div>
"""
        )

        st.dataframe(
            detail_df.style.format({
                "Thực tế": "{:.2f}",
                "Dự báo": "{:.2f}",
                "Sai số": "{:.2f}",
                "|Sai số|": "{:.2f}",
            }),
            use_container_width=True,
            hide_index=True,
            height=430,
        )

        if float(row["R2"]) < 0:
            st.warning(
                "R² trên Test đang âm, cho thấy mô hình chưa giải thích tốt các cú sốc ngoài mẫu, đặc biệt giai đoạn biến động năng lượng mạnh năm 2022."
            )

