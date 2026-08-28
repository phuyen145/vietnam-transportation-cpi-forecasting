import numpy as np
import pandas as pd
import streamlit as st

from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


ELASTICNET_FEATURES = [
    "CPI_lag1",
    "CPI_lag2",
    "RON95_change_lag1",
    "Diesel_change_lag1",
    "Brent_change_lag1",
    "USD_VND_change_lag1",
    "RON95_MA3",
    "Diesel_MA3",
    "Brent_MA3",
    "USDVND_MA3",
    "Brent_WTI_Spread_lag1",
    "Dummy_Tet",
    "Dummy_Covid",
    "Month_sin",
    "Month_cos",
]


def run_elasticnet_validation(
    df,
    alpha=0.1,
    l1_ratio=0.9,
    feature_cols=None,
):
    data = df.copy()

    if feature_cols is None:
        feature_cols = ELASTICNET_FEATURES

    data["MonthYear"] = pd.to_datetime(
        data["MonthYear"]
    ).dt.to_period("M")

    development_df = data[
        (data["MonthYear"] >= pd.Period("2012-01", freq="M"))
        &
        (data["MonthYear"] <= pd.Period("2021-12", freq="M"))
    ].copy()

    development_df = development_df.reset_index(drop=True)

    validation_months = pd.period_range(
        start="2018-01",
        end="2021-12",
        freq="M",
    )

    results = []

    for fold, val_month in enumerate(validation_months, start=1):

        train_fold = development_df[
            development_df["MonthYear"] < val_month
        ]

        val_fold = development_df[
            development_df["MonthYear"] == val_month
        ]

        X_train = train_fold[feature_cols]
        y_train = train_fold["CPI"]

        X_val = val_fold[feature_cols]
        y_val = val_fold["CPI"]

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        model = ElasticNet(
            alpha=alpha,
            l1_ratio=l1_ratio,
            max_iter=10000,
        )

        model.fit(X_train_scaled, y_train)

        pred = model.predict(X_val_scaled)[0]

        results.append({
            "Fold": fold,
            "MonthYear": str(val_month),
            "Actual": y_val.iloc[0],
            "Prediction": pred,
        })

    results_df = pd.DataFrame(results)

    rmse = np.sqrt(
        mean_squared_error(
            results_df["Actual"],
            results_df["Prediction"],
        )
    )

    return {
        "alpha": alpha,
        "l1_ratio": l1_ratio,
        "rmse": rmse,
        "predictions": results_df,
    }

from statsmodels.tsa.statespace.sarimax import SARIMAX


ARIMAX_EXOG_FEATURES = [
    "RON95_change_lag1",
    "Diesel_change_lag1",
    "Brent_change_lag1",
    "USD_VND_change_lag1",
]

@st.cache_data(show_spinner=False)
def run_arimax_validation(
    df,
    p=1,
    d=0,
    q=2,
    exog_cols=None,
):
    data = df.copy()

    if exog_cols is None:
        exog_cols = ARIMAX_EXOG_FEATURES.copy()

    data["MonthYear"] = pd.to_datetime(
        data["MonthYear"]
    ).dt.to_period("M")

    development_df = data[
        (data["MonthYear"] >= pd.Period("2012-01", freq="M"))
        &
        (data["MonthYear"] <= pd.Period("2021-12", freq="M"))
    ].copy()

    development_df = development_df.reset_index(drop=True)

    validation_months = pd.period_range(
        start="2018-01",
        end="2021-12",
        freq="M",
    )

    results = []

    for fold, val_month in enumerate(validation_months, start=1):

        train_fold = development_df[
            development_df["MonthYear"] < val_month
        ]

        val_fold = development_df[
            development_df["MonthYear"] == val_month
        ]

        model = SARIMAX(
            train_fold["CPI"],
            exog=train_fold[exog_cols],
            order=(p, d, q),
            trend="c",
            enforce_stationarity=False,
            enforce_invertibility=False,
        )

        fitted = model.fit(disp=False)

        prediction = fitted.forecast(
            steps=1,
            exog=val_fold[exog_cols],
        ).iloc[0]

        results.append({
            "Fold": fold,
            "MonthYear": str(val_month),
            "Actual": val_fold["CPI"].iloc[0],
            "Prediction": prediction,
        })

    results_df = pd.DataFrame(results)

    rmse = np.sqrt(
        mean_squared_error(
            results_df["Actual"],
            results_df["Prediction"],
        )
    )

    return {
        "p": p,
        "d": d,
        "q": q,
        "exog_cols": exog_cols,
        "rmse": rmse,
        "predictions": results_df,
    }

def run_naive_validation(df):
    data = df.copy()

    data["MonthYear"] = pd.to_datetime(
        data["MonthYear"]
    ).dt.to_period("M")

    # Development: 2012-2021
    development_df = data[
        (data["MonthYear"] >= pd.Period("2012-01", freq="M"))
        &
        (data["MonthYear"] <= pd.Period("2021-12", freq="M"))
    ].copy()

    development_df = development_df.sort_values(
        "MonthYear"
    ).reset_index(drop=True)

    # Validation: 2018-2021
    validation_months = pd.period_range(
        start="2018-01",
        end="2021-12",
        freq="M",
    )

    results = []

    for fold, val_month in enumerate(validation_months, start=1):

        current_row = development_df[
            development_df["MonthYear"] == val_month
        ]

        previous_row = development_df[
            development_df["MonthYear"] == val_month - 1
        ]

        if current_row.empty or previous_row.empty:
            continue

        actual = current_row["CPI"].iloc[0]

        # Naive: CPI tháng trước = dự báo tháng hiện tại
        prediction = previous_row["CPI"].iloc[0]

        results.append({
            "Fold": fold,
            "MonthYear": str(val_month),
            "Actual": actual,
            "Prediction": prediction,
        })

    results_df = pd.DataFrame(results)

    rmse = np.sqrt(
        mean_squared_error(
            results_df["Actual"],
            results_df["Prediction"],
        )
    )

    return {
        "model": "Naive",
        "rmse": rmse,
        "predictions": results_df,
    }

def run_ensemble_validation(
    result_1,
    result_2,
    weight_1,
    weight_2,
    model_1="Model 1",
    model_2="Model 2",
):
    pred_1 = result_1["predictions"].copy()
    pred_2 = result_2["predictions"].copy()

    pred_1 = pred_1[
        ["MonthYear", "Actual", "Prediction"]
    ].copy()

    pred_2 = pred_2[
        ["MonthYear", "Prediction"]
    ].copy()

    pred_1 = pred_1.rename(
        columns={
            "Prediction": f"{model_1}_Pred"
        }
    )

    pred_2 = pred_2.rename(
        columns={
            "Prediction": f"{model_2}_Pred"
        }
    )

    ensemble_df = pred_1.merge(
        pred_2,
        on="MonthYear",
        how="inner",
    )

    ensemble_df["Prediction"] = (
        weight_1 * ensemble_df[f"{model_1}_Pred"]
        + weight_2 * ensemble_df[f"{model_2}_Pred"]
    )

    rmse = np.sqrt(
        mean_squared_error(
            ensemble_df["Actual"],
            ensemble_df["Prediction"],
        )
    )

    return {
        "model_1": model_1,
        "model_2": model_2,
        "weight_1": weight_1,
        "weight_2": weight_2,
        "rmse": rmse,
        "predictions": ensemble_df,
    }