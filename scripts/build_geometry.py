"""Build the non-contiguous area cartogram and state label anchors.

State polygons are projected to EPSG:3577 (Australian Albers Equal-Area Conic).
Each state's true Albers area A_geo is computed via the shoelace formula, and
each state is scaled around its centroid by:
    scale_i = k * sqrt((members_i / A_geo_i) / (members_NSW / A_geo_NSW))
so that the resulting drawn polygon area is strictly proportional to active
patrolling members:
    Area_drawn_i = A_geo_i * scale_i^2  ∝  members_i
"""

import csv
import json
import math
from pathlib import Path

from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# EPSG:3577 is GDA94 / Australian Albers:
# central meridian 132E, standard parallels 18S and 36S, latitude of origin 0.
TO_ALBERS = Transformer.from_crs("EPSG:4326", "EPSG:3577", always_xy=True)
TO_WGS84 = Transformer.from_crs("EPSG:3577", "EPSG:4326", always_xy=True)


def project(lon, lat):
    return TO_ALBERS.transform(lon, lat)


def unproject(x, y):
    return TO_WGS84.transform(x, y)


def outer_rings(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon":
        return [poly[0] for poly in geom["coordinates"]]
    return []


def ring_area_and_centroid(ring):
    pts = [project(lon, lat) for lon, lat in ring]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    area2 = 0.0
    cx = 0.0
    cy = 0.0
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        cross = x0 * y1 - x1 * y0
        area2 += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    area = abs(area2) * 0.5
    if area < 1e-6:
        sx = sum(p[0] for p in pts[:-1]) / max(1, len(pts) - 1)
        sy = sum(p[1] for p in pts[:-1]) / max(1, len(pts) - 1)
        return 1.0, sx, sy
    cx /= 3.0 * area2
    cy /= 3.0 * area2
    return area, cx, cy


def geom_area_and_centroid(geom):
    total_area = 0.0
    wx = 0.0
    wy = 0.0
    for ring in outer_rings(geom):
        a, cx, cy = ring_area_and_centroid(ring)
        total_area += a
        wx += a * cx
        wy += a * cy
    return total_area, wx / total_area, wy / total_area


def map_geom(geom, fn):
    def rec(coords):
        if isinstance(coords[0], (int, float)):
            return list(fn(coords[0], coords[1]))
        return [rec(c) for c in coords]

    return {"type": geom["type"], "coordinates": rec(geom["coordinates"])}


STATE_INFO = {
    "New South Wales": {"members": 20878, "clubs": 129, "hours": 685090, "deaths": 61, "rate": 0.73, "rate_class": "0.69–0.73"},
    "Victoria": {"members": 6630, "clubs": 57, "hours": 216098, "deaths": 26, "rate": 0.38, "rate_class": "0.38–0.48"},
    "Queensland": {"members": 9072, "clubs": 57, "hours": 356662, "deaths": 23, "rate": 0.42, "rate_class": "0.38–0.48"},
    "South Australia": {"members": 2641, "clubs": 23, "hours": 71288, "deaths": 9, "rate": 0.48, "rate_class": "0.38–0.48"},
    "Western Australia": {"members": 5128, "clubs": 31, "hours": 109863, "deaths": 20, "rate": 0.69, "rate_class": "0.69–0.73"},
    "Tasmania": {"members": 792, "clubs": 15, "hours": 21773, "deaths": 10, "rate": 1.74, "rate_class": "1.74"},
    "Northern Territory": {"members": 95, "clubs": 3, "hours": 1759, "deaths": None, "rate": None, "rate_class": "No single-year rate"},
}


def main():
    states = json.loads((DATA / "au-states.geojson").read_text())

    # First pass: compute true Albers Equal-Area geographic area & centroid per state
    geom_stats = {}
    for feature in states["features"]:
        name = feature["properties"]["STATE_NAME"]
        if name not in STATE_INFO:
            continue
        area_m2, cx, cy = geom_area_and_centroid(feature["geometry"])
        geom_stats[name] = (area_m2, cx, cy)

    # Reference density: NSW so NSW is scaled by 0.88 (fits inside its border without overlapping Victoria)
    nsw_area, _, _ = geom_stats["New South Wales"]
    nsw_density = STATE_INFO["New South Wales"]["members"] / nsw_area
    base_k = 0.88

    features = []
    labels = []
    for feature in states["features"]:
        name = feature["properties"]["STATE_NAME"]
        if name not in STATE_INFO:
            continue
        info = STATE_INFO[name]
        area_m2, cx, cy = geom_stats[name]
        density = info["members"] / area_m2
        # True area-cartogram linear scale factor so Drawn_Area ∝ members
        scale = base_k * math.sqrt(density / nsw_density)

        def move(lon, lat, cx=cx, cy=cy, scale=scale):
            x, y = project(lon, lat)
            return unproject(cx + (x - cx) * scale, cy + (y - cy) * scale)

        lon, lat = unproject(cx, cy)
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "state": name,
                    "members": info["members"],
                    "clubs": info["clubs"],
                    "hours": info["hours"],
                    "deaths": info["deaths"],
                    "rate": info["rate"],
                    "rate_class": info["rate_class"],
                },
                "geometry": map_geom(feature["geometry"], move),
            }
        )
        labels.append({"state": name, "lon": round(lon, 4), "lat": round(lat, 4)})

    out = {"type": "FeatureCollection", "features": features}
    (DATA / "cartogram.geojson").write_text(json.dumps(out))
    with (DATA / "labels.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["state", "lon", "lat"])
        writer.writeheader()
        writer.writerows(labels)
    print("cartogram features", len(features))


if __name__ == "__main__":
    main()
