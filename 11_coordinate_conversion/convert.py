#!/usr/bin/env python3
"""
convert.py — Coordinate Conversion
Pipeliner Asbuilt Cookbook, Chapter 11

Reprojects coordinate columns in a CSV, TXT, or Excel file from one
coordinate system to another using pyproj.

Usage (agent or command line):
    python convert.py \
        --input points.csv \
        --source "Texas South Central NAD27" \
        --target "Texas South Central NAD83 2011" \
        --mode append

Requires: pyproj, pandas, openpyxl
    pip install pyproj pandas openpyxl
"""

import argparse
import os
import sys
import pandas as pd
from pyproj import Transformer, CRS

# ---------------------------------------------------------------------------
# Column name recognition
# Matches the Column Name Reference in REFERENCE.md
# ---------------------------------------------------------------------------

NORTHING_NAMES = {
    "northing", "northings", "north", "n", "y",
    "y coord", "y coords", "y_coord", "y_coords",
}

EASTING_NAMES = {
    "easting", "eastings", "east", "e", "x",
    "x coord", "x coords", "x_coord", "x_coords",
}

LATITUDE_NAMES = {
    "latitude", "lat", "lat.",
    "latitude_dd", "lat_dd", "latitude dd",
}

LONGITUDE_NAMES = {
    "longitude", "lon", "long", "lng", "lon.", "long.",
    "longitude_dd", "lon_dd", "longitude dd",
}


def find_column(df, name_set, label):
    """Return the first column name that matches the recognition set."""
    for col in df.columns:
        if col.strip().lower() in name_set:
            return col
    return None


def detect_coord_columns(df, source_crs):
    """
    Detect which columns hold the horizontal coordinates.
    Returns (horiz1_col, horiz2_col, axis1_meaning, axis2_meaning).
    For geographic CRS: lat col, lon col.
    For projected CRS: northing col, easting col.
    """
    crs = CRS.from_user_input(source_crs)
    if crs.is_geographic:
        c1 = find_column(df, LATITUDE_NAMES, "latitude")
        c2 = find_column(df, LONGITUDE_NAMES, "longitude")
        return c1, c2, "latitude", "longitude"
    else:
        c1 = find_column(df, NORTHING_NAMES, "northing")
        c2 = find_column(df, EASTING_NAMES, "easting")
        return c1, c2, "northing", "easting"


def output_col_names(target_crs, mode, col1, col2):
    """
    For append mode: derive clean output column names from the target CRS
    description so they are human-readable rather than EPSG codes.
    """
    crs = CRS.from_user_input(target_crs)
    name = crs.name  # e.g. "NAD83(2011) / Texas South Central"
    # Shorten to something filename/column-safe
    safe = name.replace("/", "-").replace(" ", "_")
    if crs.is_geographic:
        return f"Latitude_{safe}", f"Longitude_{safe}"
    else:
        return f"Northing_{safe}", f"Easting_{safe}"


def decimal_places(series):
    """Detect the maximum decimal places in a numeric series."""
    max_dp = 0
    for val in series.dropna().astype(str):
        if "." in val:
            max_dp = max(max_dp, len(val.split(".")[1]))
    return max_dp


def read_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".txt"):
        # Try comma first, then tab
        try:
            df = pd.read_csv(path)
            if len(df.columns) == 1:
                df = pd.read_csv(path, sep="\t")
        except Exception:
            df = pd.read_csv(path, sep="\t")
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        sys.exit(f"Unsupported file type: {ext}")
    return df, ext


def write_file(df, path, ext):
    if ext in (".csv", ".txt"):
        df.to_csv(path, index=False)
    elif ext in (".xlsx", ".xls"):
        df.to_excel(path, index=False)


def output_path(input_path, target_crs):
    """Append target zone name to filename, preserving extension."""
    crs = CRS.from_user_input(target_crs)
    zone_label = crs.name.replace("/", "-").replace(" ", "_")
    base, ext = os.path.splitext(input_path)
    return f"{base}_{zone_label}{ext}"


def main():
    parser = argparse.ArgumentParser(description="Reproject coordinate columns.")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--source", required=True, help="Source CRS (name, EPSG, or FIPS description)")
    parser.add_argument("--target", required=True, help="Target CRS (name, EPSG, or FIPS description)")
    parser.add_argument(
        "--mode",
        choices=["replace", "append"],
        default="append",
        help="Replace original coordinate columns or append new ones (default: append)",
    )
    parser.add_argument("--northing-col", help="Override northing/latitude column name")
    parser.add_argument("--easting-col", help="Override easting/longitude column name")
    args = parser.parse_args()

    df, ext = read_file(args.input)

    # Detect or override coordinate columns
    if args.northing_col and args.easting_col:
        col1, col2 = args.northing_col, args.easting_col
        crs = CRS.from_user_input(args.source)
        ax1 = "latitude" if crs.is_geographic else "northing"
        ax2 = "longitude" if crs.is_geographic else "easting"
    else:
        col1, col2, ax1, ax2 = detect_coord_columns(df, args.source)

    if col1 is None or col2 is None:
        sys.exit(
            f"Could not find coordinate columns for source CRS '{args.source}'.\n"
            "Use --northing-col and --easting-col to specify column names manually."
        )

    print(f"Source CRS : {args.source}")
    print(f"Target CRS : {args.target}")
    print(f"Columns    : {col1} ({ax1}), {col2} ({ax2})")
    print(f"Mode       : {args.mode}")

    # Detect input precision
    dp1 = decimal_places(df[col1])
    dp2 = decimal_places(df[col2])

    # Build transformer
    # always_xy=True: first value is easting/longitude, second is northing/latitude
    # We pass (easting, northing) in, get (easting, northing) out — then assign correctly.
    transformer = Transformer.from_crs(args.source, args.target, always_xy=True)

    out_east, out_north = transformer.transform(
        df[col2].values,  # easting / longitude
        df[col1].values,  # northing / latitude
    )

    # Determine output precision
    # When crossing meter/feet boundary, preserve the higher precision side
    src_crs = CRS.from_user_input(args.source)
    tgt_crs = CRS.from_user_input(args.target)
    src_unit = src_crs.axis_info[0].unit_name if not src_crs.is_geographic else "degree"
    tgt_unit = tgt_crs.axis_info[0].unit_name if not tgt_crs.is_geographic else "degree"

    if src_unit != tgt_unit and not src_crs.is_geographic and not tgt_crs.is_geographic:
        # Unit conversion: don't truncate — use max of detected input dp or 4
        out_dp = max(dp1, dp2, 4)
    elif tgt_crs.is_geographic:
        # Lat/long: 8 decimal degrees ~ 1mm precision
        out_dp = max(dp1, dp2, 8)
    else:
        out_dp = max(dp1, dp2)

    out_north_rounded = [round(v, out_dp) for v in out_north]
    out_east_rounded = [round(v, out_dp) for v in out_east]

    if args.mode == "replace":
        df[col1] = out_north_rounded
        df[col2] = out_east_rounded
        out_col1, out_col2 = col1, col2
    else:
        out_col1, out_col2 = output_col_names(args.target, args.mode, col1, col2)
        df[out_col1] = out_north_rounded
        df[out_col2] = out_east_rounded

    print(f"Output columns : {out_col1}, {out_col2}")

    out_file = output_path(args.input, args.target)
    write_file(df, out_file, ext)
    print(f"Written: {out_file}")


if __name__ == "__main__":
    main()
