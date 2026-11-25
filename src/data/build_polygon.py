"""
Build a polygon from parcela_vertices.csv and export it to a GeoPackage.

Input:
    data/processed/parcela_vertices.csv
Output:
    data/processed/parcela.gpkg

The polygon is built in EPSG:32719 (WGS84 / UTM 19S), the same CRS used
for the vertices, so areas and distances are in meters.

Validations performed:
    - The ring is closed (first vertex == last vertex). If not, the first
      vertex is appended to close it.
    - The resulting polygon is simple (no self-intersections).
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.validation import explain_validity

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_CSV = PROJECT_ROOT / "data" / "processed" / "parcela_vertices.csv"
OUT_GPKG = PROJECT_ROOT / "data" / "processed" / "parcela.gpkg"

CRS = "EPSG:32719"  # WGS84 / UTM zone 19S
LAYER_NAME = "parcela"


def build_ring(df: pd.DataFrame) -> list[tuple[float, float]]:
    """Return the list of (easting, northing) forming a closed ring."""
    coords = list(zip(df["easting"], df["northing"]))
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    return coords


def main() -> None:
    df = pd.read_csv(SRC_CSV)
    print(f"Read {len(df)} vertices from {SRC_CSV.name}")

    ring = build_ring(df)
    poly = Polygon(ring)

    if not poly.is_valid:
        raise ValueError(f"Invalid polygon: {explain_validity(poly)}")
    print("Polygon is valid and simple.")

    print(f"Area:      {poly.area:,.2f} m²  ({poly.area / 10_000:.4f} ha)")
    print(f"Perimeter: {poly.length:,.2f} m")

    gdf = gpd.GeoDataFrame(
        {"name": ["parcela_ccatcca"], "n_vertices": [len(df)]},
        geometry=[poly],
        crs=CRS,
    )

    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    if OUT_GPKG.exists():
        OUT_GPKG.unlink()  # overwrite cleanly
    gdf.to_file(OUT_GPKG, layer=LAYER_NAME, driver="GPKG")
    print(f"\nWrote -> {OUT_GPKG}  (layer: {LAYER_NAME})")


if __name__ == "__main__":
    main()