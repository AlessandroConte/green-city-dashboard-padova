# etl/fetch_openmeteo.py
# usage: python etl/fetch_openmeteo.py --start 2025-05-15 --end 2025-08-12
#        python etl/fetch_openmeteo.py --past-days 90

import argparse, os, sys, json, time
from datetime import date
import pandas as pd
import requests

DEFAULTS = dict(
    latitude=45.408,
    longitude=11.8859,
    timezone="Europe/Rome",
    domains="cams_europe",
    hourly="pm10,pm2_5,nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide,european_aqi",
    base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
)

def build_params(args):
    p = {
        "format": "csv",
        "latitude": args.latitude or DEFAULTS["latitude"],
        "longitude": args.longitude or DEFAULTS["longitude"],
        "hourly": args.hourly or DEFAULTS["hourly"],
        "domains": args.domains or DEFAULTS["domains"],
        "timezone": args.timezone or DEFAULTS["timezone"],
    }
    if args.past_days:
        p["past_days"] = args.past_days
    else:
        if args.start: p["start_date"] = args.start
        if args.end:   p["end_date"]   = args.end
    return p

def fetch_csv(params, retries=3, timeout=30):
    for i in range(retries):
        r = requests.get(DEFAULTS["base_url"], params=params, timeout=timeout)
        if r.ok and r.text.strip():
            return r.text
        time.sleep(1.5 * (i+1))
    raise RuntimeError(f"Download failed after {retries} retries")

def validate_df(df: pd.DataFrame):
    required = ["time"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    # check almeno una variabile
    if len([c for c in df.columns if c != "time"]) == 0:
        raise ValueError("No pollutant columns found")

    # esempio check base: range non negativi dove ha senso
    for c in ["pm10","pm2_5","nitrogen_dioxide","ozone","sulphur_dioxide","carbon_monoxide","european_aqi"]:
        if c in df.columns:
            bad = df[c].dropna()
            if (bad < 0).any():
                raise ValueError(f"Negative values in {c}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--latitude", type=float)
    ap.add_argument("--longitude", type=float)
    ap.add_argument("--timezone")
    ap.add_argument("--domains")
    ap.add_argument("--hourly")
    ap.add_argument("--past-days", type=int, dest="past_days")
    ap.add_argument("--start")
    ap.add_argument("--end")
    args = ap.parse_args()

    params = build_params(args)
    csv_text = fetch_csv(params)
    df = pd.read_csv(pd.compat.StringIO(csv_text))
    validate_df(df)

    os.makedirs("data/raw", exist_ok=True)
    # nome file deterministico
    suffix = (
        f"past{params['past_days']}" if "past_days" in params
        else f"{params.get('start_date','')}_{params.get('end_date','')}"
    ).replace("-","")
    fname = f"data/raw/air_quality_padova_{suffix}.csv"
    df.to_csv(fname, index=False)

    # metadati
    meta = {
        "source": "open-meteo:air-quality",
        "url": DEFAULTS["base_url"],
        "params": params,
        "rows": len(df),
        "generated_at": date.today().isoformat(),
        "script": "etl/fetch_openmeteo.py",
        "version": "1.0.0"
    }
    with open(fname.replace(".csv",".meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print("Saved:", fname)

if __name__ == "__main__":
    main()
