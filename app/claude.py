# ============================================================
# CPI TRANSPORT FORECASTING DASHBOARD
# Updated từ phiên bản dashboard cũ của project
#
# Chạy từ thư mục gốc project:
#   streamlit run app/app.py
#
# Chỉ cần:
#   pip install streamlit pandas numpy openpyxl
#
# Tùy chọn cho Forecast thật:
#   pip install joblib scikit-learn
# ============================================================

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


try:
    import joblib
except Exception:
    joblib = None


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
# 2. CSS — GIỮ STYLE CŨ, BỔ SUNG MỘT SỐ COMPONENT
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
========================================================= */

html, .stApp, body, [class*="css"] {
    font-family: Sans serif;
}

[role="tablist"] [role="tab"],
[role="tablist"] [role="tab"] * {
    font-family: inherit !important;
}

div[data-testid="stButton"] button p {
    font-family: inherit !important;
}

span[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined {
    font-family: "Material Symbols Rounded" !important;
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

[data-testid="stToolbar"],
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
    overflow: hidden !important;
}

section[data-testid="stSidebar"]
[data-testid="stVerticalBlock"] {
    position: fixed !important;

    top: 0 !important;
    left: 0 !important;

    width: 84px !important;
    height: 100vh !important;

    padding: 20px 8px !important;
    box-sizing: border-box !important;

    display: flex !important;
    flex-direction: column !important;
    justify-content: space-evenly !important;
    align-items: center !important;

    gap: 0 !important;
}

/* Mỗi nút chiếm một phần bằng nhau */
section[data-testid="stSidebar"]
[data-testid="stSidebarUserContent"]
div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) {
    flex: 1 1 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Ẩn nút collapse */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
/* =========================================================
   BUTTON MENU
========================================================= */

section[data-testid="stSidebar"]
div[data-testid="stButton"] {
    width: 100% !important;

    display: flex !important;
    justify-content: center !important;
    align-items: center !important;

    margin: 0 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stButton"] button {
    width: 58px !important;
    height: 58px !important;

    min-width: 58px !important;
    min-height: 58px !important;

    padding: 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    border: none !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}

/* Menu chưa chọn */
section[data-testid="stSidebar"]
button[kind="secondary"] {
    background: transparent !important;
    color: #9b9cab !important;
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
}

/* =========================================================
   ICON
========================================================= */

section[data-testid="stSidebar"]
span[data-testid="stIconMaterial"] {
    font-size: 30px !important;
    width: 30px !important;
    height: 30px !important;
    line-height: 30px !important;
}

section[data-testid="stSidebar"]
.material-symbols-rounded,
section[data-testid="stSidebar"]
.material-symbols-outlined {
    font-size: 30px !important;
    width: 30px !important;
    height: 30px !important;
    line-height: 30px !important;
}

section[data-testid="stSidebar"]
button svg {
    width: 30px !important;
    height: 30px !important;
}

section[data-testid="stSidebar"] {
    overflow: visible !important;
}

section[data-testid="stSidebar"]
div[data-testid="stButton"],
section[data-testid="stSidebar"]
div[data-testid="stButton"] button {
    overflow: visible !important;
}

section[data-testid="stSidebar"]
div[data-testid="stButton"] button {
    position: relative !important;
}

/* Chữ tooltip */
section[data-testid="stSidebar"]
div[data-testid="stButton"] button p {
    position: absolute !important;

    left: 70px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;

    width: max-content !important;

    margin: 0 !important;
    padding: 8px 12px !important;

    background: white !important;
    color: #555 !important;

    border-radius: 7px !important;

    font-size: 16px !important;
    font-weight: 400 !important;

    opacity: 0 !important;
    visibility: hidden !important;

    pointer-events: none !important;
    z-index: 99999 !important;
}

/* Chỉ hiện đúng icon đang rê chuột */
section[data-testid="stSidebar"]
div[data-testid="stButton"] button:hover p {
    opacity: 1 !important;
    visibility: visible !important;
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


.page-title {
    font-size: 34px;
    line-height: 1;
    font-weight: 850;
    color: #292934;
    letter-spacing: -.5px;
}

.page-description {
    color: #8c9199;
    font-size: 20px;
    margin-top: 8px;
}

/* =========================================================
   SUMMARY CARDS
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
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .6px;
}

.overview-summary-value {
    color: #292934;
    font-size: 40px;
    line-height: 1;
    font-weight: 850;
    margin-top: 15px;
}

.overview-summary-note {
    color: #979ca4;
    font-size: 15px;
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
    font-size: 18px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .4px;
}

.section-note {
    color: #989da4;
    font-size: 15px;
}

/* =========================================================
   INFO CARDS
========================================================= */

.info-card {
    background: white;
    border: 1px solid #e5ebeb;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(39,48,66,.035);
    margin-bottom: 12px;
}

.info-card-title {
    color: #292934;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
}

.info-card-text {
    color: #7f858d;
    font-size: 12px;
    line-height: 1.65;
}


/* =========================================================
   WHITE CONTAINERS
========================================================= */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border: 1px solid #e5ebeb !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(39,48,66,.035) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] > div {
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
   TABS - áp dụng cho toàn bộ st.tabs()
========================================================= */

[role="tablist"] {
    gap: 12px !important;
}

[role="tablist"] [role="tab"],
[role="tablist"] [role="tab"] * {
    font-size: 18px !important;
    font-weight: 500 !important;
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
    box-shadow: 0 2px 8px rgba(39,48,66,.035);
}

[data-testid="stMetricLabel"] {
    color: #777d86 !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    color: #292934 !important;
    font-size: 45px !important;
    font-weight: 800 !important;
}

/* =========================================================
   BUTTON
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

[data-testid="stDownloadButton"] button {
    border-radius: 8px !important;
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
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. PROJECT PATH
# app/app.py  ->  PROJECT_ROOT là thư mục cha của app
# ============================================================

APP_DIR = Path(__file__).resolve().parent

if (APP_DIR.parent / "data").exists():
    PROJECT_ROOT = APP_DIR.parent
else:
    PROJECT_ROOT = APP_DIR

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
MODELS_DIR = PROJECT_ROOT / "models"

if str(PROJECT_ROOT) not in sys.path:

    sys.path.append(str(PROJECT_ROOT))

from src.modeling import (
    run_naive_validation,
    run_elasticnet_validation,
    ELASTICNET_FEATURES,
    run_arimax_validation,
    ARIMAX_EXOG_FEATURES,
    run_ensemble_validation,

    run_naive_test,
    run_elasticnet_test,
    run_arimax_test,
    run_ensemble_test,
    evaluate_test_result,
)

# ============================================================
# 4. FILE MAP
# ============================================================

RAW_FILES = {
    "Brent crude oil": [
        "brent_crude_oil_monthly.csv",
    ],
    "USD/VND exchange rate": [
        "usd_vnd_exchange_rate.xlsx",
    ],
    "Fuel prices 2012–2018": [
        "vietnam_fuel_prices_2012_2018.xlsx",
    ],
    "Fuel prices 2012": [
        "vietnam_fuel_prices_2012.csv",
    ],
    "Fuel prices 2017–2018": [
        "vietnam_fuel_prices_2017_2018.xlsx",
    ],
    "Fuel prices 2018–2026": [
        "vietnam_fuel_prices_2018_2026.csv",
    ],
    "CPI giao thông": [
        "vietnam_transport_cpi_mom_2012_2024.xlsx",
    ],
    "WTI crude oil": [
        "wti_crude_oil_monthly.csv",
    ],
}

INTERIM_FILES = {
    "Brent monthly": "brent_monthly.csv",
    "CPI transport monthly": "cpi_transport_monthly.csv",
    "Fuel prices clean": "fuel_prices_clean.csv",
    "Fuel prices monthly": "fuel_prices_monthly.csv",
    "USD/VND monthly": "usd_vnd_monthly.csv",
    "WTI monthly": "wti_monthly.csv",
}

PROCESSED_FILES = {
    "Feature dataset": "feature_dataset.csv",
    "Model dataset": "model_dataset.csv",
    "Model evaluation metrics": "model_evaluation_metrics.csv",
    "Model predictions": "model_predictions.csv",
}

NOTEBOOKS = [
    ("01", "CPI processing", "01_cpi_processing.ipynb"),
    ("02", "Fuel processing", "02_fuel_processing.ipynb"),
    ("03", "Fuel monthly aggregation", "03_fuel_processing_monthly.ipynb"),
    ("04", "Global oil processing", "04_global_oil_processing.ipynb"),
    ("05", "Exchange rate processing", "05_exchange_rate_processing.ipynb"),
    ("06", "Dataset integration", "06_dataset_integration.ipynb"),
    ("07", "Exploratory analysis", "07_exploratory_analysis.ipynb"),
    ("08", "Feature engineering", "08_feature_engineering.ipynb"),
    ("09", "Modeling", "09_modeling.ipynb"),
    ("10", "Model evaluation", "10_model_evaluation.ipynb"),
]


# ============================================================
# 5. GENERIC HELPERS
# ============================================================

def normalize_text(value):
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text


@st.cache_data(show_spinner=False)
def load_table(path_string):
    path = Path(path_string)

    if not path.exists():
        return None

    try:
        if path.suffix.lower() == ".csv":
            try:
                return pd.read_csv(path, encoding="utf-8-sig")
            except UnicodeDecodeError:
                return pd.read_csv(path)

        if path.suffix.lower() in [".xlsx", ".xls"]:
            return pd.read_excel(path)

    except Exception:
        return None

    return None


def safe_load(path):
    df = load_table(str(path))
    return None if df is None else df.copy()


def get_date_column(df):
    if df is None or df.empty:
        return None

    preferred = [
        "MonthYear",
        "month_year",
        "Date",
        "date",
        "Month",
        "month",
        "Time",
        "time",
        "Period",
        "period",
    ]

    for col in preferred:
        if col in df.columns:
            return col

    for col in df.columns:
        lower = normalize_text(col)
        if any(key in lower for key in ["date", "month", "time", "period"]):
            return col

    return None


def prepare_date(df):
    if df is None or df.empty:
        return df, None

    work = df.copy()
    date_col = get_date_column(work)

    if date_col is not None:
        parsed = pd.to_datetime(work[date_col], errors="coerce")
        if parsed.notna().sum() >= 2:
            work[date_col] = parsed
            work = work.sort_values(date_col)
            return work, date_col

    return work, None


def get_numeric_columns(df):
    if df is None or df.empty:
        return []

    work = df.copy()
    cols = []

    for col in work.columns:
        if pd.api.types.is_numeric_dtype(work[col]):
            cols.append(col)
            continue

        converted = pd.to_numeric(
            work[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )

        if converted.notna().mean() >= 0.8:
            cols.append(col)

    return cols



def get_default_value_column(df):
    numeric_cols = get_numeric_columns(df)

    filtered = [
        c for c in numeric_cols
        if normalize_text(c) not in ["index", "unnamed_0", "year"]
    ]

    if filtered:
        return filtered[-1]

    return numeric_cols[-1] if numeric_cols else None


def prepare_time_series(df, value_col):
    work, date_col = prepare_date(df)

    if value_col not in work.columns:
        return pd.DataFrame()

    values = pd.to_numeric(work[value_col], errors="coerce")

    if date_col is None:
        out = pd.DataFrame({value_col: values}).dropna()
        return out

    out = pd.DataFrame({
        date_col: work[date_col],
        value_col: values,
    }).dropna()

    return out.set_index(date_col)



def download_file_button(path, label, key):
    if not path.exists():
        st.caption("File chưa tồn tại.")
        return

    st.download_button(
        label=label,
        data=path.read_bytes(),
        file_name=path.name,
        mime="application/octet-stream",
        key=key,
        use_container_width=True,
    )


def dataframe_download_button(df, filename, key):
    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label=f"Tải {filename}",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
        key=key,
        use_container_width=True,
    )


def section_header(title, note=""):
    st.html(
        f"""
<div class="section-header">
    <div class="section-title">{title}</div>
    <div class="section-note">{note}</div>
</div>
"""
    )

def button_selector(label, options, state_key, columns=4):
    if state_key not in st.session_state:
        st.session_state[state_key] = options[0]

    if label:
        st.markdown(f"**{label}**")

    for start in range(0, len(options), columns):
        row_options = options[start:start + columns]
        cols = st.columns(columns, gap="small")

        for i, option in enumerate(row_options):
            active = st.session_state[state_key] == option

            with cols[i]:
                if st.button(
                    str(option),
                    key=f"{state_key}_{start+i}",
                    type="primary" if active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state[state_key] = option
                    st.rerun()

    return st.session_state[state_key]

# ============================================================
# 6. LOAD PROCESSED OUTPUTS
# ============================================================

@st.cache_data(show_spinner=False)
def load_processed_outputs():
    outputs = {}

    for key, filename in PROCESSED_FILES.items():
        path = PROCESSED_DIR / filename
        df = load_table(str(path))

        if df is not None:
            date_col = get_date_column(df)
            if date_col is not None:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        outputs[key] = df

    return outputs


OUTPUTS = load_processed_outputs()

FEATURE_DATA = OUTPUTS["Feature dataset"]
MODEL_DATA = OUTPUTS["Model dataset"]
METRICS = OUTPUTS["Model evaluation metrics"]
PREDICTIONS = OUTPUTS["Model predictions"]


# Các RMSE Validation đã có trong notebook/modeling cũ
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

if "raw_source" not in st.session_state:
    st.session_state.raw_source = list(RAW_FILES.keys())[0]

# ============================================================
# 8. NAVIGATION — CẤU TRÚC 7 TRANG MỚI
# ============================================================

NAVIGATION = [
    ("Tổng quan", ":material/home:", "Trang chủ / Tổng quan"),
    ("Dữ liệu & Tiền xử lý", ":material/database:", "Dữ liệu thô & Tiền xử lý"),
    ("Phân tích khám phá", ":material/analytics:", "Phân tích khám phá dữ liệu"),
    ("Feature Engineering", ":material/manufacturing:", "Feature Engineering"),
    ("Mô hình & Kết quả", ":material/model_training:", "Mô hình & Kết quả"),
    ("Về dự án", ":material/info:", "Tài liệu / Về dự án"),
]


def change_page(page_name):
    st.session_state.page = page_name


with st.sidebar:
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    for page_name, icon, tooltip in NAVIGATION:
        active = st.session_state.page == page_name

        st.button(
            tooltip,
            key=f"nav_{page_name}",
            icon=icon,
            type="primary" if active else "secondary",
            use_container_width=True,
            on_click=change_page,
            args=(page_name,),
        )

page = st.session_state.page



# ============================================================
# 10. PAGE HEADER
# ============================================================


def page_header(title, description):
    st.html(
        f"""
<div class="page-head">
    <div>

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
# 11. HOME HELPERS
# ============================================================

OVERVIEW_SERIES = {
    "CPI giao thông": {
        "column": "CPI",
        "button": "CPI",
        "title": "CPI Giao thông 2012-2024",
        "note": "Biến mục tiêu · % thay đổi theo tháng",
    },
    "RON95": {
        "column": "RON95",
        "button": "RON95",
        "title": "Giá xăng RON95 2012-2024",
        "note": "Giá xăng trong nước · dữ liệu theo tháng",
    },
    "Diesel": {
        "column": "Diesel",
        "button": "Diesel",
        "title": "Giá dầu Diesel 2012-2024",
        "note": "Giá dầu trong nước · dữ liệu theo tháng",
    },
    "Brent": {
        "column": "Brent",
        "button": "Brent",
        "title": "Giá dầu Brent 2012-2024",
        "note": "Giá dầu thế giới · dữ liệu theo tháng",
    },
    "WTI": {
        "column": "WTI",
        "button": "WTI",
        "title": "Giá dầu WTI 2012-2024",
        "note": "Giá dầu thế giới · dữ liệu theo tháng",
    },
    "USD/VND": {
        "column": "USD_VND",
        "button": "USD/VND",
        "title": "Tỷ giá USD/VND 2012-2024",
        "note": "Tỷ giá hối đoái · dữ liệu theo tháng",
    },
}


def overview_kpis():
    observation_count = 156
    start = "01/2012"
    end = "12/2024"

    if MODEL_DATA is not None and not MODEL_DATA.empty:
        date_col = get_date_column(MODEL_DATA)

        if date_col:
            data = MODEL_DATA.copy()
            data[date_col] = pd.to_datetime(data[date_col], errors="coerce")

            # Chỉ lấy 2012–2024
            data = data[
                (data[date_col] >= "2012-01-01") &
                (data[date_col] <= "2024-12-31")
            ]

            observation_count = len(data)

            dates = data[date_col].dropna()

            if not dates.empty:
                start = dates.min().strftime("%m/%Y")
                end = dates.max().strftime("%m/%Y")

    st.html(
        f"""
<div class="overview-summary-grid">

    <div class="overview-summary-card">
        <div class="overview-summary-label">Phạm vi dữ liệu</div>
        <div class="overview-summary-value">2012–2024</div>
        <div class="overview-summary-note">
            <strong>{start} → {end}</strong> · dữ liệu theo tháng
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

def overview_series_chart():
    section_header(
        "Khám phá dữ liệu",
        "Chọn biến để hiển thị chuỗi thời gian"
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

    section_header(
        selected["title"],
        selected["note"]
    )

    with st.container(border=True):

        if MODEL_DATA is None or MODEL_DATA.empty:
            st.info("Chưa tìm thấy data/processed/model_dataset.csv")
            return

        if value_col not in MODEL_DATA.columns:
            st.warning(
                f"Không tìm thấy cột '{value_col}' trong model_dataset.csv."
            )
            return

        date_col = get_date_column(MODEL_DATA)

        if date_col is None:
            st.warning("Không tìm thấy cột thời gian.")
            return

        chart_df = MODEL_DATA[[date_col, value_col]].copy()

        chart_df[date_col] = pd.to_datetime(
            chart_df[date_col],
            errors="coerce"
        )

        # Chỉ lấy dữ liệu 2012–2024
        chart_df = chart_df[
            (chart_df[date_col] >= "2012-01-01") &
            (chart_df[date_col] <= "2024-12-31")
        ]

        chart_df = chart_df.dropna(
            subset=[date_col, value_col]
        ).sort_values(date_col)

        year_ticks = pd.date_range(
            "2012-01-01",
            "2024-01-01",
            freq="YS"
        ).to_pydatetime().tolist()

        nearest = alt.selection_point(
            nearest=True,
            on="pointerover",
            fields=[date_col],
            empty=False,
        )

        base = alt.Chart(chart_df).encode(
            x=alt.X(
                f"{date_col}:T",
                title=None,
                axis=alt.Axis(
                    values=year_ticks,
                    format="%Y",
                    labelAngle=0,
                ),
            )
        )

        line = base.mark_line().encode(
            y=alt.Y(
                f"{value_col}:Q",
                title=None,
            )
        )

        points = line.mark_point(size=70).encode(
            opacity=alt.condition(
                nearest,
                alt.value(1),
                alt.value(0)
            )
        )

        selectors = base.mark_rule(
            opacity=0.001
        ).encode(
            tooltip=[
                alt.Tooltip(
                    f"{date_col}:T",
                    title="Tháng",
                    format="%m/%Y",
                ),
                alt.Tooltip(
                    f"{value_col}:Q",
                    title=selected_name,
                    format=".2f",
                ),
            ]
        ).add_params(nearest)


        chart = (
            line
            + points
            + selectors
        ).properties(
            height=360
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )
# ============================================================
# 12. PAGE — TỔNG QUAN
# ============================================================

if page == "Tổng quan":

    page_header(
        "Tổng quan",
        "Theo dõi phạm vi dữ liệu, pipeline xử lý và trực quan hóa nhanh các biến chính của bài toán dự báo CPI giao thông.",
    )

    overview_kpis()
    overview_series_chart()


# ============================================================
# 13. PAGE — DỮ LIỆU & TIỀN XỬ LÝ
# ============================================================

elif page == "Dữ liệu & Tiền xử lý":

    page_header(
        "Dữ liệu & Tiền xử lý",
        "Xem dữ liệu thô, dữ liệu trung gian, dữ liệu đã xử lý và quy trình tương ứng với các notebook 01-06.",
    )

    tab_raw, tab_interim, tab_processed= st.tabs([
        "Raw",
        "Interim",
        "Processed",
    ])

    # -------------------- RAW --------------------
    with tab_raw:
        raw_sources = list(RAW_FILES.keys())

        button_cols = st.columns(len(raw_sources), gap="small")

        for i, source_name in enumerate(raw_sources):
            active = st.session_state.raw_source == source_name

            with button_cols[i]:
                if st.button(
                    source_name,
                    key=f"raw_{i}",
                    type="primary" if active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.raw_source = source_name
                    st.rerun()

        raw_name = st.session_state.raw_source

        candidates = RAW_FILES[raw_name]
        raw_path = None

        for filename in candidates:
            p = RAW_DIR / filename
            if p.exists():
                raw_path = p
                break

        if raw_path is None:
            st.warning(
                "Không tìm thấy file tương ứng trong data/raw. "
                "Kiểm tra lại tên file trong RAW_FILES ở đầu code."
            )
        else:
            raw_df = safe_load(raw_path)

            if raw_df is None:
                st.error(f"Không đọc được {raw_path.name}")
            else:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Số dòng", f"{len(raw_df):,}")
                c2.metric("Số cột", f"{raw_df.shape[1]:,}")
                c3.metric("Missing", f"{int(raw_df.isna().sum().sum()):,}")
                c4.metric("Duplicate", f"{int(raw_df.duplicated().sum()):,}")

                section_header("Dữ liệu raw", raw_path.name)

                st.dataframe(
                    raw_df.head(150),
                    use_container_width=True,
                    hide_index=True,
                    height=420,
                )

                st.download_button(
                    label=f"Tải {raw_path.name}",
                    data=raw_path.read_bytes(),
                    file_name=raw_path.name,
                    mime="application/octet-stream",
                    key=f"download_raw_{raw_path.name}",
                    use_container_width=True,
                )

    # -------------------- INTERIM --------------------
    with tab_interim:
        interim_name = button_selector(
            "Chọn dữ liệu interim",
            list(INTERIM_FILES.keys()),
            "interim_selector",
            columns=3,
        )

        interim_path = INTERIM_DIR / INTERIM_FILES[interim_name]
        interim_df = safe_load(interim_path)

        if interim_df is None:
            st.warning(f"Chưa tìm thấy {interim_path.name}")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Số dòng", f"{len(interim_df):,}")
            c2.metric("Số cột", f"{interim_df.shape[1]:,}")
            c3.metric("Missing", f"{int(interim_df.isna().sum().sum()):,}")
            c4.metric("Duplicate", f"{int(interim_df.duplicated().sum()):,}")

            value_col = get_default_value_column(interim_df)

            if value_col:
                section_header("Diễn biến dữ liệu", value_col)
                with st.container(border=True):
                    st.line_chart(
                        prepare_time_series(interim_df, value_col),
                        height=300,
                        use_container_width=True,
                    )

            section_header("Bảng dữ liệu", interim_path.name)

            st.dataframe(
                interim_df,
                use_container_width=True,
                hide_index=True,
                height=420,
            )

            download_file_button(
                interim_path,
                f"Tải {interim_path.name}",
                f"download_interim_{interim_path.name}",
            )

    # -------------------- PROCESSED --------------------
    with tab_processed:
        processed_name = button_selector(
            "Chọn dữ liệu processed",
            list(PROCESSED_FILES.keys()),
            "processed_selector",
            columns=4,
        )

        processed_path = PROCESSED_DIR / PROCESSED_FILES[processed_name]
        processed_df = safe_load(processed_path)

        if processed_df is None:
            st.warning(f"Chưa tìm thấy {processed_path.name}")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Số dòng", f"{len(processed_df):,}")
            c2.metric("Số cột", f"{processed_df.shape[1]:,}")
            c3.metric("Missing", f"{int(processed_df.isna().sum().sum()):,}")

            st.dataframe(
                processed_df,
                use_container_width=True,
                hide_index=True,
                height=470,
            )

            download_file_button(
                processed_path,
                f"Tải {processed_path.name}",
                f"download_processed_{processed_path.name}",
            )    

# ============================================================
# 14. PAGE — PHÂN TÍCH KHÁM PHÁ
# ============================================================

elif page == "Phân tích khám phá":

    page_header(
        "Phân tích khám phá",
        "Phân tích chuỗi thời gian, thống kê mô tả, tương quan và xu hướng/seasonality của các biến.",
    )

    if MODEL_DATA is None:
        st.error("Chưa tìm thấy data/processed/model_dataset.csv")
        st.stop()

    analysis_df = MODEL_DATA.copy()
    date_col = get_date_column(analysis_df)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Chuỗi thời gian",
        "Tết & Covid",
        "Tương quan",
        "Trend & Seasonality",
    ])

    # -------------------- TIME SERIES --------------------
    with tab1:
        available_series = [
            c for c in ["CPI", "RON95", "Diesel", "Brent", "WTI", "USD_VND"]
            if c in analysis_df.columns
        ]

        # ==========================================
        # BUTTON CHỌN NHIỀU BIẾN
        # ==========================================

        if "analysis_selected_vars" not in st.session_state:
            st.session_state.analysis_selected_vars = ["CPI", "RON95", "Diesel"]

        button_cols = st.columns(len(available_series), gap="small")

        for i, col in enumerate(available_series):
            active = col in st.session_state.analysis_selected_vars

            with button_cols[i]:
                if st.button(
                    col,
                    key=f"analysis_var_{col}",
                    type="primary" if active else "secondary",
                    use_container_width=True,
                ):
                    if active:
                        st.session_state.analysis_selected_vars.remove(col)
                    else:
                        st.session_state.analysis_selected_vars.append(col)

                    st.rerun()

        selected_vars = [
            c for c in available_series
            if c in st.session_state.analysis_selected_vars
        ]

        # ==========================================
        # CHUYỂN TẤT CẢ VỀ % THAY ĐỔI THEO THÁNG
        # ==========================================

        if selected_vars:

            percent_df = pd.DataFrame()

            if date_col:
                percent_df[date_col] = analysis_df[date_col]

            for col in selected_vars:

                series = pd.to_numeric(
                    analysis_df[col],
                    errors="coerce"
                )

                # CPI vốn đã là % MoM → giữ nguyên
                if col == "CPI":
                    percent_df[col] = series

                # Các biến còn lại → % thay đổi tháng
                else:
                    percent_df[col] = (
                        series.pct_change(fill_method=None) * 100
                    )

            # ==========================================
            # THỐNG KÊ MÔ TẢ
            # ==========================================

            summary_rows = []

            for col in selected_vars:
                s = percent_df[col].dropna()

                summary_rows.append({
                    "Biến": col,
                    "Trung bình (%)": s.mean(),
                    "Độ lệch chuẩn": s.std(),
                    "Nhỏ nhất (%)": s.min(),
                    "Lớn nhất (%)": s.max(),
                })

            st.dataframe(
                pd.DataFrame(summary_rows).round(3),
                use_container_width=True,
                hide_index=True,
            )

            # ==========================================
            # BIỂU ĐỒ
            # ==========================================

            with st.container(border=True):

                if date_col:
                    plot_df = (
                        percent_df[[date_col] + selected_vars]
                        .dropna(how="all", subset=selected_vars)
                        .set_index(date_col)
                    )
                else:
                    plot_df = percent_df[selected_vars]

                st.line_chart(
                    plot_df,
                    height=370,
                    use_container_width=True,
                )

            st.caption(
                "CPI giữ nguyên ở dạng % MoM; RON95, Diesel, Brent, WTI và USD/VND "
                "được chuyển sang % thay đổi theo tháng để có thể so sánh trên cùng thang đo."
            )

    # -------------------- TET COVID --------------------
    with tab2:
        left, right = st.columns(2)

        with left:
            st.subheader("Tết Nguyên đán")

            if "Dummy_Tet" in analysis_df.columns and "CPI" in analysis_df.columns:
                tet_summary = (
                    analysis_df.groupby("Dummy_Tet")["CPI"]
                    .agg(["count", "mean", "std", "min", "max"])
                    .round(2)
                )

                rename_index = {0: "Không Tết", 1: "Tết"}
                tet_summary.index = [rename_index.get(i, i) for i in tet_summary.index]

                st.dataframe(tet_summary, use_container_width=True)
            else:
                st.info("Dataset chưa có Dummy_Tet hoặc CPI.")

        with right:
            st.subheader("Covid-19")

            if "Dummy_Covid" in analysis_df.columns and "CPI" in analysis_df.columns:
                covid_summary = (
                    analysis_df.groupby("Dummy_Covid")["CPI"]
                    .agg(["count", "mean", "std", "min", "max"])
                    .round(2)
                )

                rename_index = {0: "Ngoài Covid", 1: "Covid"}
                covid_summary.index = [rename_index.get(i, i) for i in covid_summary.index]

                st.dataframe(covid_summary, use_container_width=True)
            else:
                st.info("Dataset chưa có Dummy_Covid hoặc CPI.")

        st.info(
            "Đây là thống kê mô tả. Sự khác biệt giữa các nhóm không đồng nghĩa với quan hệ nhân quả."
        )

    # -------------------- CORRELATION --------------------
    with tab3:
        corr_df = analysis_df.copy()

        level_cols = [
            c for c in ["RON95", "Diesel", "Brent", "WTI", "USD_VND"]
            if c in corr_df.columns
        ]

        for col in level_cols:
            corr_df[f"{col}_change"] = (
                pd.to_numeric(corr_df[col], errors="coerce")
                .pct_change(fill_method=None) * 100
            )

        corr_cols = ["CPI"] if "CPI" in corr_df.columns else []
        corr_cols += [f"{c}_change" for c in level_cols]

        if len(corr_cols) >= 2:
            corr = corr_df[corr_cols].corr().round(2)

            st.dataframe(
                corr.style.background_gradient(
                    cmap="coolwarm",
                    vmin=-1,
                    vmax=1,
                ).format("{:.2f}"),
                use_container_width=True,
            )

            st.caption(
                "Các biến giá được chuyển sang % thay đổi theo tháng để phù hợp hơn với CPI dạng % MoM."
            )
        else:
            st.info("Chưa đủ biến số để tính correlation.")

    # -------------------- TREND / SEASONALITY --------------------
    with tab4:
        numeric_cols = [
            c for c in get_numeric_columns(analysis_df)
            if c not in ["Dummy_Tet", "Dummy_Covid"]
        ]

        if not numeric_cols:
            st.info("Không có biến số nào để phân tích trend/seasonality.")
            st.stop()

        selected = button_selector(
            "Chọn biến",
            numeric_cols,
            "trend_variable",
            columns=4,
        )

        series = pd.to_numeric(analysis_df[selected], errors="coerce")

        trend_df = pd.DataFrame({
            "Observed": series,
            "MA3": series.rolling(3, center=True).mean(),
            "MA12": series.rolling(12, center=True).mean(),
        })

        if date_col:
            trend_df.index = analysis_df[date_col]

        with st.container(border=True):
            st.line_chart(
                trend_df,
                height=350,
                use_container_width=True,
            )

        if date_col:
            month = pd.to_datetime(analysis_df[date_col], errors="coerce").dt.month
            season_df = pd.DataFrame({
                "Month": month,
                "Value": series,
            }).dropna()

            seasonality = (
                season_df.groupby("Month")["Value"]
                .mean()
                .reindex(range(1, 13))
            )

            section_header("Seasonality theo tháng", "Trung bình theo tháng trong năm")
            st.bar_chart(seasonality, height=280)

        st.caption(
            "MA3 và MA12 dùng để quan sát trend trực quan; đây không phải decomposition thống kê chính thức."
        )


# ============================================================
# 15. PAGE — FEATURE ENGINEERING
# ============================================================

elif page == "Feature Engineering":

    page_header(
        "Feature Engineering",
        "Kiểm tra các feature đã tạo trong notebook 08 và xem trực tiếp feature_dataset.csv.",
    )

    if FEATURE_DATA is None:
        st.error("Chưa tìm thấy data/processed/feature_dataset.csv")
        st.stop()

    feature_df = FEATURE_DATA.copy()

    groups = {
        "Lag": [
            c for c in feature_df.columns
            if "lag" in normalize_text(c)
        ],
        "% change / diff": [
            c for c in feature_df.columns
            if any(
                key in normalize_text(c)
                for key in ["change", "pct", "diff", "growth", "mom", "yoy"]
            )
        ],
        "Moving average / rolling": [
            c for c in feature_df.columns
            if any(
                key in normalize_text(c)
                for key in ["rolling", "moving", "_ma", "mean_", "std_"]
            )
        ],
        "Dummy / seasonality": [
            c for c in feature_df.columns
            if any(
                key in normalize_text(c)
                for key in ["dummy", "tet", "covid", "month_sin", "month_cos", "season"]
            )
        ],
    }

    c1, c2, c3, c4 = st.columns(4)

    for card, (name, cols) in zip(
        [c1, c2, c3, c4],
        groups.items(),
    ):
        card.metric(name, len(cols))

    section_header("Danh sách feature", "Lọc theo nhóm hoặc tên feature")

    group_choice = button_selector(
        "Nhóm feature",
        ["Tất cả"] + list(groups.keys()),
        "feature_group",
        columns=5,
    )

    if group_choice == "Tất cả":
        feature_list = list(feature_df.columns)
    else:
        feature_list = groups[group_choice]

    st.dataframe(
        pd.DataFrame({"Feature": feature_list}),
        use_container_width=True,
        hide_index=True,
        height=min(420, 80 + max(1, len(feature_list)) * 34),
    )

    section_header("Feature dataset", f"{len(feature_df):,} dòng · {feature_df.shape[1]} cột")

    if "feature_preview_cols" not in st.session_state:
        st.session_state.feature_preview_cols = list(
            feature_df.columns[:min(6, len(feature_df.columns))]
        )

    all_cols = list(feature_df.columns)

    button_options = ["Tất cả"] + all_cols

    for start in range(0, len(button_options), 6):
        row_options = button_options[start:start + 6]
        buttons = st.columns(6, gap="small")

        for i, option in enumerate(row_options):

            if option == "Tất cả":
                active = len(st.session_state.feature_preview_cols) == len(all_cols)
            else:
                active = option in st.session_state.feature_preview_cols

            with buttons[i]:
                if st.button(
                    option,
                    key=f"feature_preview_{option}",
                    type="primary" if active else "secondary",
                    use_container_width=True,
                ):

                    if option == "Tất cả":
                        if active:
                            st.session_state.feature_preview_cols = []
                        else:
                            st.session_state.feature_preview_cols = all_cols.copy()

                    else:
                        if active:
                            st.session_state.feature_preview_cols.remove(option)
                        else:
                            st.session_state.feature_preview_cols.append(option)

                    st.rerun()

    preview_cols = [
        c for c in all_cols
        if c in st.session_state.feature_preview_cols
    ]

    if preview_cols:
        st.dataframe(
            feature_df[preview_cols],
            use_container_width=True,
            hide_index=True,
            height=460,
        )

    feature_path = PROCESSED_DIR / PROCESSED_FILES["Feature dataset"]
    download_file_button(
        feature_path,
        "Tải feature_dataset.csv",
        "download_feature_dataset",
    )

    # Tương quan feature-target như một hỗ trợ giải thích feature
    if "CPI" in feature_df.columns:
        numeric_cols = get_numeric_columns(feature_df)

        if "CPI" in numeric_cols:
            corr = (
                feature_df[numeric_cols]
                .apply(pd.to_numeric, errors="coerce")
                .corr()["CPI"]
                .drop(labels=["CPI"], errors="ignore")
                .dropna()
                .sort_values(key=np.abs, ascending=False)
                .head(15)
            )

            if not corr.empty:
                section_header(
                    "Feature liên hệ mạnh với CPI",
                    "Tương quan tuyến tính · không phải feature importance",
                )

                corr_table = corr.rename("Correlation").reset_index()
                corr_table.columns = ["Feature", "Correlation"]

                st.dataframe(
                    corr_table.style.format({"Correlation": "{:.3f}"}),
                    use_container_width=True,
                    hide_index=True,
                )


# ============================================================
# 16. PAGE — MÔ HÌNH & KẾT QUẢ
# Gộp: cấu hình + validation + ensemble + test + predictions
# ============================================================

elif page == "Mô hình & Kết quả":

    page_header(
        "Mô hình & Kết quả",
        "Xem cấu hình mô hình, Validation, Ensemble, đánh giá Test và Actual vs Predicted trên cùng một trang.",
    )

    tabs = st.tabs([
        "Cấu hình",
        "Validation",
        "Test metrics",
        "Actual vs Predicted",
        "Residual",
        "Mô hình tham chiếu",
    ])

    # -------------------- CONFIG --------------------
    with tabs[0]:
        model = button_selector("Chọn mô hình", ["Naive", "ElasticNet", "ARIMAX", "Ensemble"], "model_config_selector", columns=4)

        if model == "Naive":
            
            with st.container(border=True):
                st.subheader("Naive Model")

                st.write(
                    "Dự báo CPI tháng hiện tại bằng CPI của tháng liền trước."
                )

                st.code("ŷ(t) = y(t-1)")

            # Tự chạy Naive một lần và lưu kết quả
            if "naive_result" not in st.session_state:
                st.session_state.naive_result = run_naive_validation(
                    FEATURE_DATA
                )

            result = st.session_state.naive_result

            st.metric(
                "Validation RMSE",
                f"{result['rmse']:.4f}",
            )

            st.dataframe(
                result["predictions"],
                use_container_width=True,
                hide_index=True,
            )

            st.line_chart(
                result["predictions"]
                .set_index("MonthYear")[["Actual", "Prediction"]],
                height=320,
            )
        elif model == "ElasticNet":

            available_features = [
                c for c in get_numeric_columns(FEATURE_DATA)
                if c != "CPI"
            ]

            best_elastic_features = [
                c for c in ELASTICNET_FEATURES
                if c in available_features
            ]

            # Khôi phục cấu hình ElasticNet đã chạy gần nhất
            if "elastic_config" in st.session_state:
                saved_alpha, saved_l1, saved_features = st.session_state.elastic_config

                if "elastic_alpha" not in st.session_state:
                    st.session_state.elastic_alpha = saved_alpha

                if "elastic_l1_ratio" not in st.session_state:
                    st.session_state.elastic_l1_ratio = saved_l1

                if "elastic_features" not in st.session_state:
                    st.session_state.elastic_features = list(saved_features)

            else:
                # Lần đầu mở ElasticNet
                if "elastic_alpha" not in st.session_state:
                    st.session_state.elastic_alpha = 0.1

                if "elastic_l1_ratio" not in st.session_state:
                    st.session_state.elastic_l1_ratio = 0.9

                if "elastic_features" not in st.session_state:
                    st.session_state.elastic_features = available_features.copy()

            def use_best_elasticnet():
                st.session_state.elastic_alpha = 0.1
                st.session_state.elastic_l1_ratio = 0.9
                st.session_state.elastic_features = best_elastic_features.copy()


            c1, c2 = st.columns(2)

            with c1:
                alpha = st.number_input(
                    "Alpha",
                    min_value=0.001,
                    max_value=10.0,
                    step=0.01,
                    key="elastic_alpha",
                )

            with c2:
                l1_ratio = st.number_input(
                    "L1 Ratio",
                    min_value=0.0,
                    max_value=1.0,
                    step=0.1,
                    key="elastic_l1_ratio",
                )

            selected_features = st.multiselect(
                "Feature sử dụng",
                available_features,
                key="elastic_features",
            )

            elastic_config = (
                float(alpha),
                float(l1_ratio),
                tuple(selected_features),
            )

            old_elastic_config = st.session_state.get("elastic_config")

            st.button(
                "Dùng cấu hình tốt nhất",
                on_click=use_best_elasticnet,
                use_container_width=True,
            )

            if st.button(
                "Chạy ElasticNet",
                type="primary",
                use_container_width=True,
            ):

                if not selected_features:
                    st.warning("Bạn phải chọn ít nhất một feature.")

                else:
                    if (
                        old_elastic_config != elastic_config
                        or "elastic_result" not in st.session_state
                    ):
                        with st.spinner(
                            "Đang chạy Expanding-window Validation..."
                        ):
                            st.session_state.elastic_result = (
                                run_elasticnet_validation(
                                    FEATURE_DATA,
                                    alpha=alpha,
                                    l1_ratio=l1_ratio,
                                    feature_cols=selected_features,
                                )
                            )

                        st.session_state.elastic_config = elastic_config

            if (
                "elastic_result" in st.session_state
                and st.session_state.get("elastic_config") == elastic_config
            ):
                result = st.session_state.elastic_result

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Alpha",
                    f"{result['alpha']:.3f}",
                )

                c2.metric(
                    "L1 Ratio",
                    f"{result['l1_ratio']:.2f}",
                )

                c3.metric(
                    "Validation RMSE",
                    f"{result['rmse']:.4f}",
                )

                st.dataframe(
                    result["predictions"],
                    use_container_width=True,
                    hide_index=True,
                )

                st.line_chart(
                    result["predictions"]
                    .set_index("MonthYear")[
                        ["Actual", "Prediction"]
                    ],
                    height=320,
                )

        elif model == "ARIMAX":
                best_arimax_exog = [
                    "RON95_change_lag1",
                    "Diesel_change_lag1",
                    "Brent_change_lag1",
                    "USD_VND_change_lag1",
                ]

                available_exog = [
                    c for c in FEATURE_DATA.columns
                    if c not in [
                        "MonthYear",
                        "CPI",
                        "CPI_lag1",
                        "CPI_lag2",
                    ]
                ]

                # Khôi phục cấu hình ARIMAX đã chạy gần nhất
                if "arimax_config" in st.session_state:
                    saved_p, saved_d, saved_q, saved_exog = st.session_state.arimax_config

                    if "arimax_p" not in st.session_state:
                        st.session_state.arimax_p = saved_p

                    if "arimax_d" not in st.session_state:
                        st.session_state.arimax_d = saved_d

                    if "arimax_q" not in st.session_state:
                        st.session_state.arimax_q = saved_q

                    if "arimax_exog" not in st.session_state:
                        st.session_state.arimax_exog = list(saved_exog)

                else:
                    # Lần đầu mở ARIMAX
                    if "arimax_p" not in st.session_state:
                        st.session_state.arimax_p = 1

                    if "arimax_d" not in st.session_state:
                        st.session_state.arimax_d = 0

                    if "arimax_q" not in st.session_state:
                        st.session_state.arimax_q = 2

                    if "arimax_exog" not in st.session_state:
                        st.session_state.arimax_exog = available_exog.copy()

                def use_best_arimax():
                    st.session_state.arimax_p = 1
                    st.session_state.arimax_d = 0
                    st.session_state.arimax_q = 2
                    st.session_state.arimax_exog = best_arimax_exog.copy()

                c1, c2, c3 = st.columns(3)

                with c1:
                    p = st.number_input(
                        "p",
                        min_value=0,
                        max_value=5,
                        step=1,
                        key="arimax_p",
                    )

                with c2:
                    d = st.number_input(
                        "d",
                        min_value=0,
                        max_value=2,
                        step=1,
                        key="arimax_d",
                    )

                with c3:
                    q = st.number_input(
                        "q",
                        min_value=0,
                        max_value=5,
                        step=1,
                        key="arimax_q",
                    )

                available_exog = [
                    c for c in FEATURE_DATA.columns
                    if c not in [
                        "MonthYear",
                        "CPI",
                        "CPI_lag1",
                        "CPI_lag2",
                    ]
                ]

                selected_exog = st.multiselect(
                        "Biến ngoại sinh",
                        available_exog,
                        key="arimax_exog",
                    )

                st.button(
                    "Dùng cấu hình tốt nhất",
                    on_click=use_best_arimax,
                    use_container_width=True,
                )

                arimax_config = (int(p), int(d), int(q), tuple(selected_exog))

                old_config = st.session_state.get("arimax_config")
                if st.button(
                    "Chạy ARIMAX",
                    type="primary",
                    use_container_width=True,
                ):

                    if not selected_exog:
                        st.warning("Bạn phải chọn ít nhất một biến ngoại sinh.")

                    else:
                        if (
                            old_config != arimax_config
                            or "arimax_result" not in st.session_state
                        ):
                            with st.spinner(
                                "Đang chạy Expanding-window Validation..."
                            ):
                                st.session_state.arimax_result = run_arimax_validation(
                                    FEATURE_DATA,
                                    p=int(p),
                                    d=int(d),
                                    q=int(q),
                                    exog_cols=selected_exog,
                                )

                            st.session_state.arimax_config = arimax_config


                if (
                    "arimax_result" in st.session_state
                    and st.session_state.get("arimax_config") == arimax_config
                ):
                    result = st.session_state.arimax_result

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric("p", result["p"])
                    c2.metric("d", result["d"])
                    c3.metric("q", result["q"])
                    c4.metric(
                        "Validation RMSE",
                        f"{result['rmse']:.4f}",
                    )

                    st.dataframe(
                        result["predictions"],
                        use_container_width=True,
                        hide_index=True,
                    )

                    st.line_chart(
                        result["predictions"]
                        .set_index("MonthYear")[["Actual", "Prediction"]],
                        height=320,
                    )

        elif model == "Ensemble":

            # =====================================================
            # 1. NAIVE KHÔNG CẦN TUNE -> TỰ TÍNH NẾU CHƯA CÓ
            # =====================================================

            if "naive_result" not in st.session_state:
                st.session_state.naive_result = run_naive_validation(
                    FEATURE_DATA
                )

            # =====================================================
            # 2. CHỌN CẶP MÔ HÌNH
            # =====================================================

            pair_options = [
                "ElasticNet + ARIMAX",
                "Naive + ElasticNet",
                "Naive + ARIMAX",
            ]

            selected_pair = button_selector(
                "Chọn cặp mô hình",
                pair_options,
                "ensemble_pair_selector",
                columns=3,
            )

            pair_map = {
                "ElasticNet + ARIMAX": (
                    "ElasticNet",
                    "ARIMAX",
                ),
                "Naive + ElasticNet": (
                    "Naive",
                    "ElasticNet",
                ),
                "Naive + ARIMAX": (
                    "Naive",
                    "ARIMAX",
                ),
            }

            model_1, model_2 = pair_map[selected_pair]

            st.write(
                f"Ensemble đang kết hợp **{model_1} + {model_2}** "
                "bằng phương pháp Weighted Averaging."
            )

            st.code(
                f"ŷ_ensemble = w₁ × ŷ_{model_1} + w₂ × ŷ_{model_2}"
            )

            # =====================================================
            # 3. HELPER LẤY KẾT QUẢ MODEL
            # =====================================================

            def model_result_key(model_name):

                if model_name == "Naive":
                    return "naive_result"

                if model_name == "ElasticNet":
                    return "elastic_result"

                if model_name == "ARIMAX":
                    return "arimax_result"


            def model_config_key(model_name):

                if model_name == "ElasticNet":
                    return "elastic_config"

                if model_name == "ARIMAX":
                    return "arimax_config"

                return None


            def model_is_ready(model_name):

                result_key = model_result_key(model_name)

                if result_key not in st.session_state:
                    return False

                config_key = model_config_key(model_name)

                if config_key is not None:
                    return config_key in st.session_state

                return True


            def get_model_result(model_name):

                return st.session_state[
                    model_result_key(model_name)
                ]


            ready_1 = model_is_ready(model_1)
            ready_2 = model_is_ready(model_2)

            # =====================================================
            # 4. HIỂN THỊ THÔNG TIN 2 MODEL
            # =====================================================

            c1, c2 = st.columns(2)

            with c1:

                st.markdown(f"**{model_1} hiện tại**")

                if ready_1:

                    result_1 = get_model_result(model_1)

                    if model_1 == "ElasticNet":

                        config = st.session_state.elastic_config

                        st.write(
                            f"Alpha = `{config[0]:.3f}` · "
                            f"L1 Ratio = `{config[1]:.2f}` · "
                            f"{len(config[2])} features"
                        )

                    elif model_1 == "ARIMAX":

                        config = st.session_state.arimax_config

                        st.write(
                            f"ARIMA({config[0]}, {config[1]}, {config[2]}) · "
                            f"{len(config[3])} biến ngoại sinh"
                        )

                    else:

                        st.write(
                            "Naive: ŷ(t) = y(t-1)"
                        )

                    st.metric(
                        f"RMSE {model_1}",
                        f"{result_1['rmse']:.4f}",
                    )

                else:

                    st.warning(
                        f"Chưa chạy {model_1}."
                    )

            with c2:

                st.markdown(f"**{model_2} hiện tại**")

                if ready_2:

                    result_2 = get_model_result(model_2)

                    if model_2 == "ElasticNet":

                        config = st.session_state.elastic_config

                        st.write(
                            f"Alpha = `{config[0]:.3f}` · "
                            f"L1 Ratio = `{config[1]:.2f}` · "
                            f"{len(config[2])} features"
                        )

                    elif model_2 == "ARIMAX":

                        config = st.session_state.arimax_config

                        st.write(
                            f"ARIMA({config[0]}, {config[1]}, {config[2]}) · "
                            f"{len(config[3])} biến ngoại sinh"
                        )

                    else:

                        st.write(
                            "Naive: ŷ(t) = y(t-1)"
                        )

                    st.metric(
                        f"RMSE {model_2}",
                        f"{result_2['rmse']:.4f}",
                    )

                else:

                    st.warning(
                        f"Chưa chạy {model_2}."
                    )

            # =====================================================
            # 5. KIỂM TRA NẾU NSD ĐỔI CẶP MODEL
            # =====================================================

            if "ensemble_pair_saved" not in st.session_state:

                st.session_state.ensemble_pair_saved = selected_pair

            elif (
                st.session_state.ensemble_pair_saved
                != selected_pair
            ):

                st.session_state.ensemble_pair_saved = selected_pair

                # Khi đổi cặp -> trở về chế độ tự thiết kế
                st.session_state.ensemble_mode = "custom"

                # Tránh giữ trọng số của cặp trước
                st.session_state.ensemble_weights_saved = (
                    0.5,
                    0.5,
                )

                st.session_state.ensemble_weight_1 = 0.5
                st.session_state.ensemble_weight_2 = 0.5

            # =====================================================
            # 6. KHỞI TẠO TRỌNG SỐ
            # =====================================================

            if "ensemble_mode" not in st.session_state:
                st.session_state.ensemble_mode = "custom"

            if "ensemble_weights_saved" not in st.session_state:

                # Cặp mặc định của đề tài
                if selected_pair == "ElasticNet + ARIMAX":

                    st.session_state.ensemble_weights_saved = (
                        float(ENSEMBLE_WEIGHT_ELASTIC),
                        float(ENSEMBLE_WEIGHT_ARIMAX),
                    )

                else:

                    st.session_state.ensemble_weights_saved = (
                        0.5,
                        0.5,
                    )

            if "ensemble_weight_1" not in st.session_state:

                st.session_state.ensemble_weight_1 = (
                    st.session_state.ensemble_weights_saved[0]
                )

            if "ensemble_weight_2" not in st.session_state:

                st.session_state.ensemble_weight_2 = (
                    st.session_state.ensemble_weights_saved[1]
                )

            # =====================================================
            # 7. CALLBACK LƯU TRỌNG SỐ
            # =====================================================

            def save_ensemble_weights():

                st.session_state.ensemble_weights_saved = (
                    float(st.session_state.ensemble_weight_1),
                    float(st.session_state.ensemble_weight_2),
                )

            # =====================================================
            # 8. TRỌNG SỐ THEO RMSE HIỆN TẠI
            # =====================================================

            def use_current_rmse_weights():

                result_1 = get_model_result(model_1)
                result_2 = get_model_result(model_2)

                rmse_1 = float(result_1["rmse"])
                rmse_2 = float(result_2["rmse"])

                inv_1 = 1 / rmse_1
                inv_2 = 1 / rmse_2

                weight_1 = (
                    inv_1 / (inv_1 + inv_2)
                )

                weight_2 = (
                    inv_2 / (inv_1 + inv_2)
                )

                st.session_state.ensemble_weight_1 = weight_1
                st.session_state.ensemble_weight_2 = weight_2

                st.session_state.ensemble_weights_saved = (
                    weight_1,
                    weight_2,
                )

                st.session_state.ensemble_mode = "current"

            # =====================================================
            # 9. TRỌNG SỐ TỐI ƯU CỦA ĐỀ TÀI
            # chỉ áp dụng ElasticNet + ARIMAX
            # =====================================================

            def use_best_ensemble():

                st.session_state.ensemble_weight_1 = float(
                    ENSEMBLE_WEIGHT_ELASTIC
                )

                st.session_state.ensemble_weight_2 = float(
                    ENSEMBLE_WEIGHT_ARIMAX
                )

                st.session_state.ensemble_weights_saved = (
                    float(ENSEMBLE_WEIGHT_ELASTIC),
                    float(ENSEMBLE_WEIGHT_ARIMAX),
                )

                st.session_state.ensemble_mode = "best"

            # =====================================================
            # 10. TỰ THIẾT KẾ
            # =====================================================

            def use_custom_ensemble():

                st.session_state.ensemble_mode = "custom"

            # =====================================================
            # 11. BUTTON CHỌN CÁCH TẠO TRỌNG SỐ
            # =====================================================

            mode = st.session_state.ensemble_mode

            c1, c2, c3 = st.columns(3)

            with c1:

                st.button(
                    "Theo RMSE hiện tại",
                    on_click=use_current_rmse_weights,
                    disabled=not (ready_1 and ready_2),
                    type=(
                        "primary"
                        if mode == "current"
                        else "secondary"
                    ),
                    use_container_width=True,
                )

            with c2:

                st.button(
                    "Tối ưu của đề tài",
                    on_click=use_best_ensemble,
                    disabled=(
                        selected_pair
                        != "ElasticNet + ARIMAX"
                    ),
                    type=(
                        "primary"
                        if mode == "best"
                        else "secondary"
                    ),
                    use_container_width=True,
                )

            with c3:

                st.button(
                    "Tự thiết kế",
                    on_click=use_custom_ensemble,
                    type=(
                        "primary"
                        if mode == "custom"
                        else "secondary"
                    ),
                    use_container_width=True,
                )

            if not (ready_1 and ready_2):

                st.info(
                    "Cần chạy đủ hai mô hình được chọn "
                    "trước khi tính trọng số theo RMSE."
                )

            if selected_pair != "ElasticNet + ARIMAX":

                st.caption(
                    "Trọng số tối ưu của đề tài chỉ được xác định "
                    "cho cặp ElasticNet + ARIMAX."
                )

            # =====================================================
            # 12. INPUT TRỌNG SỐ
            # =====================================================

            is_locked = (
                st.session_state.ensemble_mode != "custom"
            )

            c1, c2 = st.columns(2)

            with c1:

                weight_1 = st.number_input(
                    f"Trọng số {model_1}",
                    min_value=0.0,
                    max_value=1.0,
                    step=0.01,
                    format="%.3f",
                    key="ensemble_weight_1",
                    disabled=is_locked,
                    on_change=save_ensemble_weights,
                )

            with c2:

                weight_2 = st.number_input(
                    f"Trọng số {model_2}",
                    min_value=0.0,
                    max_value=1.0,
                    step=0.01,
                    format="%.3f",
                    key="ensemble_weight_2",
                    disabled=is_locked,
                    on_change=save_ensemble_weights,
                )

            # =====================================================
            # 13. CHẾ ĐỘ HIỆN TẠI
            # =====================================================

            if mode == "current":

                st.caption(
                    "🔒 Trọng số được tính từ RMSE Validation "
                    "của hai mô hình hiện tại."
                )

            elif mode == "best":

                st.caption(
                    "🔒 Đang sử dụng trọng số tối ưu "
                    "ElasticNet + ARIMAX của đề tài."
                )

            else:

                st.caption(
                    "✏️ Chế độ tự thiết kế: "
                    "NSD có thể thay đổi trọng số."
                )

            # =====================================================
            # 14. KIỂM TRA TỔNG TRỌNG SỐ
            # =====================================================

            total_weight = (
                weight_1 + weight_2
            )

            if abs(total_weight - 1.0) > 0.001:

                st.warning(
                    f"Tổng trọng số hiện tại = {total_weight:.3f}. "
                    "Tổng trọng số phải bằng 1."
                )

            # =====================================================
            # 15. SIGNATURE CỦA MODEL
            # =====================================================

            def get_model_signature(model_name):

                if model_name == "Naive":
                    return ("Naive",)

                if model_name == "ElasticNet":
                    return st.session_state.get(
                        "elastic_config"
                    )

                if model_name == "ARIMAX":
                    return st.session_state.get(
                        "arimax_config"
                    )


            ensemble_signature = (
                selected_pair,
                get_model_signature(model_1),
                get_model_signature(model_2),
                round(float(weight_1), 8),
                round(float(weight_2), 8),
            )

            # Lưu riêng kết quả của từng cặp Ensemble
            if "ensemble_results" not in st.session_state:
                st.session_state.ensemble_results = {}

            # =====================================================
            # 16. ĐÁNH GIÁ ENSEMBLE
            # =====================================================

            if st.button(
                "Đánh giá Ensemble",
                type="primary",
                use_container_width=True,
            ):

                if not ready_1:

                    st.warning(
                        f"Bạn cần chạy {model_1} trước."
                    )

                elif not ready_2:

                    st.warning(
                        f"Bạn cần chạy {model_2} trước."
                    )

                elif abs(total_weight - 1.0) > 0.001:

                    st.warning(
                        "Tổng trọng số phải bằng 1 "
                        "trước khi đánh giá."
                    )

                else:

                    ensemble_result = run_ensemble_validation(
                        get_model_result(model_1),
                        get_model_result(model_2),
                        weight_1,
                        weight_2,
                        model_1,
                        model_2,
                    )

                    st.session_state.ensemble_results[selected_pair] = {
                        "result": ensemble_result,
                        "signature": ensemble_signature,
                    }

            # =====================================================
            # 17. HIỂN THỊ KẾT QUẢ CỦA CẶP ĐANG CHỌN
            # =====================================================

            current_ensemble = st.session_state.ensemble_results.get(
                selected_pair
            )

            if (
                current_ensemble is not None
                and current_ensemble["signature"] == ensemble_signature
            ):

                result = current_ensemble["result"]

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    f"Weight {result['model_1']}",
                    f"{result['weight_1']:.3f}",
                )

                c2.metric(
                    f"Weight {result['model_2']}",
                    f"{result['weight_2']:.3f}",
                )

                c3.metric(
                    "Validation RMSE",
                    f"{result['rmse']:.4f}",
                )

                st.dataframe(
                    result["predictions"],
                    use_container_width=True,
                    hide_index=True,
                )

                st.line_chart(
                    result["predictions"]
                    .set_index("MonthYear")[
                        ["Actual", "Prediction"]
                    ],
                    height=320,
                )

            elif current_ensemble is not None:

                st.info(
                    "Cấu hình mô hình hoặc trọng số của cặp này "
                    "đã thay đổi. Bấm 'Đánh giá Ensemble' để cập nhật."
                )

    # -------------------- VALIDATION --------------------
    with tabs[1]:

        st.markdown(
            """
    **Development:** 01/2012 – 12/2021  
    **Expanding-window Validation:** 01/2018 – 12/2021  
    **Số fold:** 48  
    **Test:** 01/2022 – 12/2024, không dùng để tune mô hình.
    """
        )

        # =====================================================
        # 1. GOM CÁC KẾT QUẢ VALIDATION ĐÃ CÓ
        # =====================================================

        validation_rows = []

        # ---------------- NAIVE ----------------
        if "naive_result" not in st.session_state:
            st.session_state.naive_result = run_naive_validation(
                FEATURE_DATA
            )

        validation_rows.append({
            "Model": "Naive",
            "Loại": "Mô hình đơn",
            "RMSE": float(
                st.session_state.naive_result["rmse"]
            ),
        })

        # ---------------- ELASTICNET ----------------
        if (
            "elastic_result" in st.session_state
            and "elastic_config" in st.session_state
        ):
            validation_rows.append({
                "Model": "ElasticNet",
                "Loại": "Mô hình đơn",
                "RMSE": float(
                    st.session_state.elastic_result["rmse"]
                ),
            })

        # ---------------- ARIMAX ----------------
        if (
            "arimax_result" in st.session_state
            and "arimax_config" in st.session_state
        ):
            validation_rows.append({
                "Model": "ARIMAX",
                "Loại": "Mô hình đơn",
                "RMSE": float(
                    st.session_state.arimax_result["rmse"]
                ),
            })

        # =====================================================
        # 2. ENSEMBLE ĐÃ CHẠY
        # =====================================================

        if "ensemble_results" in st.session_state:

            pair_map_validation = {
                "ElasticNet + ARIMAX": (
                    "ElasticNet",
                    "ARIMAX",
                ),
                "Naive + ElasticNet": (
                    "Naive",
                    "ElasticNet",
                ),
                "Naive + ARIMAX": (
                    "Naive",
                    "ARIMAX",
                ),
            }

            def validation_model_signature(model_name):

                if model_name == "Naive":
                    return ("Naive",)

                if model_name == "ElasticNet":
                    return st.session_state.get(
                        "elastic_config"
                    )

                if model_name == "ARIMAX":
                    return st.session_state.get(
                        "arimax_config"
                    )

            for pair_name, saved in (
                st.session_state.ensemble_results.items()
            ):

                if pair_name not in pair_map_validation:
                    continue

                model_1, model_2 = (
                    pair_map_validation[pair_name]
                )

                saved_signature = saved["signature"]

                # Signature lưu lúc Ensemble được đánh giá:
                # (
                #   pair,
                #   config model 1,
                #   config model 2,
                #   weight 1,
                #   weight 2
                # )

                current_model_1_signature = (
                    validation_model_signature(model_1)
                )

                current_model_2_signature = (
                    validation_model_signature(model_2)
                )

                # Nếu ElasticNet / ARIMAX đã đổi cấu hình
                # thì Ensemble cũ không còn hợp lệ
                is_current = (
                    saved_signature[0] == pair_name
                    and saved_signature[1]
                    == current_model_1_signature
                    and saved_signature[2]
                    == current_model_2_signature
                )

                if not is_current:
                    continue

                ensemble_result = saved["result"]

                validation_rows.append({
                    "Model": pair_name,
                    "Loại": "Ensemble",
                    "RMSE": float(
                        ensemble_result["rmse"]
                    ),
                })

        # =====================================================
        # 3. HIỂN THỊ BẢNG SO SÁNH
        # =====================================================

        val_df = pd.DataFrame(validation_rows)

        if val_df.empty:

            st.info(
                "Chưa có kết quả Validation để so sánh."
            )

        else:

            val_df = (
                val_df
                .sort_values("RMSE")
                .reset_index(drop=True)
            )

            val_df.insert(
                0,
                "Xếp hạng",
                range(1, len(val_df) + 1),
            )

            st.dataframe(
                val_df.style.format({
                    "RMSE": "{:.4f}"
                }),
                use_container_width=True,
                hide_index=True,
            )

            # =================================================
            # 4. MÔ HÌNH TỐT NHẤT
            # =================================================

            best_row = val_df.iloc[0]

            best_model = best_row["Model"]
            best_rmse = float(best_row["RMSE"])

            st.success(
                f"Mô hình có RMSE Validation thấp nhất hiện tại: "
                f"**{best_model}** — RMSE = **{best_rmse:.4f}**"
            )

            # Lưu để bước sau dùng khi fit Development
            st.session_state.validation_best_model = (
                best_model
            )

            st.session_state.validation_best_rmse = (
                best_rmse
            )

            # =================================================
            # 5. CHỌN VÀ CHỐT MÔ HÌNH
            # =================================================

            validated_models = val_df["Model"].tolist()

            # Mặc định chọn mô hình tốt nhất
            if (
                "final_model_selector" not in st.session_state
                or st.session_state.final_model_selector
                not in validated_models
            ):
                st.session_state.final_model_selector = best_model


            selected_final_model = button_selector(
                "Chọn mô hình để chốt",
                validated_models,
                "final_model_selector",
                columns=min(4, len(validated_models)),
            )


            if st.button(
                "Chốt mô hình",
                type="primary",
                use_container_width=True,
            ):

                selected_row = val_df[
                    val_df["Model"] == selected_final_model
                ].iloc[0]

                st.session_state.final_model = (
                    selected_final_model
                )

                st.session_state.final_model_validation_rmse = float(
                    selected_row["RMSE"]
                )

                # =================================================
                # LƯU SNAPSHOT CẤU HÌNH ĐÃ CHỐT
                # =================================================

                if selected_final_model == "Naive":

                    st.session_state.final_model_spec = {
                        "type": "single",
                        "model": "Naive",
                    }


                elif selected_final_model == "ElasticNet":

                    alpha_saved, l1_saved, features_saved = (
                        st.session_state.elastic_config
                    )

                    st.session_state.final_model_spec = {
                        "type": "single",
                        "model": "ElasticNet",
                        "alpha": float(alpha_saved),
                        "l1_ratio": float(l1_saved),
                        "features": list(features_saved),
                    }


                elif selected_final_model == "ARIMAX":

                    p_saved, d_saved, q_saved, exog_saved = (
                        st.session_state.arimax_config
                    )

                    st.session_state.final_model_spec = {
                        "type": "single",
                        "model": "ARIMAX",
                        "p": int(p_saved),
                        "d": int(d_saved),
                        "q": int(q_saved),
                        "exog": list(exog_saved),
                    }


                else:
                    # =============================================
                    # ENSEMBLE
                    # =============================================

                    saved_ensemble = (
                        st.session_state.ensemble_results[
                            selected_final_model
                        ]
                    )

                    ensemble_result = saved_ensemble["result"]
                    ensemble_signature = saved_ensemble["signature"]

                    model_1 = ensemble_result["model_1"]
                    model_2 = ensemble_result["model_2"]

                    # Config model 1 / model 2 tại đúng thời điểm
                    # Ensemble được Validation
                    config_1 = ensemble_signature[1]
                    config_2 = ensemble_signature[2]

                    st.session_state.final_model_spec = {
                        "type": "ensemble",

                        "pair": selected_final_model,

                        "model_1": model_1,
                        "model_2": model_2,

                        "weight_1": float(
                            ensemble_result["weight_1"]
                        ),

                        "weight_2": float(
                            ensemble_result["weight_2"]
                        ),

                        "config_1": config_1,
                        "config_2": config_2,
                    }

            if "final_model" in st.session_state:

                st.success(
                    f"Đã chốt mô hình: "
                    f"**{st.session_state.final_model}** "
                    f"— Validation RMSE = "
                    f"**{st.session_state.final_model_validation_rmse:.4f}**"
                )

    # -------------------- TEST METRICS --------------------
# -------------------- TEST METRICS --------------------
    with tabs[2]:

        st.markdown(
            """
    **Test:** 01/2022 – 12/2024  
    Mô hình được fit lại trên toàn bộ **Development 2012–2021** bằng cấu hình đã chốt từ Validation.
    """
        )

        # =====================================================
        # 1. CHƯA CHỐT MODEL
        # =====================================================

        if "final_model_spec" not in st.session_state:

            st.info(
                "Chưa có mô hình được chốt. "
                "Hãy sang tab Validation và bấm 'Chốt mô hình' trước."
            )

        else:

            final_spec = st.session_state.final_model_spec
            final_model_name = st.session_state.final_model

            st.success(
                f"Mô hình đã chốt: **{final_model_name}** "
                f"— Validation RMSE = "
                f"**{st.session_state.final_model_validation_rmse:.4f}**"
            )

            # =================================================
            # 2. HELPER CHẠY TEST CHO MODEL THÀNH PHẦN
            # =================================================

            def run_saved_model_test(
                model_name,
                config=None,
            ):

                # ---------------- NAIVE ----------------
                if model_name == "Naive":

                    return run_naive_test(
                        FEATURE_DATA
                    )

                # ---------------- ELASTICNET ----------------
                if model_name == "ElasticNet":

                    alpha_saved = float(config[0])
                    l1_saved = float(config[1])
                    features_saved = list(config[2])

                    return run_elasticnet_test(
                        FEATURE_DATA,
                        alpha=alpha_saved,
                        l1_ratio=l1_saved,
                        feature_cols=features_saved,
                    )

                # ---------------- ARIMAX ----------------
                if model_name == "ARIMAX":

                    p_saved = int(config[0])
                    d_saved = int(config[1])
                    q_saved = int(config[2])
                    exog_saved = list(config[3])

                    return run_arimax_test(
                        FEATURE_DATA,
                        p=p_saved,
                        d=d_saved,
                        q=q_saved,
                        exog_cols=exog_saved,
                    )

            # =================================================
            # 3. SIGNATURE CẤU HÌNH ĐÃ CHỐT
            # =================================================

            final_test_signature = repr(
                final_spec
            )

            # =================================================
            # 4. CHẠY TEST
            # =================================================

            if st.button(
                "Đánh giá mô hình đã chốt trên Test",
                type="primary",
                use_container_width=True,
            ):

                with st.spinner(
                    "Đang fit lại Development 2012–2021 và dự báo Test 2022–2024..."
                ):

                    # =========================================
                    # SINGLE MODEL
                    # =========================================

                    if final_spec["type"] == "single":

                        selected_model = final_spec["model"]

                        if selected_model == "Naive":

                            test_result = run_naive_test(
                                FEATURE_DATA
                            )

                        elif selected_model == "ElasticNet":

                            test_result = run_elasticnet_test(
                                FEATURE_DATA,
                                alpha=final_spec["alpha"],
                                l1_ratio=final_spec["l1_ratio"],
                                feature_cols=final_spec["features"],
                            )

                        elif selected_model == "ARIMAX":

                            test_result = run_arimax_test(
                                FEATURE_DATA,
                                p=final_spec["p"],
                                d=final_spec["d"],
                                q=final_spec["q"],
                                exog_cols=final_spec["exog"],
                            )

                    # =========================================
                    # ENSEMBLE
                    # =========================================

                    else:

                        model_1 = final_spec["model_1"]
                        model_2 = final_spec["model_2"]

                        result_1 = run_saved_model_test(
                            model_1,
                            final_spec["config_1"],
                        )

                        result_2 = run_saved_model_test(
                            model_2,
                            final_spec["config_2"],
                        )

                        test_result = run_ensemble_test(
                            result_1,
                            result_2,
                            final_spec["weight_1"],
                            final_spec["weight_2"],
                            model_1,
                            model_2,
                        )

                    # =========================================
                    # METRICS
                    # =========================================

                    test_metrics = evaluate_test_result(
                        test_result
                    )

                    st.session_state.final_test_result = (
                        test_result
                    )

                    st.session_state.final_test_metrics = (
                        test_metrics
                    )

                    st.session_state.final_test_signature = (
                        final_test_signature
                    )

                    st.session_state.final_test_model = (
                        final_model_name
                    )

            # =================================================
            # 5. HIỂN THỊ KẾT QUẢ TEST
            # =================================================

            if (
                "final_test_result" in st.session_state
                and st.session_state.get(
                    "final_test_signature"
                ) == final_test_signature
            ):

                metrics = (
                    st.session_state.final_test_metrics
                )

                st.markdown(
                    f"### Kết quả Test — {final_model_name}"
                )

                c1, c2, c3, c4, c5 = st.columns(5)

                c1.metric(
                    "R²",
                    f"{metrics['R2']:.4f}",
                )

                c2.metric(
                    "MAE",
                    f"{metrics['MAE']:.4f}",
                )

                c3.metric(
                    "RMSE",
                    f"{metrics['RMSE']:.4f}",
                )

                c4.metric(
                    "MAPE",
                    f"{metrics['MAPE (%)']:.2f}%",
                )

                c5.metric(
                    "DA",
                    f"{metrics['DA (%)']:.2f}%",
                )

                metric_df = pd.DataFrame([
                    {
                        "Model": final_model_name,
                        "R2": metrics["R2"],
                        "MAE": metrics["MAE"],
                        "RMSE": metrics["RMSE"],
                        "MAPE (%)": metrics["MAPE (%)"],
                        "DA (%)": metrics["DA (%)"],
                    }
                ])

                st.dataframe(
                    metric_df.style.format({
                        "R2": "{:.4f}",
                        "MAE": "{:.4f}",
                        "RMSE": "{:.4f}",
                        "MAPE (%)": "{:.2f}",
                        "DA (%)": "{:.2f}",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

                st.warning(
                    "MAPE có thể rất cao khi CPI thực tế gần 0. "
                    "Nên ưu tiên RMSE/MAE và sử dụng DA như chỉ số bổ sung."
                )

            elif "final_test_result" in st.session_state:

                st.info(
                    "Mô hình đã chốt đã thay đổi. "
                    "Bấm 'Đánh giá mô hình đã chốt trên Test' "
                    "để chạy lại kết quả."
                )

    # -------------------- ACTUAL VS PREDICTED --------------------
    with tabs[3]:

        if "final_test_result" not in st.session_state:

            st.info(
                "Chưa có kết quả Test. "
                "Hãy sang tab Test metrics và chạy mô hình đã chốt trước."
            )

        else:

            test_result = st.session_state.final_test_result
            final_model_name = st.session_state.get(
                "final_test_model",
                st.session_state.get("final_model", "Model"),
            )

            pred_df = test_result["predictions"].copy()

            pred_df["MonthYear"] = pd.to_datetime(
                pred_df["MonthYear"],
                errors="coerce",
            )

            chart_df = pred_df[
                ["MonthYear", "Actual", "Prediction"]
            ].copy()

            chart_df = chart_df.rename(
                columns={
                    "Actual": "Thực tế",
                    "Prediction": "Dự báo",
                }
            )

            chart_df = chart_df.set_index("MonthYear")

            st.markdown(
                f"### Actual vs Predicted — {final_model_name}"
            )

            with st.container(border=True):

                st.line_chart(
                    chart_df[
                        ["Thực tế", "Dự báo"]
                    ],
                    height=380,
                    use_container_width=True,
                )

            # =================================================
            # BẢNG CHI TIẾT
            # =================================================

            detail = pred_df[
                ["MonthYear", "Actual", "Prediction"]
            ].copy()

            detail["Sai số"] = (
                pd.to_numeric(
                    detail["Actual"],
                    errors="coerce",
                )
                -
                pd.to_numeric(
                    detail["Prediction"],
                    errors="coerce",
                )
            )

            detail["|Sai số|"] = (
                detail["Sai số"].abs()
            )

            detail = detail.rename(
                columns={
                    "MonthYear": "Tháng",
                    "Actual": "Thực tế",
                    "Prediction": "Dự báo",
                }
            )

            st.dataframe(
                detail,
                use_container_width=True,
                hide_index=True,
                height=420,
            )

            dataframe_download_button(
                detail,
                f"{final_model_name.lower().replace(' ', '_').replace('+', 'plus')}_test_predictions.csv",
                "download_final_test_predictions",
            )

    # -------------------- RESIDUAL --------------------
    with tabs[4]:

        # =====================================================
        # 1. KIỂM TRA ĐÃ CÓ KẾT QUẢ TEST CHƯA
        # =====================================================

        if "final_test_result" not in st.session_state:

            st.info(
                "Chưa có kết quả Test. "
                "Hãy sang tab Test metrics và chạy mô hình đã chốt trước."
            )

        else:

            test_result = st.session_state.final_test_result

            final_model_name = st.session_state.get(
                "final_test_model",
                st.session_state.get(
                    "final_model",
                    "Model",
                ),
            )

            pred_df = test_result["predictions"].copy()

            # =================================================
            # 2. CHUẨN HÓA DỮ LIỆU
            # =================================================

            pred_df["MonthYear"] = pd.to_datetime(
                pred_df["MonthYear"],
                errors="coerce",
            )

            pred_df["Actual"] = pd.to_numeric(
                pred_df["Actual"],
                errors="coerce",
            )

            pred_df["Prediction"] = pd.to_numeric(
                pred_df["Prediction"],
                errors="coerce",
            )

            pred_df = pred_df.dropna(
                subset=[
                    "MonthYear",
                    "Actual",
                    "Prediction",
                ]
            )

            # =================================================
            # 3. TÍNH RESIDUAL
            # =================================================

            pred_df["Residual"] = (
                pred_df["Actual"]
                - pred_df["Prediction"]
            )

            pred_df["|Residual|"] = (
                pred_df["Residual"].abs()
            )

            st.markdown(
                f"### Residual — {final_model_name}"
            )

            st.caption(
                "Residual = Actual − Prediction. "
                "Residual dương nghĩa là mô hình dự báo thấp hơn thực tế; "
                "Residual âm nghĩa là mô hình dự báo cao hơn thực tế."
            )

            # =================================================
            # 4. BIỂU ĐỒ RESIDUAL
            # =================================================

            residual_chart = pred_df[
                ["MonthYear", "Residual"]
            ].copy()

            residual_chart["Zero"] = 0.0

            residual_chart = residual_chart.set_index(
                "MonthYear"
            )

            with st.container(border=True):

                st.line_chart(
                    residual_chart[
                        ["Residual", "Zero"]
                    ],
                    height=330,
                    use_container_width=True,
                )

            # =================================================
            # 5. THỐNG KÊ RESIDUAL
            # =================================================

            residual = pred_df["Residual"]

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Residual mean",
                f"{residual.mean():.4f}",
            )

            c2.metric(
                "Residual std",
                f"{residual.std():.4f}",
            )

            c3.metric(
                "Max |Residual|",
                f"{residual.abs().max():.4f}",
            )

            # =================================================
            # 6. BẢNG CHI TIẾT
            # =================================================

            st.markdown(
                "### Chi tiết sai số"
            )

            residual_detail = pred_df[
                [
                    "MonthYear",
                    "Actual",
                    "Prediction",
                    "Residual",
                    "|Residual|",
                ]
            ].copy()

            residual_detail = residual_detail.rename(
                columns={
                    "MonthYear": "Tháng",
                    "Actual": "Thực tế",
                    "Prediction": "Dự báo",
                    "Residual": "Sai số",
                    "|Residual|": "|Sai số|",
                }
            )

            st.dataframe(
                residual_detail,
                use_container_width=True,
                hide_index=True,
                height=420,
            )

            # =================================================
            # 7. PHÂN PHỐI RESIDUAL
            # =================================================

            st.markdown(
                "### Phân phối Residual"
            )

            if len(residual.dropna()) >= 2:

                hist = pd.cut(
                    residual.dropna(),
                    bins=12,
                ).value_counts().sort_index()

                # Interval không serialize trực tiếp sang Vega
                hist.index = hist.index.astype(str)

                st.bar_chart(
                    hist,
                    height=280,
                )

    # -------------------- REFERENCE MODEL --------------------
    with tabs[5]:

        st.markdown("## Mô hình tham chiếu của đề tài")

        st.caption(
            "Kết quả này được xác định từ quy trình xây dựng mô hình gốc "
            "của đề tài và không thay đổi theo cấu hình do người sử dụng thử nghiệm."
        )

        # =====================================================
        # 1. KIỂM TRA FILE KẾT QUẢ GỐC
        # =====================================================

        if METRICS is None or PREDICTIONS is None:

            st.warning(
                "Chưa tìm thấy model_evaluation_metrics.csv "
                "hoặc model_predictions.csv."
            )

        else:

            # =================================================
            # 2. XÁC ĐỊNH MODEL CÓ TEST RMSE THẤP NHẤT
            # =================================================

            reference_metrics = METRICS.copy()

            reference_metrics["RMSE"] = pd.to_numeric(
                reference_metrics["RMSE"],
                errors="coerce",
            )

            reference_metrics = (
                reference_metrics
                .dropna(subset=["RMSE"])
                .sort_values("RMSE")
                .reset_index(drop=True)
            )

            best_row = reference_metrics.iloc[0]

            reference_model = best_row["Model"]

            # =================================================
            # 3. TỔNG QUAN
            # =================================================

            st.markdown("### Kết quả tốt nhất trên Test 2022–2024")

            c1, c2 = st.columns(2)

            c1.metric(
                "Mô hình",
                reference_model,
            )

            c2.metric(
                "Test RMSE",
                f"{best_row['RMSE']:.4f}",
            )

            st.info(
                "Trong kết quả đánh giá cuối cùng của đề tài, "
                f"{reference_model} có RMSE Test thấp nhất. "
                "Kết quả này được dùng làm mốc tham chiếu cho các cấu hình "
                "do người sử dụng thử nghiệm."
            )

            # =================================================
            # 4. CẤU HÌNH CHUẨN CỦA ĐỀ TÀI
            # =================================================

            st.markdown("### Cấu hình chuẩn")

            st.write(
                "**Ensemble = ElasticNet + ARIMAX**"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.markdown("**ElasticNet**")

                st.write("Alpha: `0.1`")
                st.write("L1 Ratio: `0.9`")

                st.write(
                    f"Số feature: `{len(ELASTICNET_FEATURES)}`"
                )

                with st.expander(
                    "Xem feature ElasticNet"
                ):

                    st.dataframe(
                        pd.DataFrame({
                            "Feature": ELASTICNET_FEATURES
                        }),
                        use_container_width=True,
                        hide_index=True,
                    )

            with c2:

                st.markdown("**ARIMAX**")

                st.write("Order: `ARIMA(1, 0, 2)`")

                st.write(
                    f"Số biến ngoại sinh: "
                    f"`{len(ARIMAX_EXOG_FEATURES)}`"
                )

                with st.expander(
                    "Xem biến ngoại sinh ARIMAX"
                ):

                    st.dataframe(
                        pd.DataFrame({
                            "Biến ngoại sinh":
                                ARIMAX_EXOG_FEATURES
                        }),
                        use_container_width=True,
                        hide_index=True,
                    )

            # =================================================
            # 5. TRỌNG SỐ ENSEMBLE
            # =================================================

            st.markdown("### Trọng số Ensemble")

            c1, c2 = st.columns(2)

            c1.metric(
                "ElasticNet",
                f"{ENSEMBLE_WEIGHT_ELASTIC:.4f}",
            )

            c2.metric(
                "ARIMAX",
                f"{ENSEMBLE_WEIGHT_ARIMAX:.4f}",
            )

            st.code(
                f"ŷ_Ensemble = "
                f"{ENSEMBLE_WEIGHT_ELASTIC:.4f} × ŷ_ElasticNet "
                f"+ "
                f"{ENSEMBLE_WEIGHT_ARIMAX:.4f} × ŷ_ARIMAX"
            )

            # =================================================
            # 6. VALIDATION
            # =================================================

            st.markdown("### Kết quả Validation")

            validation_reference = pd.DataFrame({
                "Model": [
                    "Naive",
                    "ElasticNet",
                    "ARIMAX",
                    "Ensemble",
                ],
                "RMSE": [
                    VALIDATION_RMSE["Naive"],
                    VALIDATION_RMSE["ElasticNet"],
                    VALIDATION_RMSE["ARIMAX"],
                    VALIDATION_RMSE["Ensemble"],
                ],
            }).sort_values("RMSE")

            st.dataframe(
                validation_reference.style.format({
                    "RMSE": "{:.4f}"
                }),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "ElasticNet có RMSE Validation thấp nhất; "
                "Ensemble và ElasticNet có kết quả khá gần nhau "
                "nên tiếp tục được đánh giá trên Test."
            )

            # =================================================
            # 7. TEST METRICS TẤT CẢ MODEL
            # =================================================

            st.markdown("### So sánh trên Test 2022–2024")

            metric_format = {}

            for col in reference_metrics.columns:

                if col in ["R2", "MAE", "RMSE"]:
                    metric_format[col] = "{:.4f}"

                elif col in ["MAPE (%)", "DA (%)"]:
                    metric_format[col] = "{:.2f}"

            st.dataframe(
                reference_metrics.style.format(
                    metric_format
                ),
                use_container_width=True,
                hide_index=True,
            )

            # =================================================
            # 8. METRIC CỦA MODEL TỐT NHẤT
            # =================================================

            st.markdown(
                f"### Chi tiết {reference_model}"
            )

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric(
                "R²",
                f"{best_row['R2']:.4f}",
            )

            c2.metric(
                "MAE",
                f"{best_row['MAE']:.4f}",
            )

            c3.metric(
                "RMSE",
                f"{best_row['RMSE']:.4f}",
            )

            c4.metric(
                "MAPE",
                f"{best_row['MAPE (%)']:.2f}%",
            )

            c5.metric(
                "DA",
                f"{best_row['DA (%)']:.2f}%",
            )

            # =================================================
            # 9. ACTUAL VS PREDICTED
            # =================================================

            pred_map = {
                "Naive": "Naive_Pred",
                "ElasticNet": "ElasticNet_Pred",
                "ARIMAX": "ARIMAX_Pred",
                "Ensemble": "Ensemble_Pred",
            }

            pred_col = pred_map.get(
                reference_model
            )

            if (
                pred_col is not None
                and pred_col in PREDICTIONS.columns
            ):

                reference_pred = (
                    PREDICTIONS[
                        ["MonthYear", "Actual", pred_col]
                    ]
                    .copy()
                )

                reference_pred["MonthYear"] = pd.to_datetime(
                    reference_pred["MonthYear"],
                    errors="coerce",
                )

                st.markdown(
                    "### Actual vs Predicted"
                )

                chart_df = reference_pred.rename(
                    columns={
                        "Actual": "Thực tế",
                        pred_col: "Dự báo",
                    }
                )

                chart_df = chart_df.set_index(
                    "MonthYear"
                )

                with st.container(border=True):

                    st.line_chart(
                        chart_df[
                            ["Thực tế", "Dự báo"]
                        ],
                        height=380,
                        use_container_width=True,
                    )

                # =============================================
                # 10. RESIDUAL
                # =============================================

                st.markdown("### Residual")

                reference_pred["Residual"] = (
                    reference_pred["Actual"]
                    - reference_pred[pred_col]
                )

                residual_chart = (
                    reference_pred[
                        ["MonthYear", "Residual"]
                    ]
                    .copy()
                )

                residual_chart["Zero"] = 0.0

                residual_chart = (
                    residual_chart
                    .set_index("MonthYear")
                )

                with st.container(border=True):

                    st.line_chart(
                        residual_chart,
                        height=300,
                        use_container_width=True,
                    )

                residual = (
                    reference_pred["Residual"]
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Residual mean",
                    f"{residual.mean():.4f}",
                )

                c2.metric(
                    "Residual std",
                    f"{residual.std():.4f}",
                )

                c3.metric(
                    "Max |Residual|",
                    f"{residual.abs().max():.4f}",
                )
# ============================================================
# 18. PAGE — VỀ DỰ ÁN
# ============================================================

elif page == "Về dự án":

    page_header(
        "Về dự án",
        "Tóm tắt bài toán, dữ liệu, phương pháp luận, cấu trúc notebook và các hạn chế khi diễn giải kết quả.",
    )

    section_header("Bài toán nghiên cứu")

    st.html(
        """
<div class="info-card">
    <div class="info-card-title">Dự báo CPI nhóm Giao thông Việt Nam</div>
    <div class="info-card-text">
        Hệ thống sử dụng chuỗi CPI giao thông kết hợp giá xăng dầu trong nước,
        giá dầu Brent/WTI và tỷ giá USD/VND để phân tích biến động và đánh giá
        khả năng dự báo ngoài mẫu trong giai đoạn 2022–2024.
    </div>
</div>
"""
    )

    section_header("Phương pháp luận")

    st.markdown(
        """
- Đồng bộ toàn bộ nguồn dữ liệu về **tần suất tháng**.
- Development: **2012–2021**.
- Expanding-window Validation để chọn cấu hình và trọng số.
- Test: **2022–2024**, không dùng để tune mô hình.
- Mô hình: **Naive, ElasticNet, ARIMAX và Ensemble**.
- Chỉ số: **RMSE, MAE, R², MAPE và Directional Accuracy (DA)**.
"""
    )

    section_header("Hạn chế")

    st.markdown(
        """
- CPI giao thông chịu ảnh hưởng của các cú sốc ngoài mẫu như biến động năng lượng và địa chính trị.
- R² âm trên Test cho thấy mô hình có thể chưa giải thích tốt các biến động bất thường.
- MAPE không ổn định khi CPI thực tế gần 0 hoặc âm.
- Forecast tương lai cần giả định hoặc dự báo trước các biến ngoại sinh.
- Khi dự báo nhiều bước, lag/rolling/change phải được cập nhật tuần tự theo đúng pipeline huấn luyện.
"""
    )