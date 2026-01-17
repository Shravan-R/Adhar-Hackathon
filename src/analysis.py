def get_age_columns(df):
    return [c for c in df.columns if c.startswith("bio_age_")]

def biometric_age_trend(df):
    age_cols = get_age_columns(df)
    trend = (
        df.groupby("date")[age_cols]
        .sum()
        .reset_index()
        .sort_values("date")
    )
    return trend

def enrolment_time_trend(df):
    """
    Aggregate enrolments over time.
    """
    trend = (
        df.groupby("date")
        .size()
        .reset_index(name="enrolments")
        .sort_values("date")
    )
    return trend


def enrolment_by_state(df):
    """
    Aggregate total enrolments by state.
    """
    state_df = (
        df.groupby("state")
        .size()
        .reset_index(name="enrolments")
        .sort_values("enrolments", ascending=False)
    )
    return state_df


def biometric_anomaly_detection(df, threshold=2.5):
    """
    Detect anomalies in total biometric updates using Z-score.
    """
    age_cols = [c for c in df.columns if c.startswith("bio_age_")]

    daily_total = (
        df.groupby("date")[age_cols]
        .sum()
        .sum(axis=1)
        .reset_index(name="total_updates")
    )

    mean = daily_total["total_updates"].mean()
    std = daily_total["total_updates"].std()

    daily_total["z_score"] = (
        (daily_total["total_updates"] - mean) / std
    )

    anomalies = daily_total[
        daily_total["z_score"].abs() > threshold
    ]

    return daily_total, anomalies
