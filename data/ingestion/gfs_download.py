#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

DEFAULT_LEFTLON = -85.0
DEFAULT_RIGHTLON = -83.0
DEFAULT_TOPLAT = 34.2
DEFAULT_BOTTOMLAT = 32.8

# Atlanta, GA approx center: 33.7490 N, -84.3880 W
# Default bbox ~1.5° x 1.4° around Atlanta

VARIABLE_FLAGS = {
    # 2m temperature
    "var_TMP": "on",
    # 2m relative humidity
    "var_RH": "on",
    # 10m winds
    "var_UGRD": "on",
    "var_VGRD": "on",
    # Mean sea-level pressure
    "var_PRMSL": "on",
    # Total cloud cover
    "var_TCDC": "on",
    # Accumulated precip
    "var_APCP": "on",
}

LEVEL_FLAGS = {
    "lev_2_m_above_ground": "on",
    "lev_10_m_above_ground": "on",
    # PRMSL and APCP are surface/accumulated; level selection is implicit for them
}

FILTER_BASE = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"


def build_params(ymd: str, cycle: str, fhr: str, bbox: dict) -> dict:
    params = {
        "file": f"gfs.t{cycle}z.pgrb2.0p25.f{fhr}",
        "dir": f"/gfs.{ymd}/{cycle}/atmos",
        "subregion": "",
        "leftlon": str(bbox["leftlon"]),
        "rightlon": str(bbox["rightlon"]),
        "toplat": str(bbox["toplat"]),
        "bottomlat": str(bbox["bottomlat"]),
        # variables
        **VARIABLE_FLAGS,
        # levels
        **LEVEL_FLAGS,
    }
    return params


def download(session: requests.Session, url: str, params: dict, out_path: Path, timeout=(10, 180)) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with session.get(url, params=params, stream=True, timeout=timeout) as r:
            ct = r.headers.get("Content-Type", "")
            if r.status_code == 200 and ("octet-stream" in ct or ct == "application/grib"):
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                sys.stderr.write(f"Skip/Fail {r.status_code} {r.url} CT={ct}\n")
                return False
    except requests.RequestException as e:
        sys.stderr.write(f"Error {e}\n")
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download filtered GFS (0.25°) for Atlanta (defaults).")
    parser.add_argument("--start-date", type=str, required=False, help="YYYY-MM-DD", default=datetime.utcnow().strftime("%Y-%m-%d"))
    parser.add_argument("--end-date", type=str, required=False, help="YYYY-MM-DD", default=datetime.utcnow().strftime("%Y-%m-%d"))
    parser.add_argument("--cycles", type=str, nargs="*", default=["00", "06", "12", "18"], help="GFS cycles, e.g., 00 06 12 18")
    parser.add_argument("--hours", type=int, nargs="*", default=list(range(0, 73, 3)), help="Forecast hours, e.g., 0 3 6 ...")
    parser.add_argument("--leftlon", type=float, default=DEFAULT_LEFTLON)
    parser.add_argument("--rightlon", type=float, default=DEFAULT_RIGHTLON)
    parser.add_argument("--toplat", type=float, default=DEFAULT_TOPLAT)
    parser.add_argument("--bottomlat", type=float, default=DEFAULT_BOTTOMLAT)
    parser.add_argument("--outdir", type=str, default="/Users/kshitijmishra/weatherApp/data/raw/gfs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        sys.stderr.write("Invalid date format; use YYYY-MM-DD\n")
        return 1

    if end_date < start_date:
        sys.stderr.write("end-date must be >= start-date\n")
        return 1

    bbox = {
        "leftlon": args.leftlon,
        "rightlon": args.rightlon,
        "toplat": args.toplat,
        "bottomlat": args.bottomlat,
    }

    outdir = Path(args.outdir)
    session = requests.Session()
    session.headers.update({"User-Agent": "weatherApp-gfs/0.1"})

    total = 0
    saved = 0

    for i in range((end_date - start_date).days + 1):
        d = start_date + timedelta(days=i)
        ymd = d.strftime("%Y%m%d")
        for cc in args.cycles:
            for h in args.hours:
                fhr = f"{h:03d}"
                params = build_params(ymd, cc, fhr, bbox)
                out_name = f"gfs.{ymd}.{cc}.f{fhr}.atl_bbox.grb2"
                out_path = outdir / ymd / cc / out_name
                total += 1
                if out_path.exists() and out_path.stat().st_size > 0:
                    print(f"Exists {out_path}")
                    continue
                ok = download(session, FILTER_BASE, params, out_path)
                if ok:
                    print(f"Saved {out_path}")
                    saved += 1
    print(f"Done. Attempts={total}, saved={saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
