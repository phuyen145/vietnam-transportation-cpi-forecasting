import io
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

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
    border-right: none !important;
}

section[data-testid="stSidebar"] > div {
    width: 84px !important;
    min-width: 84px !important;
    max-width: 84px !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 18px 8px 15px 8px !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.sidebar-spacer {
    height: 14px;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button {
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

section[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    color: #a4a5b1 !important;
}

section[data-testid="stSidebar"] button[kind="primary"] {
    background: #353541 !important;
    color: #ff7e67 !important;
}

section[data-testid="stSidebar"] button:hover {
    background: #353541 !important;
    color: #ff7e67 !important;
    transform: translateY(-1px);
}

section[data-testid="stSidebar"] span.material-symbols-rounded {
    font-size: 27px !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] p {
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
   PIPELINE
========================================================= */

.pipeline-grid {
    display: grid;
    grid-template-columns: 1fr 36px 1fr 36px 1fr 36px 1fr;
    align-items: center;
    gap: 8px;
    margin-bottom: 22px;
}

.pipeline-card {
    background: white;
    border: 1px solid #e5ebeb;
    border-radius: 10px;
    padding: 17px 18px;
    min-height: 103px;
    box-shadow: 0 2px 8px rgba(39,48,66,.035);
}

.pipeline-no {
    color: #ff7e67;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .8px;
}

.pipeline-name {
    color: #292934;
    font-size: 14px;
    font-weight: 800;
    margin-top: 6px;
}

.pipeline-desc {
    color: #9297a0;
    font-size: 11px;
    line-height: 1.5;
    margin-top: 5px;
}

.pipeline-arrow {
    color: #adb2b9;
    text-align: center;
    font-size: 22px;
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

.file-chip {
    display: inline-block;
    padding: 5px 9px;
    margin: 3px 3px 3px 0;
    background: #f3f8f8;
    color: #626874;
    border-radius: 16px;
    font-size: 10px;
    font-weight: 700;
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

div[data-baseweb="tab-list"] {
    gap: 6px;
}

button[data-baseweb="tab"] {
    background: white;
    border-radius: 8px;
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
}

[data-testid="stMetricValue"] {
    color: #292934 !important;
    font-size: 25px !important;
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

    .pipeline-grid {
        grid-template-columns: 1fr;
    }

    .pipeline-arrow {
        transform: rotate(90deg);
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


def find_column(df, keywords, exclude=None):
    if df is None or df.empty:
        return None

    exclude = exclude or []

    for col in df.columns:
        n = normalize_text(col)

        if all(normalize_text(k) in n for k in keywords):
            if not any(normalize_text(k) in n for k in exclude):
                return col

    for col in df.columns:
        n = normalize_text(col)

        if any(normalize_text(k) in n for k in keywords):
            if not any(normalize_text(k) in n for k in exclude):
                return col

    return None


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


def format_month(value):
    try:
        return pd.to_datetime(value).strftime("%m/%Y")
    except Exception:
        return "—"


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


# ============================================================
# 8. NAVIGATION — CẤU TRÚC 7 TRANG MỚI
# ============================================================

NAVIGATION = [
    ("Tổng quan", ":material/home:", "Trang chủ / Tổng quan"),
    ("Dữ liệu & Tiền xử lý", ":material/database:", "Dữ liệu thô & Tiền xử lý"),
    ("Phân tích khám phá", ":material/analytics:", "Phân tích khám phá dữ liệu"),
    ("Feature Engineering", ":material/manufacturing:", "Feature Engineering"),
    ("Mô hình & Kết quả", ":material/model_training:", "Mô hình & Kết quả"),
    ("Dự báo tương lai", ":material/trending_up:", "Dự báo tương lai"),
    ("Về dự án", ":material/info:", "Tài liệu / Về dự án"),
]


with st.sidebar:
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    for page_name, icon, tooltip in NAVIGATION:
        active = st.session_state.page == page_name

        if st.button(
            " ",
            key=f"nav_{page_name}",
            icon=icon,
            help=tooltip,
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = page_name
            st.rerun()


page = st.session_state.page

# ============================================================
# 10. PAGE HEADER
# Breadcrumb thay đổi theo trang hiện tại
# ============================================================

PAGE_BREADCRUMBS = {
    "Tổng quan": "HOME",
    "Dữ liệu & Tiền xử lý": "DATA",
    "Phân tích khám phá": "EDA",
    "Feature Engineering": "FEATURES",
    "Mô hình & Kết quả": "MODELING",
    "Dự báo tương lai": "FORECAST",
    "Về dự án": "ABOUT",
}


def page_header(title, description):
    breadcrumb = PAGE_BREADCRUMBS.get(title, title.upper())

    st.html(
        f"""
<div class="page-head">
    <div>
        <div class="breadcrumb">{breadcrumb}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
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


def overview_kpis():
    observation_count = 156
    start = "01/2012"
    end = "12/2024"

    if MODEL_DATA is not None and not MODEL_DATA.empty:
        observation_count = len(MODEL_DATA)

        date_col = get_date_column(MODEL_DATA)
        if date_col:
            dates = pd.to_datetime(MODEL_DATA[date_col], errors="coerce").dropna()
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


def overview_pipeline():
    section_header("Quy trình tổng thể", "raw → interim → processed → model")

    st.html(
        """
<div class="pipeline-grid">
    <div class="pipeline-card">
        <div class="pipeline-no">01 · RAW</div>
        <div class="pipeline-name">Dữ liệu gốc</div>
        <div class="pipeline-desc">CPI, xăng dầu Việt Nam, Brent, WTI và USD/VND.</div>
    </div>

    <div class="pipeline-arrow">→</div>

    <div class="pipeline-card">
        <div class="pipeline-no">02 · INTERIM</div>
        <div class="pipeline-name">Làm sạch</div>
        <div class="pipeline-desc">Chuẩn hóa ngày, giá, tên biến và tổng hợp về tháng.</div>
    </div>

    <div class="pipeline-arrow">→</div>

    <div class="pipeline-card">
        <div class="pipeline-no">03 · PROCESSED</div>
        <div class="pipeline-name">Feature dataset</div>
        <div class="pipeline-desc">Merge dữ liệu và tạo lag, change, MA, dummy, seasonality.</div>
    </div>

    <div class="pipeline-arrow">→</div>

    <div class="pipeline-card">
        <div class="pipeline-no">04 · MODEL</div>
        <div class="pipeline-name">Mô hình</div>
        <div class="pipeline-desc">Validation, Test, Ensemble, metrics và predictions.</div>
    </div>
</div>
"""
    )


def overview_series_chart():
    section_header("Khám phá dữ liệu", "Chọn biến để hiển thị chuỗi thời gian")

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

    section_header(selected["title"], selected["note"])

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

        date_col = get_date_column(MODEL_DATA)

        if date_col is None:
            chart_df = MODEL_DATA[[value_col]].dropna()
        else:
            chart_df = (
                MODEL_DATA[[date_col, value_col]]
                .dropna()
                .copy()
                .set_index(date_col)
            )

        chart_df = chart_df.rename(columns={value_col: selected_name})

        st.line_chart(
            chart_df,
            height=360,
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
    overview_pipeline()
    overview_series_chart()


# ============================================================
# 13. PAGE — DỮ LIỆU & TIỀN XỬ LÝ
# ============================================================

elif page == "Dữ liệu & Tiền xử lý":

    page_header(
        "Dữ liệu & Tiền xử lý",
        "Xem dữ liệu thô, dữ liệu trung gian, dữ liệu đã xử lý và quy trình tương ứng với các notebook 01–06.",
    )

    tab_raw, tab_interim, tab_processed, tab_process = st.tabs([
        "Dữ liệu thô",
        "Interim",
        "Processed",
        "Quy trình xử lý",
    ])

    # -------------------- RAW --------------------
    with tab_raw:
        raw_name = st.selectbox(
            "Chọn nguồn dữ liệu thô",
            list(RAW_FILES.keys()),
            key="raw_selector",
        )

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

                section_header("Preview dữ liệu raw", raw_path.name)

                st.dataframe(
                    raw_df.head(150),
                    use_container_width=True,
                    hide_index=True,
                    height=420,
                )

    # -------------------- INTERIM --------------------
    with tab_interim:
        interim_name = st.selectbox(
            "Chọn dữ liệu interim",
            list(INTERIM_FILES.keys()),
            key="interim_selector",
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
        processed_name = st.selectbox(
            "Chọn dữ liệu processed",
            list(PROCESSED_FILES.keys()),
            key="processed_selector",
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

    # -------------------- PROCESS --------------------
    with tab_process:
        section_header("Pipeline tiền xử lý", "Notebook 01–06")

        process_df = pd.DataFrame(
            [
                {
                    "Bước": no,
                    "Nội dung": title,
                    "Notebook": filename,
                    "Trạng thái": "Có file" if (NOTEBOOK_DIR / filename).exists() else "Chưa thấy",
                }
                for no, title, filename in NOTEBOOKS[:6]
            ]
        )

        st.dataframe(
            process_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            """
**Quy trình chính**

1. **CPI giao thông:** làm sạch và chuẩn hóa chuỗi CPI theo tháng.  
2. **Giá xăng dầu:** làm sạch nhiều nguồn, chuẩn hóa giá và ngày hiệu lực.  
3. **Fuel monthly:** tổng hợp giá xăng dầu theo tháng để đồng bộ tần suất.  
4. **Brent/WTI:** chuẩn hóa dữ liệu dầu thế giới theo tháng.  
5. **USD/VND:** chuẩn hóa tỷ giá theo tháng.  
6. **Dataset integration:** merge các nguồn theo `MonthYear`, kiểm tra missing và phạm vi thời gian.
"""
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

        selected_vars = st.multiselect(
            "Chọn biến",
            available_series,
            default=available_series[:3],
        )

        if selected_vars:
            summary_rows = []

            for col in selected_vars:
                s = pd.to_numeric(analysis_df[col], errors="coerce").dropna()
                summary_rows.append({
                    "Biến": col,
                    "Trung bình": s.mean(),
                    "Độ lệch chuẩn": s.std(),
                    "Nhỏ nhất": s.min(),
                    "Lớn nhất": s.max(),
                })

            st.dataframe(
                pd.DataFrame(summary_rows).round(3),
                use_container_width=True,
                hide_index=True,
            )

            with st.container(border=True):
                if date_col:
                    plot_df = (
                        analysis_df[[date_col] + selected_vars]
                        .dropna(how="all", subset=selected_vars)
                        .set_index(date_col)
                    )
                else:
                    plot_df = analysis_df[selected_vars]

                st.line_chart(
                    plot_df,
                    height=370,
                    use_container_width=True,
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

        selected = st.selectbox(
            "Chọn biến",
            numeric_cols,
            index=numeric_cols.index("CPI") if "CPI" in numeric_cols else 0,
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

    col_left, col_right = st.columns([1, 2])

    with col_left:
        group_choice = st.selectbox(
            "Nhóm feature",
            ["Tất cả"] + list(groups.keys()),
        )

    with col_right:
        search_term = st.text_input(
            "Tìm feature",
            placeholder="Ví dụ: lag, brent, ron95, usd...",
        )

    if group_choice == "Tất cả":
        feature_list = list(feature_df.columns)
    else:
        feature_list = groups[group_choice]

    if search_term:
        token = normalize_text(search_term)
        feature_list = [
            c for c in feature_list
            if token in normalize_text(c)
        ]

    st.dataframe(
        pd.DataFrame({"Feature": feature_list}),
        use_container_width=True,
        hide_index=True,
        height=min(420, 80 + max(1, len(feature_list)) * 34),
    )

    section_header("Feature dataset", f"{len(feature_df):,} dòng · {feature_df.shape[1]} cột")

    preview_cols = st.multiselect(
        "Chọn cột hiển thị",
        list(feature_df.columns),
        default=list(feature_df.columns[:min(12, len(feature_df.columns))]),
    )

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
        "Ensemble",
        "Test metrics",
        "Actual vs Predicted",
        "Residual",
    ])

    # -------------------- CONFIG --------------------
    with tabs[0]:
        model = st.selectbox(
            "Chọn mô hình",
            ["Naive", "ElasticNet", "ARIMAX", "Ensemble"],
            key="model_config_selector",
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
                "ElasticNet sử dụng các feature đã xây dựng trong feature_dataset.csv. "
                "StandardScaler chỉ được fit trên Train của từng fold."
            )

            if FEATURE_DATA is not None:
                feature_cols = [
                    c for c in FEATURE_DATA.columns
                    if c not in ["MonthYear", "CPI"]
                ]

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

            exog_candidates = [
                "RON95_change_lag1",
                "Diesel_change_lag1",
                "Brent_change_lag1",
                "USD_VND_change_lag1",
            ]

            st.multiselect(
                "Biến ngoại sinh đã chọn",
                exog_candidates,
                default=exog_candidates,
                disabled=True,
            )

            st.caption(
                "Exogenous được chọn bằng AIC/BIC; cấu hình (1,0,2) được chốt theo RMSE Expanding-window Validation."
            )

        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("ElasticNet weight", f"{ENSEMBLE_WEIGHT_ELASTIC:.3f}")
            c2.metric("ARIMAX weight", f"{ENSEMBLE_WEIGHT_ARIMAX:.3f}")
            c3.metric("Validation RMSE", f"{VALIDATION_RMSE['Ensemble']:.4f}")

            st.info(
                "Trọng số Ensemble được tính theo nghịch đảo RMSE Validation và cố định trước khi đánh giá Test."
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

        val_df = pd.DataFrame({
            "Model": list(VALIDATION_RMSE.keys()),
            "RMSE": list(VALIDATION_RMSE.values()),
        }).sort_values("RMSE")

        st.dataframe(
            val_df.style.format({"RMSE": "{:.4f}"}),
            use_container_width=True,
            hide_index=True,
        )

        st.bar_chart(
            val_df.set_index("Model")["RMSE"],
            height=300,
        )

    # -------------------- ENSEMBLE --------------------
    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        c1.metric("ElasticNet weight", f"{ENSEMBLE_WEIGHT_ELASTIC:.3f}")
        c2.metric("ARIMAX weight", f"{ENSEMBLE_WEIGHT_ARIMAX:.3f}")
        c3.metric("Validation RMSE", f"{VALIDATION_RMSE['Ensemble']:.4f}")

        st.code(
            "Ensemble = w₁ × ElasticNet + w₂ × ARIMAX"
        )

        st.caption(
            "Trọng số được tính từ Development và không được tính lại bằng Test."
        )

    # -------------------- TEST METRICS --------------------
    with tabs[3]:
        if METRICS is None:
            st.info("Chưa tìm thấy model_evaluation_metrics.csv")
        else:
            metric_view = METRICS.copy()

            if "RMSE" in metric_view.columns:
                metric_view = metric_view.sort_values("RMSE")

            format_map = {}

            for col in metric_view.columns:
                if col in ["R2", "MAE", "RMSE"]:
                    format_map[col] = "{:.4f}"
                elif "%" in str(col) or col in ["MAPE", "DA"]:
                    format_map[col] = "{:.2f}"

            st.dataframe(
                metric_view.style.format(format_map),
                use_container_width=True,
                hide_index=True,
            )

            st.warning(
                "MAPE có thể rất cao khi CPI thực tế gần 0 hoặc âm. "
                "Nên ưu tiên RMSE/MAE và dùng DA như chỉ số bổ sung."
            )

            metric_path = PROCESSED_DIR / PROCESSED_FILES["Model evaluation metrics"]
            download_file_button(
                metric_path,
                "Tải model_evaluation_metrics.csv",
                "download_metrics",
            )

    # -------------------- ACTUAL VS PREDICTED --------------------
    with tabs[4]:
        if PREDICTIONS is None:
            st.error("Chưa tìm thấy model_predictions.csv")
        else:
            model_map = {
                "Naive": "Naive_Pred",
                "ElasticNet": "ElasticNet_Pred",
                "ARIMAX": "ARIMAX_Pred",
                "Ensemble": "Ensemble_Pred",
            }

            available_models = [
                m for m, c in model_map.items()
                if c in PREDICTIONS.columns
            ]

            if not available_models:
                st.warning(
                    "Không tìm thấy các cột Naive_Pred, ElasticNet_Pred, ARIMAX_Pred hoặc Ensemble_Pred."
                )
            else:
                default_model = available_models[0]

                if METRICS is not None and {"Model", "RMSE"}.issubset(METRICS.columns):
                    best_model = METRICS.sort_values("RMSE").iloc[0]["Model"]
                    if best_model in available_models:
                        default_model = best_model

                selected_model = st.selectbox(
                    "Mô hình",
                    available_models,
                    index=available_models.index(default_model),
                    key="pred_model_selector",
                )

                pred_col = model_map[selected_model]
                date_col = get_date_column(PREDICTIONS)

                cols = [c for c in [date_col, "Actual", pred_col] if c is not None]

                chart_df = PREDICTIONS[cols].copy()

                if "Actual" in chart_df.columns:
                    chart_df = chart_df.rename(columns={
                        "Actual": "Thực tế",
                        pred_col: selected_model,
                    })

                    if date_col:
                        chart_df = chart_df.set_index(date_col)

                    with st.container(border=True):
                        st.line_chart(
                            chart_df,
                            height=380,
                            use_container_width=True,
                        )

                    detail = PREDICTIONS[cols].copy()
                    detail["Sai số"] = (
                        pd.to_numeric(detail["Actual"], errors="coerce")
                        - pd.to_numeric(detail[pred_col], errors="coerce")
                    )
                    detail["|Sai số|"] = detail["Sai số"].abs()

                    detail = detail.rename(columns={
                        "Actual": "Thực tế",
                        pred_col: "Dự báo",
                    })

                    st.dataframe(
                        detail,
                        use_container_width=True,
                        hide_index=True,
                        height=420,
                    )

                    dataframe_download_button(
                        detail,
                        f"{selected_model.lower()}_test_predictions.csv",
                        "download_selected_predictions",
                    )

    # -------------------- RESIDUAL --------------------
    with tabs[5]:
        if PREDICTIONS is None:
            st.error("Chưa tìm thấy model_predictions.csv")
        else:
            residual_map = {
                "Naive": "Naive_Pred",
                "ElasticNet": "ElasticNet_Pred",
                "ARIMAX": "ARIMAX_Pred",
                "Ensemble": "Ensemble_Pred",
            }

            residual_models = [
                m for m, c in residual_map.items()
                if c in PREDICTIONS.columns
            ]

            if "Actual" not in PREDICTIONS.columns or not residual_models:
                st.warning("Predictions chưa đủ cột để tính residual.")
            else:
                residual_model = st.selectbox(
                    "Mô hình",
                    residual_models,
                    key="residual_model_selector",
                )

                pred_col = residual_map[residual_model]
                date_col = get_date_column(PREDICTIONS)

                residual = (
                    pd.to_numeric(PREDICTIONS["Actual"], errors="coerce")
                    - pd.to_numeric(PREDICTIONS[pred_col], errors="coerce")
                )

                residual_df = pd.DataFrame({
                    "Residual": residual,
                    "Zero": 0.0,
                })

                if date_col:
                    residual_df.index = PREDICTIONS[date_col]

                with st.container(border=True):
                    st.line_chart(
                        residual_df,
                        height=330,
                        use_container_width=True,
                    )

                c1, c2, c3 = st.columns(3)
                c1.metric("Residual mean", f"{residual.mean():.4f}")
                c2.metric("Residual std", f"{residual.std():.4f}")
                c3.metric("Max |Residual|", f"{residual.abs().max():.4f}")

                hist = pd.cut(
                    residual.dropna(),
                    bins=12,
                ).value_counts().sort_index()

                # Interval index không serialize được sang Vega-Lite (JSON) ->
                # phải convert sang string trước khi vẽ, nếu không st.bar_chart
                # sẽ crash toàn bộ app với SchemaValidationError.
                hist.index = hist.index.astype(str)

                section_header("Phân phối residual", "Histogram dạng bin")
                st.bar_chart(hist, height=260)


# ============================================================
# 17. PAGE — DỰ BÁO TƯƠNG LAI
# Không giả vờ dự báo nếu chưa có model artifact
# ============================================================

elif page == "Dự báo tương lai":

    page_header(
        "Dự báo tương lai",
        "Nhập kịch bản biến động giá xăng, tỷ giá và dầu thế giới để tạo dự báo khi model artifact đã được lưu.",
    )

    st.info(
        "Trang này chỉ chạy dự báo thật khi có file mô hình đã huấn luyện trong thư mục models/. "
        "model_predictions.csv chỉ là kết quả Test 2022–2024, không phải model để dự báo tương lai."
    )

    # Tìm model artifact
    model_candidates = []

    if MODELS_DIR.exists():
        model_candidates += list(MODELS_DIR.glob("*.joblib"))
        model_candidates += list(MODELS_DIR.glob("*.pkl"))

    if not model_candidates:
        section_header("Kịch bản dự báo", "Chưa có model artifact")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.slider(
                "Giá xăng trong nước",
                -20,
                30,
                0,
                1,
                format="%d%%",
                disabled=True,
            )

        with c2:
            st.slider(
                "USD/VND",
                -10,
                15,
                0,
                1,
                format="%d%%",
                disabled=True,
            )

        with c3:
            st.slider(
                "Brent / WTI",
                -30,
                40,
                0,
                1,
                format="%d%%",
                disabled=True,
            )

        st.button(
            "Chạy dự báo kịch bản",
            type="primary",
            use_container_width=True,
            disabled=True,
        )

        st.warning(
            "Hiện project chưa có models/best_model.joblib nên nút dự báo được khóa để tránh tạo kết quả giả."
        )

        st.markdown("**Trong notebook 09_modeling.ipynb, lưu model sau khi train:**")

        st.code(
            """from pathlib import Path
import joblib

Path("../models").mkdir(exist_ok=True)

# Nếu có scaler/feature transform, nên lưu cả pipeline
joblib.dump(best_model, "../models/best_model.joblib")""",
            language="python",
        )

    elif joblib is None:
        st.error(
            "Đã thấy model artifact nhưng môi trường chưa có joblib. "
            "Chạy: pip install joblib"
        )

    elif MODEL_DATA is None:
        st.error("Thiếu model_dataset.csv để lấy vector đầu vào gần nhất.")

    else:
        selected_artifact = st.selectbox(
            "Model artifact",
            model_candidates,
            format_func=lambda p: p.name,
        )

        @st.cache_resource(show_spinner=False)
        def load_model(path_string):
            return joblib.load(path_string)

        try:
            model = load_model(str(selected_artifact))
        except Exception as exc:
            st.error(f"Không load được model: {exc}")
            st.stop()

        model_df = MODEL_DATA.copy()
        date_col = get_date_column(model_df)

        feature_names = None

        if hasattr(model, "feature_names_in_"):
            feature_names = list(model.feature_names_in_)

        if feature_names is None:
            st.warning(
                "Model không có feature_names_in_. "
                "Nên lưu sklearn Pipeline đã fit bằng DataFrame để dashboard biết chính xác feature đầu vào."
            )
            st.stop()

        missing_features = [
            c for c in feature_names
            if c not in model_df.columns
        ]

        if missing_features:
            st.error(
                "model_dataset.csv thiếu feature model yêu cầu: "
                + ", ".join(missing_features[:10])
            )
            st.stop()

        X_base = model_df.iloc[[-1]][feature_names].copy()
        X_scenario = X_base.copy()

        c1, c2, c3 = st.columns(3)

        with c1:
            fuel_pct = st.slider(
                "Giá xăng trong nước",
                -20,
                30,
                0,
                1,
                format="%d%%",
            )

        with c2:
            fx_pct = st.slider(
                "USD/VND",
                -10,
                15,
                0,
                1,
                format="%d%%",
            )

        with c3:
            oil_pct = st.slider(
                "Brent / WTI",
                -30,
                40,
                0,
                1,
                format="%d%%",
            )

        def direct_feature(col, keywords):
            n = normalize_text(col)

            derived = [
                "lag",
                "rolling",
                "moving",
                "_ma",
                "pct",
                "change",
                "diff",
                "growth",
                "mom",
                "yoy",
            ]

            return (
                any(k in n for k in keywords)
                and not any(k in n for k in derived)
            )

        changed = []

        rules = [
            ("Fuel", fuel_pct, ["fuel", "ron", "diesel", "xang"]),
            ("USD/VND", fx_pct, ["usd", "vnd", "exchange"]),
            ("Brent/WTI", oil_pct, ["brent", "wti", "crude"]),
        ]

        for group, pct, keywords in rules:
            for col in feature_names:
                if direct_feature(col, keywords):
                    old_value = pd.to_numeric(
                        pd.Series([X_scenario.iloc[0][col]]),
                        errors="coerce",
                    ).iloc[0]

                    if pd.notna(old_value):
                        new_value = old_value * (1 + pct / 100)

                        X_scenario.loc[
                            X_scenario.index[0],
                            col,
                        ] = new_value

                        changed.append({
                            "Nhóm": group,
                            "Feature": col,
                            "Giá trị gốc": old_value,
                            "Kịch bản": new_value,
                            "Thay đổi (%)": pct,
                        })

        if st.button(
            "Chạy dự báo kịch bản",
            type="primary",
            use_container_width=True,
        ):
            try:
                baseline = np.asarray(
                    model.predict(X_base)
                ).reshape(-1)[0]

                scenario = np.asarray(
                    model.predict(X_scenario)
                ).reshape(-1)[0]

                delta = scenario - baseline

                c1, c2, c3 = st.columns(3)
                c1.metric("Baseline forecast", f"{baseline:.4f}")
                c2.metric("Scenario forecast", f"{scenario:.4f}")
                c3.metric("Tác động", f"{delta:+.4f}")

                if changed:
                    st.dataframe(
                        pd.DataFrame(changed),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.warning(
                        "Không có feature trực tiếp nào khớp với các nhóm kịch bản. "
                        "Cần map tên feature theo model_dataset.csv."
                    )

            except Exception as exc:
                st.error(f"Model predict thất bại: {exc}")

        st.caption(
            "Lưu ý: nếu model sử dụng lag/change/rolling, để dự báo nhiều bước trong tương lai cần xây dựng lại feature pipeline cho từng kỳ."
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

    section_header("Cấu trúc notebook", "01 → 10")

    notebook_table = pd.DataFrame(
        [
            {
                "STT": no,
                "Nội dung": title,
                "Notebook": filename,
                "Trạng thái": "Có" if (NOTEBOOK_DIR / filename).exists() else "Chưa thấy",
            }
            for no, title, filename in NOTEBOOKS
        ]
    )

    st.dataframe(
        notebook_table,
        use_container_width=True,
        hide_index=True,
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

    section_header("Trạng thái dữ liệu", "Kiểm tra nhanh project structure")

    status_rows = []

    for label, filename in INTERIM_FILES.items():
        path = INTERIM_DIR / filename
        status_rows.append({
            "Nhóm": "Interim",
            "File": filename,
            "Mục đích": label,
            "Trạng thái": "Sẵn sàng" if path.exists() else "Thiếu file",
        })

    for label, filename in PROCESSED_FILES.items():
        path = PROCESSED_DIR / filename
        status_rows.append({
            "Nhóm": "Processed",
            "File": filename,
            "Mục đích": label,
            "Trạng thái": "Sẵn sàng" if path.exists() else "Thiếu file",
        })

    st.dataframe(
        pd.DataFrame(status_rows),
        use_container_width=True,
        hide_index=True,
    )