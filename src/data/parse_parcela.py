"""
Parse Parcela.xlsx into a clean CSV with DMS -> decimal -> UTM coordinates.

Input:
    data/raw/Parcela.xlsx (sheet "Hoja1")
Output:
    data/processed/parcela_vertices.csv

Columns produced:
    vertex_id, vertex_num,
    lat_dd, lon_dd, easting, northing, utm_zone, utm_hemisphere, epsg,
    elev_m

Assumption:
    Source coordinates are WGS84 (EPSG:4326).
    Target is WGS84 / UTM zone 19S (EPSG:32719).
"""

import re
from pathlib import Path

import pandas as pd
from pyproj import Transformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_XLSX = PROJECT_ROOT / "data" / "raw" / "Parcela.xlsx"
OUT_DIR = PROJECT_ROOT / "data" / "processed"
OUT_CSV = OUT_DIR / "parcela_vertices.csv"

UTM_EPSG = 32719  # WGS84 / UTM zone 19S
UTM_ZONE = 19
UTM_HEMI = "S"

DMS_PATTERN = re.compile(r"""(\d+)°(\d+)'([\d.]+)"([NSEW])""")
NUM_PATTERN = re.compile(r"[\d.,]+")

def dms_to_dd(dms: str) -> tuple[float, float]:
    """Convert '13°40\\'26.98"S 71°17\\'59.21"W' to (lat_dd, lon_dd)."""
    parts = DMS_PATTERN.findall(dms)
    if len(parts) != 2:
        raise ValueError(f"Unexpected DMS format: {dms!r}")
    values = []
    for deg, minutes, seconds, hemi in parts:
        dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
        if hemi in ("S", "W"):
            dd = -dd
        values.append(dd)
    return values[0], values[1]


def parse_elevation(s: str) -> float:
    """Convert '3,865.05\xa0m' to 3865.05."""
    match = NUM_PATTERN.search(s)
    if not match:
        raise ValueError(f"Unexpected elevation format: {s!r}")
    return float(match.group().replace(",", ""))


def main() -> None:
    df = pd.read_excel(SRC_XLSX, sheet_name="Hoja1")

    # A) Vertex id / number
    df = df.rename(columns={"Vertices/Puntos": "vertex_id"})
    df["vertex_num"] = df["vertex_id"].str.extract(r"(\d+)").astype(int)

    # B) Coordinates: DMS -> decimal -> UTM
    coords = df["Coordenadas Geográficas"].apply(dms_to_dd)
    df["lat_dd"] = [c[0] for c in coords]
    df["lon_dd"] = [c[1] for c in coords]

    transformer = Transformer.from_crs(
        "EPSG:4326", f"EPSG:{UTM_EPSG}", always_xy=True
    )
    easting, northing = transformer.transform(
        df["lon_dd"].to_numpy(), df["lat_dd"].to_numpy()
    )
    df["easting"] = easting
    df["northing"] = northing
    df["utm_zone"] = UTM_ZONE
    df["utm_hemisphere"] = UTM_HEMI
    df["epsg"] = UTM_EPSG

    # C) Elevation
    df["elev_m"] = df["Elevación del suelo"].apply(parse_elevation)

    # Final column order
    out_cols = [
        "vertex_id", "vertex_num",
        "lat_dd", "lon_dd",
        "easting", "northing",
        "utm_zone", "utm_hemisphere", "epsg",
        "elev_m",
    ]
    df = df[out_cols]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)

    print(f"Wrote {len(df)} rows -> {OUT_CSV}")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()