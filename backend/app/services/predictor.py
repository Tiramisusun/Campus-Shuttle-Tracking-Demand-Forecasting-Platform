import pandas as pd
from prophet import Prophet
from ..models.demand import DemandRecord
from ..extensions import db

def forecast_demand(route: str, periods: int = 12):
    records = (
        db.session.query(DemandRecord)
        .filter_by(route=route)
        .order_by(DemandRecord.timestamp)
        .all()
    )

    if len(records) < 10:
        return {"error": "Not enough historical data"}

    df = pd.DataFrame([
        {"ds": r.timestamp, "y": r.passenger_count} for r in records
    ])

    model = Prophet(interval_width=0.95)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq="H")
    forecast = model.predict(future)

    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
    return result.rename(columns={
        "ds": "timestamp",
        "yhat": "predicted",
        "yhat_lower": "lower_bound",
        "yhat_upper": "upper_bound",
    }).to_dict(orient="records")
