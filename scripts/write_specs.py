"""Generate all Vega-Lite v5 JSON specifications for FIT3179 A2."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "specs"

FONT = "Source Sans 3, sans-serif"
SERIF = "Fraunces, Georgia, serif"

WINE = "#7a1f1c"
WINE_MID = "#c95b52"
WINE_PALE = "#f3cfc9"
WINE_BAND_LOW = "#f7ece9"
WINE_BAND_MID = "#edd5cf"
WINE_BAND_HIGH = "#e2bab2"

SEA = "#1d4e73"
SEA_MID = "#4a7fa6"
SEA_PALE = "#d4e3ee"

OCHRE = "#8a6232"
AMBER = "#b07128"
PLUM = "#6b5b7b"
SLATE_NAVY = "#344e68"
INDIGO_MALE = "#4b4e8f"
AMBER_FEMALE = "#b07128"
TEAL_CAT = "#1f6f78"
TERRA_CAT = "#b84a39"

INK = "#1c2430"
PAPER = "#fffcf8"
SAND = "#e7e0d6"
MUTED = "#786f66"
LIGHT_LINE = "#ded6ca"
LAND = "#f7f4ee"
OCEAN = "#d8e6ee"

RATE_DOMAIN = ["0.38–0.48", "0.69–0.73", "1.74", "No single-year rate"]
RATE_RANGE = [WINE_PALE, WINE_MID, WINE, SAND]

# EPSG:3577 Australian Albers Equal-Area Conic parameters
PROJECTION = {
    "type": "conicEqualArea",
    "rotate": [-132, 0],
    "parallels": [-18, -36],
}

# Custom human silhouette SVG path (normalized to [-1, 1] box) for true Pictorial ISOTYPE
PERSON_PATH = (
    "M 0 -0.92 C 0.20 -0.92 0.34 -0.78 0.34 -0.58 C 0.34 -0.38 0.20 -0.24 0 -0.24 "
    "C -0.20 -0.24 -0.34 -0.38 -0.34 -0.58 C -0.34 -0.78 -0.20 -0.92 0 -0.92 Z "
    "M -0.44 -0.14 C -0.44 -0.18 -0.38 -0.20 -0.30 -0.20 L 0.30 -0.20 "
    "C 0.38 -0.20 0.44 -0.18 0.44 -0.14 L 0.48 0.34 L 0.30 0.34 L 0.26 0.92 "
    "L 0.04 0.92 L 0.04 0.38 L -0.04 0.38 L -0.04 0.92 L -0.26 0.92 "
    "L -0.30 0.34 L -0.48 0.34 Z"
)

DATA_VER = "?v=30"


def csv_data(filename):
    """Return a cache-busted CSV data descriptor that works on both localhost and GitHub Pages."""
    return {
        "url": f"data/{filename}{DATA_VER}",
        "format": {"type": "csv"},
    }


def geojson_data(filename):
    """Return a cache-busted GeoJSON feature data descriptor that works on both localhost and GitHub Pages."""
    return {
        "url": f"data/{filename}{DATA_VER}",
        "format": {"type": "json", "property": "features"},
    }


def config(background=PAPER):
    return {
        "background": background,
        "font": FONT,
        "axis": {
            "labelFont": FONT,
            "titleFont": FONT,
            "labelFontSize": 12.5,
            "titleFontSize": 12.5,
            "titleFontWeight": 600,
            "labelColor": INK,
            "titleColor": INK,
            "domainColor": "#bfb6aa",
            "tickColor": "#bfb6aa",
            "grid": False,
            "labelPadding": 6,
            "titlePadding": 8,
            "labelLimit": 220,
        },
        "legend": {
            "labelFont": FONT,
            "titleFont": FONT,
            "labelFontSize": 12,
            "titleFontSize": 12,
            "titleFontWeight": 600,
            "labelColor": INK,
            "titleColor": INK,
            "symbolStrokeWidth": 0,
            "labelLimit": 240,
            "titleLimit": 280,
        },
        "header": {
            "labelFont": FONT,
            "titleFont": FONT,
            "labelFontSize": 13.5,
            "labelColor": INK,
            "labelFontWeight": 600,
        },
        "view": {"stroke": None},
        "title": {
            "font": FONT,
            "color": INK,
            "fontSize": 13.5,
            "fontWeight": 600,
            "subtitleFont": FONT,
            "subtitleFontSize": 11.5,
            "subtitleColor": MUTED,
            "anchor": "start",
        },
    }


def dump(name, spec):
    path = OUT / name
    path.write_text(json.dumps(spec, indent=2) + "\n")
    print("wrote", name)


def main():
    OUT.mkdir(exist_ok=True)

    # 1. National Bars (Small Multiples Benchmark Comparison)
    dump(
        "national_bars.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "2023/24 rescues and preventative actions against their ten-year averages.",
            "data": csv_data("national_bars.csv"),
            "padding": {"left": 14, "right": 18, "top": 8, "bottom": 8},
            "facet": {
                "row": {
                    "field": "measure",
                    "title": None,
                    "sort": ["Preventative actions", "Rescues"],
                    "header": {"labelOrient": "top", "labelAnchor": "start", "labelPadding": 6},
                }
            },
            "spec": {
                "width": 350,
                "height": 74,
                "encoding": {
                    "y": {
                        "field": "period",
                        "type": "nominal",
                        "sort": ["Ten-year average", "2023/24"],
                        "title": None,
                        "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                    },
                    "x": {
                        "field": "value",
                        "type": "quantitative",
                        "title": None,
                        "scale": {"zero": True, "nice": True},
                        "axis": {
                            "labelExpr": "datum.value >= 1000000 ? format(datum.value/1000000, '.1f') + 'M' : format(datum.value, ',')",
                            "tickCount": 4,
                            "labelFontSize": 11.5,
                        },
                    },
                },
                "layer": [
                    {
                        "mark": {"type": "bar", "height": {"band": 0.64}, "cornerRadiusEnd": 2},
                        "encoding": {
                            "color": {
                                "field": "period",
                                "type": "nominal",
                                "legend": None,
                                "scale": {
                                    "domain": ["Ten-year average", "2023/24"],
                                    "range": ["#9e958b", SEA],
                                },
                            },
                            "tooltip": [
                                {"field": "measure", "type": "nominal", "title": "Activity"},
                                {"field": "period", "type": "nominal", "title": "Period"},
                                {"field": "value", "type": "quantitative", "title": "Count", "format": ","},
                            ],
                        },
                    },
                    {
                        "mark": {
                            "type": "text",
                            "align": "right",
                            "dx": -8,
                            "fontSize": 12.5,
                            "fontWeight": 600,
                            "font": FONT,
                            "color": "#ffffff",
                        },
                        "encoding": {
                            "text": {"field": "value", "type": "quantitative", "format": ","},
                        },
                    },
                ],
            },
            "resolve": {"scale": {"x": "independent"}},
            "config": config(),
        },
    )

    # 2. Interactive 10-Year Brush & Sequential Bar View (Week 10 MCV + Brush)
    dump(
        "decade_brush.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Interactive 10-year overview-and-detail view with interval brush linking preventative actions and coastal drowning deaths.",
            "data": csv_data("decade_trends.csv"),
            "padding": {"left": 10, "right": 12, "top": 8, "bottom": 8},
            "vconcat": [
                {
                    "width": 430,
                    "height": 175,
                    "title": {
                        "text": "Annual coastal drowning deaths (dashed line = 128/yr mean)",
                        "fontSize": 12.5,
                    },
                    "layer": [
                        {
                            "transform": [{"filter": {"param": "year_brush"}}],
                            "mark": {"type": "bar", "width": {"band": 0.58}, "cornerRadiusEnd": 2, "color": WINE},
                            "encoding": {
                                "x": {
                                    "field": "year",
                                    "type": "ordinal",
                                    "title": None,
                                    "axis": {"labelAngle": -25, "labelFontSize": 11.5},
                                },
                                "y": {
                                    "field": "deaths",
                                    "type": "quantitative",
                                    "title": "Deaths",
                                    "scale": {"zero": True, "domain": [0, 175]},
                                    "axis": {"tickCount": 4},
                                },
                                "opacity": {
                                    "condition": {"test": "datum.year == '2023/24' || datum.year == '2015/16'", "value": 1.0},
                                    "value": 0.72,
                                },
                                "tooltip": [
                                    {"field": "year", "type": "nominal", "title": "Reporting year"},
                                    {"field": "deaths", "type": "quantitative", "title": "Coastal drowning deaths"},
                                    {"field": "rate", "type": "quantitative", "title": "Rate per 100,000", "format": ".2f"},
                                    {"field": "preventative", "type": "quantitative", "title": "Preventative actions", "format": ","},
                                    {"field": "rescues", "type": "quantitative", "title": "Rescues", "format": ","},
                                    {"field": "notable_event", "type": "nominal", "title": "Context"},
                                ],
                            },
                        },
                        {
                            "transform": [
                                {"filter": {"param": "year_brush"}},
                                {"filter": "datum.year == '2014/15' || datum.year == '2015/16' || datum.year == '2019/20' || datum.year == '2023/24'"},
                            ],
                            "mark": {
                                "type": "text",
                                "dy": -7,
                                "fontSize": 11.5,
                                "fontWeight": 600,
                                "font": FONT,
                                "color": WINE,
                            },
                            "encoding": {
                                "x": {"field": "year", "type": "ordinal"},
                                "y": {"field": "deaths", "type": "quantitative"},
                                "text": {"field": "deaths", "type": "quantitative"},
                            },
                        },
                        {
                            "mark": {"type": "rule", "color": INK, "strokeWidth": 1.6, "strokeDash": [5, 4]},
                            "encoding": {"y": {"datum": 127.6}},
                        },
                    ],
                },
                {
                    "width": 430,
                    "height": 78,
                    "title": {
                        "text": "Preventative actions (millions) — drag horizontally to filter years",
                        "fontSize": 12,
                        "color": SEA,
                    },
                    "params": [
                        {
                            "name": "year_brush",
                            "select": {"type": "interval", "encodings": ["x"]},
                        }
                    ],
                    "mark": {
                        "type": "area",
                        "color": SEA_PALE,
                        "opacity": 0.7,
                        "line": {"color": SEA, "strokeWidth": 2},
                        "point": {"filled": True, "color": SEA, "size": 40},
                    },
                    "encoding": {
                        "x": {
                            "field": "year",
                            "type": "ordinal",
                            "title": None,
                            "axis": {"labelAngle": -25, "labelFontSize": 11.5},
                        },
                        "y": {
                            "field": "preventative_m",
                            "type": "quantitative",
                            "title": "Actions (M)",
                            "scale": {"zero": True, "domain": [0, 2.8]},
                            "axis": {"tickCount": 3, "format": ".1f"},
                        },
                        "tooltip": [
                            {"field": "year", "type": "nominal", "title": "Season"},
                            {"field": "preventative", "type": "quantitative", "title": "Preventative actions", "format": ","},
                            {"field": "rescues", "type": "quantitative", "title": "Rescues", "format": ","},
                        ],
                    },
                },
            ],
            "config": config(),
        },
    )

    # 3. Map 1: Interactive Classified Choropleth Map (100% Normalized Metrics Only)
    dump(
        "choropleth.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Classified choropleth of the 2023/24 coastal drowning rate with interactive normalized metric selector.",
            "width": 920,
            "height": 450,
            "padding": {"left": 10, "right": 10, "top": 10, "bottom": 10},
            "projection": PROJECTION,
            "params": [
                {
                    "name": "label_mode",
                    "value": "rate",
                    "bind": {
                        "input": "select",
                        "options": ["rate", "rate_10yr", "beyond_pct", "clubs_per_1000km"],
                        "labels": [
                            "2023/24 rate (per 100k)",
                            "10-year avg rate (per 100k)",
                            "Share >1 km from patrol (%)",
                            "SLS clubs per 1,000 km coast",
                        ],
                        "name": "Inspect normalized state metric: ",
                    },
                }
            ],
            "layer": [
                {
                    "data": geojson_data("au-states.geojson"),
                    "transform": [
                        {
                            "lookup": "properties.STATE_NAME",
                            "from": {
                                "data": csv_data("states.csv"),
                                "key": "state",
                                "fields": [
                                    "code",
                                    "deaths",
                                    "rate",
                                    "rate_10yr",
                                    "rate_class",
                                    "beyond_pct",
                                    "clubs",
                                    "clubs_per_1000km",
                                    "pop_m",
                                ],
                            },
                        }
                    ],
                    "mark": {"type": "geoshape", "stroke": "#ffffff", "strokeWidth": 1.3},
                    "encoding": {
                        "color": {
                            "field": "rate_class",
                            "type": "nominal",
                            "scale": {"domain": RATE_DOMAIN, "range": RATE_RANGE},
                            "legend": {
                                "title": "2023/24 deaths per 100,000 people (normalized rate)",
                                "orient": "bottom",
                                "columns": 4,
                                "direction": "horizontal",
                                "labelLimit": 200,
                            },
                        },
                        "tooltip": [
                            {"field": "properties.STATE_NAME", "title": "State / Territory", "type": "nominal"},
                            {"field": "rate", "title": "2023/24 rate (per 100k)", "type": "quantitative", "format": ".2f"},
                            {"field": "rate_10yr", "title": "10-year avg rate (per 100k)", "type": "quantitative", "format": ".2f"},
                            {"field": "beyond_pct", "title": "Deaths >1 km from service (%)", "type": "quantitative"},
                            {"field": "clubs_per_1000km", "title": "Clubs per 1,000 km coast", "type": "quantitative", "format": ".1f"},
                            {"field": "pop_m", "title": "ABS population (millions)", "type": "quantitative", "format": ".2f"},
                        ],
                    },
                },
                {
                    "data": csv_data("states.csv"),
                    "transform": [
                        {
                            "lookup": "state",
                            "from": {
                                "data": csv_data("labels.csv"),
                                "key": "state",
                                "fields": ["lon", "lat"],
                            },
                        },
                        {
                            "calculate": (
                                "label_mode == 'rate_10yr' ? datum.code + '  ' + datum.rate_10yr : "
                                "label_mode == 'beyond_pct' ? datum.code + '  ' + datum.beyond_pct + '%' : "
                                "label_mode == 'clubs_per_1000km' ? datum.code + '  ' + datum.clubs_per_1000km + '/1k km' : "
                                "(datum.deaths === '' || datum.deaths == null ? datum.code + ' (no 1-yr)' : datum.code + '  ' + datum.rate)"
                            ),
                            "as": "label",
                        },
                    ],
                    "mark": {
                        "type": "text",
                        "font": FONT,
                        "fontSize": 13,
                        "fontWeight": 600,
                        "color": INK,
                        "dy": 2,
                    },
                    "encoding": {
                        "longitude": {"field": "lon", "type": "quantitative"},
                        "latitude": {"field": "lat", "type": "quantitative"},
                        "text": {"field": "label", "type": "nominal"},
                    },
                },
                {
                    "data": {
                        "values": [
                            {
                                "lon": 146.4,
                                "lat": -44.2,
                                "note": "Tasmania: 1.74 per 100k (3.1× national rate)",
                            }
                        ]
                    },
                    "mark": {
                        "type": "text",
                        "align": "center",
                        "dy": 8,
                        "font": FONT,
                        "fontSize": 12,
                        "fontWeight": 600,
                        "color": WINE,
                    },
                    "encoding": {
                        "longitude": {"field": "lon", "type": "quantitative"},
                        "latitude": {"field": "lat", "type": "quantitative"},
                        "text": {"field": "note", "type": "nominal"},
                    },
                },
            ],
            "config": config(OCEAN),
        },
    )

    # 4. True Stephen Few Bullet Chart (Selective Annotation on Key Extremes Only)
    bullet_state_order = [
        "Tasmania",
        "New South Wales",
        "Western Australia",
        "South Australia",
        "Queensland",
        "Victoria",
    ]
    dump(
        "bullets.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "True bullet chart comparing state coastal drowning rates against qualitative risk tiers, 10-year average ticks, and the 0.56 national rate.",
            "width": 360,
            "height": 270,
            "padding": {"left": 12, "right": 18, "top": 10, "bottom": 10},
            "data": csv_data("bullets.csv"),
            "encoding": {
                "y": {
                    "field": "state",
                    "type": "nominal",
                    "sort": bullet_state_order,
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                }
            },
            "layer": [
                {
                    "mark": {"type": "bar", "color": WINE_BAND_HIGH, "height": {"band": 0.78}},
                    "encoding": {
                        "x": {
                            "field": "band_high",
                            "type": "quantitative",
                            "title": "Deaths per 100,000 people (<0.45 low · 0.45–0.75 mod · >0.75 high)",
                            "scale": {"zero": True, "domain": [0, 2.0]},
                            "axis": {"values": [0, 0.4, 0.56, 0.8, 1.2, 1.6, 2.0], "format": ".2f"},
                        }
                    },
                },
                {
                    "mark": {"type": "bar", "color": WINE_BAND_MID, "height": {"band": 0.78}},
                    "encoding": {"x": {"field": "band_mid", "type": "quantitative"}},
                },
                {
                    "mark": {"type": "bar", "color": WINE_BAND_LOW, "height": {"band": 0.78}},
                    "encoding": {"x": {"field": "band_low", "type": "quantitative"}},
                },
                {
                    "mark": {"type": "bar", "color": WINE, "height": {"band": 0.42}, "cornerRadiusEnd": 2},
                    "encoding": {
                        "x": {"field": "rate", "type": "quantitative"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "rate", "type": "quantitative", "title": "2023/24 rate (per 100k)", "format": ".2f"},
                            {"field": "rate_22_23", "type": "quantitative", "title": "2022/23 rate (per 100k)", "format": ".2f"},
                            {"field": "rate_10yr", "type": "quantitative", "title": "10-year avg rate", "format": ".2f"},
                            {"field": "deaths", "type": "quantitative", "title": "2023/24 deaths"},
                            {"field": "national", "type": "quantitative", "title": "National rate", "format": ".2f"},
                        ],
                    },
                },
                {
                    "mark": {"type": "tick", "color": INK, "thickness": 2.2, "size": 22},
                    "encoding": {
                        "x": {"field": "rate_10yr", "type": "quantitative"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "rate_10yr", "type": "quantitative", "title": "10-year average rate (tick mark)", "format": ".2f"},
                        ],
                    },
                },
                {
                    "mark": {"type": "rule", "color": INK, "strokeWidth": 1.8, "strokeDash": [5, 3]},
                    "encoding": {"x": {"datum": 0.56}},
                },
                {
                    "transform": [
                        {"filter": "datum.code == 'Tas' || datum.code == 'NSW' || datum.code == 'WA' || datum.code == 'Vic'"},
                    ],
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 7,
                        "font": FONT,
                        "fontSize": 12,
                        "fontWeight": 600,
                        "color": INK,
                    },
                    "encoding": {
                        "x": {"field": "rate", "type": "quantitative"},
                        "text": {"field": "rate", "type": "quantitative", "format": ".2f"},
                    },
                },
                {
                    "data": {"values": [{"note": "National: 0.56 │ Ticks = 10-yr avg"}]},
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 8,
                        "dy": 212,
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "color": INK,
                    },
                    "encoding": {
                        "x": {"datum": 0.56},
                        "y": {"value": 0},
                        "text": {"field": "note", "type": "nominal"},
                    },
                },
            ],
            "config": config(),
        },
    )

    # 5. Slope States (Interactive State Highlight + Left & Right Labels)
    dump(
        "slope_states.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Interactive slope chart of state coastal drowning rates from 2022/23 to 2023/24.",
            "width": 440,
            "height": 340,
            "padding": {"left": 14, "right": 24, "top": 10, "bottom": 10},
            "data": csv_data("slope_states.csv"),
            "transform": [
                {
                    "calculate": "datum.code + '  ' + format(datum.rate, '.2f') + ' (n=' + datum.deaths + ')'",
                    "as": "calc_label",
                }
            ],
            "layer": [
                {
                    "params": [
                        {
                            "name": "state_hover",
                            "select": {"type": "point", "fields": ["state"], "on": "mouseover", "clear": "mouseout"},
                        }
                    ],
                    "mark": {"type": "line", "strokeWidth": 2.8},
                    "encoding": {
                        "x": {
                            "field": "year",
                            "type": "ordinal",
                            "sort": ["2022/23", "2023/24"],
                            "title": None,
                            "scale": {"padding": 0.35},
                            "axis": {"labelFontSize": 13, "labelFontWeight": 600, "labelAngle": 0},
                        },
                        "y": {
                            "field": "rate",
                            "type": "quantitative",
                            "title": "Deaths per 100,000 people",
                            "scale": {"zero": True, "domain": [0, 1.9]},
                            "axis": {"tickCount": 5},
                        },
                        "detail": {"field": "state", "type": "nominal"},
                        "color": {
                            "condition": [
                                {"param": "state_hover", "empty": False, "value": WINE},
                                {"test": "datum.code == 'Tas' || datum.code == 'NSW'", "value": WINE},
                            ],
                            "value": "#b8a6a1",
                        },
                        "opacity": {
                            "condition": {"param": "state_hover", "value": 1},
                            "value": 0.9,
                        },
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "year", "type": "nominal", "title": "Year"},
                            {"field": "rate", "type": "quantitative", "title": "Rate per 100k", "format": ".2f"},
                            {"field": "deaths", "type": "quantitative", "title": "Coastal deaths"},
                        ],
                    },
                },
                {
                    "mark": {"type": "circle", "size": 80, "opacity": 1},
                    "encoding": {
                        "x": {"field": "year", "type": "ordinal", "sort": ["2022/23", "2023/24"]},
                        "y": {"field": "rate", "type": "quantitative"},
                        "color": {
                            "condition": {"test": "datum.code == 'Tas' || datum.code == 'NSW'", "value": WINE},
                            "value": "#9e8f89",
                        },
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "year", "type": "nominal", "title": "Year"},
                            {"field": "rate", "type": "quantitative", "title": "Rate per 100k", "format": ".2f"},
                            {"field": "deaths", "type": "quantitative", "title": "Coastal deaths"},
                        ],
                    },
                },
                *[
                    {
                        "transform": [{"filter": f"datum.code == '{code}' && datum.year == '2023/24'"}],
                        "mark": {
                            "type": "text",
                            "align": "left",
                            "dx": 10,
                            "dy": dy,
                            "font": FONT,
                            "fontSize": 11.5,
                            "fontWeight": 600,
                            "color": WINE if code in ("Tas", "NSW") else INK,
                        },
                        "encoding": {
                            "x": {"field": "year", "type": "ordinal", "sort": ["2022/23", "2023/24"]},
                            "y": {"field": "rate", "type": "quantitative"},
                            "text": {"field": "calc_label", "type": "nominal"},
                        },
                    }
                    for code, dy in [
                        ("Tas", 0),
                        ("NSW", -8),
                        ("WA", 8),
                        ("SA", -8),
                        ("Qld", 3),
                        ("Vic", 14),
                    ]
                ],
                *[
                    {
                        "transform": [{"filter": f"datum.code == '{code}' && datum.year == '2022/23'"}],
                        "mark": {
                            "type": "text",
                            "align": "right",
                            "dx": -10,
                            "dy": dy,
                            "font": FONT,
                            "fontSize": 11.5,
                            "fontWeight": 600 if code in ("Tas", "NSW") else 400,
                            "color": WINE if code in ("Tas", "NSW") else MUTED,
                        },
                        "encoding": {
                            "x": {"field": "year", "type": "ordinal", "sort": ["2022/23", "2023/24"]},
                            "y": {"field": "rate", "type": "quantitative"},
                            "text": {"field": "calc_label", "type": "nominal"},
                        },
                    }
                    for code, dy in [
                        ("WA", -6),
                        ("NSW", -10),
                        ("Tas", 1),
                        ("Qld", 13),
                        ("SA", -4),
                        ("Vic", 10),
                    ]
                ],
            ],
            "config": config(),
        },
    )

    # 6. Map 2: Graduated Symbol Map (Classified Circle Sizes, Zero Overlap, No Colour Luminance)
    dump(
        "symbol_map.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Graduated symbol map with 4 classified volunteer patrol hour tiers. Single flat colour, zero circle overlap.",
            "width": 470,
            "height": 420,
            "padding": {"left": 10, "right": 10, "top": 10, "bottom": 10},
            "projection": PROJECTION,
            "layer": [
                {
                    "data": geojson_data("au-states.geojson"),
                    "mark": {"type": "geoshape", "fill": LAND, "stroke": "#ffffff", "strokeWidth": 1.2},
                },
                {
                    "data": csv_data("states.csv"),
                    "transform": [
                        {
                            "lookup": "state",
                            "from": {
                                "data": csv_data("labels.csv"),
                                "key": "state",
                                "fields": ["lon", "lat"],
                            },
                        },
                        {
                            "calculate": (
                                "datum.hours < 50000 ? '< 50,000 hrs' : "
                                "datum.hours < 150000 ? '50,000–150,000 hrs' : "
                                "datum.hours < 400000 ? '150,000–400,000 hrs' : '> 400,000 hrs'"
                            ),
                            "as": "hours_class",
                        },
                    ],
                    "mark": {
                        "type": "circle",
                        "opacity": 0.88,
                        "color": SEA,
                        "stroke": "#ffffff",
                        "strokeWidth": 1.6,
                    },
                    "encoding": {
                        "longitude": {"field": "lon", "type": "quantitative"},
                        "latitude": {"field": "lat", "type": "quantitative"},
                        "size": {
                            "field": "hours_class",
                            "type": "ordinal",
                            "scale": {
                                "domain": [
                                    "< 50,000 hrs",
                                    "50,000–150,000 hrs",
                                    "150,000–400,000 hrs",
                                    "> 400,000 hrs",
                                ],
                                "range": [95, 240, 480, 880],
                            },
                            "title": "Volunteer patrol hours (4 graduated classes)",
                            "legend": {
                                "orient": "bottom",
                                "columns": 2,
                                "direction": "horizontal",
                                "labelLimit": 190,
                            },
                        },
                        "order": {"field": "hours", "type": "quantitative", "sort": "descending"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "hours_class", "type": "nominal", "title": "Graduated class"},
                            {"field": "hours", "type": "quantitative", "title": "Volunteer patrol hours", "format": ","},
                            {"field": "members", "type": "quantitative", "title": "Patrolling members", "format": ","},
                            {"field": "clubs", "type": "quantitative", "title": "SLS clubs"},
                        ],
                    },
                },
                {
                    "data": csv_data("states.csv"),
                    "transform": [
                        {
                            "lookup": "state",
                            "from": {
                                "data": csv_data("labels.csv"),
                                "key": "state",
                                "fields": ["lon", "lat"],
                            },
                        },
                        {
                            "calculate": "datum.code + ' · ' + format(datum.hours, ',')",
                            "as": "state_hrs",
                        },
                    ],
                    "mark": {
                        "type": "text",
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "dy": -19,
                        "color": INK,
                    },
                    "encoding": {
                        "longitude": {"field": "lon", "type": "quantitative"},
                        "latitude": {"field": "lat", "type": "quantitative"},
                        "text": {"field": "state_hrs", "type": "nominal"},
                    },
                },
            ],
            "config": config(OCEAN),
        },
    )

    # 7. Map 3: Non-Contiguous Area Cartogram (Area = Patrolling Members, Colour = Drowning Rate)
    dump(
        "cartogram.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Non-contiguous area cartogram. State polygon area is scaled to active patrolling members; colour shows the drowning rate class.",
            "width": 470,
            "height": 420,
            "padding": {"left": 10, "right": 10, "top": 10, "bottom": 10},
            "projection": PROJECTION,
            "layer": [
                {
                    "data": geojson_data("au-states.geojson"),
                    "mark": {
                        "type": "geoshape",
                        "fill": "#e6f0f5",
                        "stroke": "#b2c5d1",
                        "strokeWidth": 1,
                        "strokeDash": [3, 3],
                    },
                },
                {
                    "data": geojson_data("cartogram.geojson"),
                    "mark": {"type": "geoshape", "stroke": "#ffffff", "strokeWidth": 1.3},
                    "encoding": {
                        "color": {
                            "field": "properties.rate_class",
                            "type": "nominal",
                            "scale": {"domain": RATE_DOMAIN, "range": RATE_RANGE},
                            "legend": {
                                "title": "Deaths per 100,000 people",
                                "orient": "bottom",
                                "columns": 2,
                                "direction": "horizontal",
                                "labelLimit": 180,
                            },
                        },
                        "tooltip": [
                            {"field": "properties.state", "type": "nominal", "title": "State"},
                            {"field": "properties.members", "type": "quantitative", "title": "Active patrolling members", "format": ","},
                            {"field": "properties.clubs", "type": "quantitative", "title": "Surf Life Saving clubs"},
                            {"field": "properties.hours", "type": "quantitative", "title": "Volunteer patrol hours", "format": ","},
                            {"field": "properties.rate_class", "type": "nominal", "title": "Drowning rate class"},
                        ],
                    },
                },
                {
                    "data": csv_data("states.csv"),
                    "transform": [
                        {
                            "lookup": "state",
                            "from": {
                                "data": csv_data("labels.csv"),
                                "key": "state",
                                "fields": ["lon", "lat"],
                            },
                        },
                        {
                            "calculate": "datum.code + ' (' + format(datum.members, ',') + ')'",
                            "as": "member_label",
                        },
                    ],
                    "mark": {"type": "text", "font": FONT, "fontSize": 11.5, "fontWeight": 600, "color": INK},
                    "encoding": {
                        "longitude": {"field": "lon", "type": "quantitative"},
                        "latitude": {"field": "lat", "type": "quantitative"},
                        "text": {"field": "member_label", "type": "nominal"},
                    },
                },
            ],
            "config": config(OCEAN),
        },
    )

    # 8. True 10-Year State Coastal Drowning Rate Heatmap (Single Sequential Scale, Selective Un-Cluttered Annotations)
    heatmap_states = [
        "Tasmania",
        "Western Australia",
        "New South Wales",
        "Queensland",
        "South Australia",
        "Victoria",
    ]
    dump(
        "heatmap.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Ten-year heatmap of coastal drowning rates per 100,000 people across Australian states (2014/15–2023/24) with selective milestone annotations.",
            "width": 780,
            "height": 290,
            "padding": {"left": 14, "right": 16, "top": 8, "bottom": 8},
            "data": csv_data("heatmap.csv"),
            "encoding": {
                "x": {
                    "field": "fy",
                    "type": "ordinal",
                    "title": "Reporting season (1 July – 30 June)",
                    "axis": {
                        "orient": "bottom",
                        "labelAngle": 0,
                        "labelFontSize": 12,
                        "domain": False,
                        "ticks": False,
                    },
                },
                "y": {
                    "field": "state",
                    "type": "nominal",
                    "sort": heatmap_states,
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                },
            },
            "layer": [
                {
                    "mark": {"type": "rect", "stroke": PAPER, "strokeWidth": 2},
                    "encoding": {
                        "color": {
                            "field": "rate",
                            "type": "quantitative",
                            "scale": {
                                "type": "linear",
                                "domain": [0.2, 0.6, 1.1, 1.75],
                                "range": ["#f6ede8", "#df9a8c", "#b3443c", WINE],
                            },
                            "legend": {
                                "title": "Deaths per 100,000 people",
                                "orient": "bottom",
                                "direction": "horizontal",
                                "gradientLength": 200,
                                "format": ".2f",
                            },
                        },
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "fy", "type": "nominal", "title": "Financial year"},
                            {"field": "rate", "type": "quantitative", "title": "Rate per 100,000", "format": ".2f"},
                            {"field": "deaths", "type": "quantitative", "title": "Coastal drowning deaths"},
                        ],
                    },
                },
                {
                    "transform": [{"filter": "datum.note != '' && datum.note != null"}],
                    "mark": {"type": "text", "font": FONT, "fontSize": 11.5, "fontWeight": 600},
                    "encoding": {
                        "text": {"field": "note", "type": "nominal"},
                        "color": {
                            "condition": {"test": "datum.rate >= 0.70", "value": "#ffffff"},
                            "value": INK,
                        },
                    },
                },
            ],
            "config": config(),
        },
    )

    # 9. Refined Lollipop Chart: Rescues per 10,000 Volunteer Patrol Hours (Length Channel Only, Selective Annotations)
    lollipop_order = [
        "Queensland",
        "New South Wales",
        "Western Australia",
        "Victoria",
        "Tasmania",
        "South Australia",
    ]
    dump(
        "hours_ratio.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Lollipop chart of rescues per 10,000 volunteer patrol hours encoded strictly by length.",
            "width": 360,
            "height": 250,
            "padding": {"left": 12, "right": 20, "top": 10, "bottom": 10},
            "data": csv_data("hours_ratio.csv"),
            "encoding": {
                "y": {
                    "field": "state",
                    "type": "nominal",
                    "sort": lollipop_order,
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                }
            },
            "layer": [
                {
                    "mark": {"type": "rule", "color": SEA, "strokeWidth": 3},
                    "encoding": {
                        "x": {
                            "field": "per_10k",
                            "type": "quantitative",
                            "title": "Rescues per 10,000 volunteer patrol hours",
                            "scale": {"zero": True, "domain": [0, 88]},
                            "axis": {"tickCount": 5},
                        },
                        "x2": {"datum": 0},
                    },
                },
                {
                    "mark": {"type": "circle", "color": SEA, "size": 150, "opacity": 1},
                    "encoding": {
                        "x": {"field": "per_10k", "type": "quantitative"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "per_10k", "type": "quantitative", "title": "Rescues per 10k hours", "format": ".1f"},
                            {"field": "rescues", "type": "quantitative", "title": "Total rescues", "format": ","},
                            {"field": "hours", "type": "quantitative", "title": "Volunteer patrol hours", "format": ","},
                            {"field": "clubs", "type": "quantitative", "title": "SLS clubs"},
                        ],
                    },
                },
                {
                    "mark": {"type": "rule", "color": OCHRE, "strokeWidth": 1.6, "strokeDash": [5, 3]},
                    "encoding": {"x": {"datum": 60.6}},
                },
                {
                    "data": {"values": [{"label": "National avg: 60.6"}]},
                    "mark": {
                        "type": "text",
                        "align": "right",
                        "dx": -6,
                        "dy": 102,
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "color": OCHRE,
                    },
                    "encoding": {
                        "x": {"datum": 60.6},
                        "y": {"value": 0},
                        "text": {"field": "label", "type": "nominal"},
                    },
                },
                {
                    "transform": [
                        {"filter": "datum.code == 'Qld' || datum.code == 'NSW' || datum.code == 'SA'"},
                    ],
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 10,
                        "font": FONT,
                        "fontSize": 12,
                        "fontWeight": 600,
                        "color": INK,
                    },
                    "encoding": {
                        "x": {"field": "per_10k", "type": "quantitative"},
                        "text": {"field": "per_10k", "type": "quantitative", "format": ".1f"},
                    },
                },
            ],
            "config": config(),
        },
    )

    # 10. Connected Dumbbell / Gap Chart: Share of Deaths >1 km vs Within 1 km of an SLS Service
    distance_order = [
        "Tasmania",
        "South Australia",
        "Western Australia",
        "Queensland",
        "Victoria",
        "New South Wales",
    ]
    dump(
        "distance.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Connected dumbbell chart comparing share of coastal drowning deaths within 1 km vs more than 1 km from an SLS service.",
            "width": 360,
            "height": 250,
            "padding": {"left": 12, "right": 20, "top": 10, "bottom": 10},
            "data": csv_data("distance.csv"),
            "transform": [
                {"calculate": "100 - datum.beyond_pct", "as": "calc_within_pct"},
                {"calculate": "datum.beyond_pct + '%'", "as": "beyond_label"},
                {"calculate": "(100 - datum.beyond_pct) + '%'", "as": "within_label"},
            ],
            "encoding": {
                "y": {
                    "field": "state",
                    "type": "nominal",
                    "sort": distance_order,
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                }
            },
            "layer": [
                {
                    "mark": {"type": "rule", "color": "#cbbab4", "strokeWidth": 3.5},
                    "encoding": {
                        "x": {
                            "field": "calc_within_pct",
                            "type": "quantitative",
                            "title": "Share of coastal deaths (%) — Within 1 km (blue) vs. >1 km (red)",
                            "scale": {"zero": True, "domain": [0, 106]},
                            "axis": {"values": [0, 20, 40, 60, 69, 80, 100]},
                        },
                        "x2": {"field": "beyond_pct"},
                    },
                },
                {
                    "mark": {"type": "circle", "color": SEA, "size": 120, "opacity": 1},
                    "encoding": {
                        "x": {"field": "calc_within_pct", "type": "quantitative"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "calc_within_pct", "type": "quantitative", "title": "Within 1 km (%)"},
                        ],
                    },
                },
                {
                    "mark": {"type": "circle", "color": WINE, "size": 150, "opacity": 1},
                    "encoding": {
                        "x": {"field": "beyond_pct", "type": "quantitative"},
                        "tooltip": [
                            {"field": "state", "type": "nominal", "title": "State"},
                            {"field": "beyond_pct", "type": "quantitative", "title": "More than 1 km away (%)"},
                            {"field": "calc_within_pct", "type": "quantitative", "title": "Within 1 km (%)"},
                        ],
                    },
                },
                {
                    "mark": {"type": "rule", "color": WINE, "strokeWidth": 1.5, "strokeDash": [4, 3]},
                    "encoding": {"x": {"datum": 69}},
                },
                {
                    "transform": [
                        {"filter": "datum.code == 'Tas' || datum.code == 'SA' || datum.code == 'NSW'"},
                    ],
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 9,
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "color": WINE,
                    },
                    "encoding": {
                        "x": {"field": "beyond_pct", "type": "quantitative"},
                        "text": {"field": "beyond_label", "type": "nominal"},
                    },
                },
                {
                    "transform": [
                        {"filter": "datum.code == 'Tas' || datum.code == 'SA' || datum.code == 'NSW'"},
                    ],
                    "mark": {
                        "type": "text",
                        "align": "right",
                        "dx": -9,
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "color": SEA,
                    },
                    "encoding": {
                        "x": {"field": "calc_within_pct", "type": "quantitative"},
                        "text": {"field": "within_label", "type": "nominal"},
                    },
                },
            ],
            "config": config(),
        },
    )

    # 11. Sunburst Chart (Distinct Categorical Hues + Direct Percentage Labels on Every Slice + Single Clean Legend!)
    dump(
        "sunburst.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Two-ring hierarchical sunburst with distinct categorical hues and direct percentage annotations on every slice.",
            "width": 360,
            "height": 350,
            "padding": {"left": 16, "right": 16, "top": 8, "bottom": 8},
            "layer": [
                {
                    "data": csv_data("sunburst_inner.csv"),
                    "transform": [
                        {"calculate": "format(datum.pct, '.1f') + '%'", "as": "pct_str"},
                    ],
                    "layer": [
                        {
                            "mark": {"type": "arc", "innerRadius": 52, "outerRadius": 114, "stroke": "#ffffff", "strokeWidth": 2},
                            "encoding": {
                                "theta": {"field": "count", "type": "quantitative", "stack": True},
                                "order": {"field": "ord", "type": "quantitative"},
                                "color": {
                                    "field": "label",
                                    "type": "nominal",
                                    "scale": {
                                        "domain": [
                                            "Beach · 56.0% (84)",
                                            "Offshore · 18.7% (28)",
                                            "Rock/cliff · 12.7% (19)",
                                            "Other coastal · 12.7% (19)",
                                        ],
                                        "range": [TERRA_CAT, TEAL_CAT, OCHRE, PLUM],
                                    },
                                    "legend": {
                                        "title": "Inner ring · Coastal location (% of 150)",
                                        "orient": "bottom",
                                        "columns": 2,
                                        "labelLimit": 180,
                                    },
                                },
                                "tooltip": [
                                    {"field": "slice", "type": "nominal", "title": "Location"},
                                    {"field": "pct", "type": "quantitative", "title": "Share of total (%)", "format": ".1f"},
                                    {"field": "count", "type": "quantitative", "title": "Drowning deaths (n)"},
                                ],
                            },
                        },
                        {
                            "mark": {
                                "type": "text",
                                "radius": 83,
                                "font": FONT,
                                "fontSize": 11.5,
                                "fontWeight": 700,
                                "color": "#ffffff",
                            },
                            "encoding": {
                                "theta": {"field": "count", "type": "quantitative", "stack": True},
                                "order": {"field": "ord", "type": "quantitative"},
                                "text": {"field": "pct_str", "type": "nominal"},
                            },
                        },
                    ],
                },
                {
                    "data": csv_data("sunburst_outer.csv"),
                    "transform": [
                        {
                            "calculate": (
                                "datum.ord == 1 ? 'Unknown 23.3%' : "
                                "datum.ord == 2 ? 'Rip 19.3%' : "
                                "datum.ord == 3 ? 'No rip 13.3%' : ''"
                            ),
                            "as": "outer_pct_str",
                        }
                    ],
                    "layer": [
                        {
                            "mark": {"type": "arc", "innerRadius": 120, "outerRadius": 166, "stroke": "#ffffff", "strokeWidth": 2},
                            "encoding": {
                                "theta": {"field": "count", "type": "quantitative", "stack": True},
                                "order": {"field": "ord", "type": "quantitative"},
                                "color": {
                                    "field": "slice",
                                    "type": "nominal",
                                    "scale": {
                                        "domain": [
                                            "Beach · Rip unknown (41.7% of beach)",
                                            "Beach · Rip confirmed (34.5% of beach)",
                                            "Beach · No rip (23.8% of beach)",
                                            "Offshore waters (non-beach)",
                                            "Rock or cliff (non-beach)",
                                            "Other coastal waters (non-beach)",
                                        ],
                                        "range": [SLATE_NAVY, "#a8332d", "#2a6f68", PAPER, PAPER, PAPER],
                                    },
                                    "legend": None,
                                },
                                "opacity": {
                                    "condition": {"test": "datum.band == 'Beach'", "value": 1.0},
                                    "value": 0.0,
                                },
                                "tooltip": [
                                    {"field": "slice", "type": "nominal", "title": "Beach rip breakdown"},
                                    {"field": "pct_total", "type": "quantitative", "title": "Share of all 150 deaths (%)", "format": ".1f"},
                                    {"field": "pct_beach", "type": "quantitative", "title": "Share of 84 beach deaths (%)", "format": ".1f"},
                                    {"field": "count", "type": "quantitative", "title": "Deaths (n)"},
                                ],
                            },
                        },
                        {
                            "mark": {
                                "type": "text",
                                "radius": 143,
                                "font": FONT,
                                "fontSize": 10.5,
                                "fontWeight": 700,
                                "color": "#ffffff",
                            },
                            "encoding": {
                                "theta": {"field": "count", "type": "quantitative", "stack": True},
                                "order": {"field": "ord", "type": "quantitative"},
                                "text": {"field": "outer_pct_str", "type": "nominal"},
                            },
                        },
                    ],
                },
                {
                    "data": {"values": [{"t1": "150 deaths"}]},
                    "mark": {"type": "text", "font": FONT, "fontSize": 13, "fontWeight": 600, "dy": -7, "color": INK},
                    "encoding": {"text": {"field": "t1", "type": "nominal"}},
                },
                {
                    "data": {"values": [{"t2": "56.0% beach"}]},
                    "mark": {"type": "text", "font": FONT, "fontSize": 11.5, "dy": 10, "color": WINE},
                    "encoding": {"text": {"field": "t2", "type": "nominal"}},
                },
            ],
            "resolve": {"scale": {"color": "independent"}},
            "config": config(),
        },
    )

    # 12. Activity Counts & Share (Selective Annotations on Key Bars Only)
    activity_order = [
        "Swimming and wading",
        "All other coastal activities",
        "Boating",
        "Snorkelling",
        "Falls into water",
    ]
    dump(
        "activity_counts.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "2023/24 coastal drowning deaths by activity with selective annotations.",
            "width": 320,
            "height": 210,
            "padding": {"left": 24, "right": 24, "top": 8, "bottom": 8},
            "data": csv_data("activity_counts.csv"),
            "transform": [
                {
                    "calculate": "datum.deaths + ' (' + format(datum.deaths / 150 * 100, '.1f') + '%)'",
                    "as": "calc_label",
                }
            ],
            "encoding": {
                "y": {
                    "field": "activity",
                    "type": "nominal",
                    "sort": activity_order,
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                },
                "x": {
                    "field": "deaths",
                    "type": "quantitative",
                    "title": "Coastal drowning deaths in 2023/24 (n = 150)",
                    "scale": {"zero": True, "domain": [0, 78]},
                    "axis": {"tickCount": 5},
                },
            },
            "layer": [
                {
                    "mark": {"type": "bar", "height": {"band": 0.58}, "cornerRadiusEnd": 2},
                    "encoding": {
                        "color": {
                            "condition": {"test": "datum.activity == 'Swimming and wading'", "value": WINE},
                            "value": "#9e8f89",
                        },
                        "tooltip": [
                            {"field": "activity", "type": "nominal", "title": "Activity"},
                            {"field": "deaths", "type": "quantitative", "title": "Deaths (2023/24)"},
                            {"field": "calc_label", "type": "nominal", "title": "Count & share"},
                        ],
                    },
                },
                {
                    "transform": [
                        {"filter": "datum.activity == 'Swimming and wading' || datum.activity == 'Boating' || datum.activity == 'Falls into water'"},
                    ],
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 7,
                        "font": FONT,
                        "fontSize": 12,
                        "fontWeight": 600,
                        "color": INK,
                    },
                    "encoding": {
                        "text": {"field": "calc_label", "type": "nominal"},
                    },
                },
            ],
            "config": config(),
        },
    )

    # 13. Slope Activity (Interactive Legend-Bound Slope Chart)
    dump(
        "slope_activity.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Interactive legend-bound slope chart comparing activity share of coastal drowning deaths in 2014–24 vs 2023/24.",
            "width": 440,
            "height": 290,
            "padding": {"left": 14, "right": 16, "top": 8, "bottom": 8},
            "data": csv_data("slope_activity.csv"),
            "transform": [
                {
                    "calculate": "format(datum.share, '.1f') + '%'",
                    "as": "share_pct",
                }
            ],
            "layer": [
                {
                    "params": [
                        {
                            "name": "act_sel",
                            "select": {"type": "point", "fields": ["activity"]},
                            "bind": "legend",
                        }
                    ],
                    "mark": {"type": "line", "strokeWidth": 2.8},
                    "encoding": {
                        "x": {
                            "field": "period",
                            "type": "ordinal",
                            "sort": ["2014–24", "2023/24"],
                            "title": None,
                            "scale": {"padding": 0.3},
                            "axis": {"labelAngle": 0, "labelFontSize": 13, "labelFontWeight": 600},
                        },
                        "y": {
                            "field": "share",
                            "type": "quantitative",
                            "title": "Share of coastal drowning deaths (%)",
                            "scale": {"zero": True, "domain": [0, 48]},
                            "axis": {"tickCount": 5},
                        },
                        "color": {
                            "field": "activity",
                            "type": "nominal",
                            "scale": {
                                "domain": ["Swimming and wading", "Boating", "Snorkelling", "All other activities"],
                                "range": [TERRA_CAT, TEAL_CAT, OCHRE, "#786f66"],
                            },
                            "legend": {
                                "title": "Click legend to highlight activity:",
                                "orient": "bottom",
                                "columns": 2,
                            },
                        },
                        "opacity": {
                            "condition": {"param": "act_sel", "value": 1},
                            "value": 0.2,
                        },
                        "tooltip": [
                            {"field": "activity", "type": "nominal", "title": "Activity"},
                            {"field": "period", "type": "nominal", "title": "Period"},
                            {"field": "share", "type": "quantitative", "title": "Share (%)", "format": ".1f"},
                            {"field": "deaths", "type": "quantitative", "title": "Deaths"},
                        ],
                    },
                },
                {
                    "mark": {"type": "circle", "size": 75},
                    "encoding": {
                        "x": {"field": "period", "type": "ordinal", "sort": ["2014–24", "2023/24"]},
                        "y": {"field": "share", "type": "quantitative"},
                        "color": {
                            "field": "activity",
                            "type": "nominal",
                            "scale": {
                                "domain": ["Swimming and wading", "Boating", "Snorkelling", "All other activities"],
                                "range": [TERRA_CAT, TEAL_CAT, OCHRE, "#786f66"],
                            },
                            "legend": None,
                        },
                        "opacity": {
                            "condition": {"param": "act_sel", "value": 1},
                            "value": 0.25,
                        },
                    },
                },
                *[
                    {
                        "transform": [{"filter": f"datum.activity == '{act}' && datum.period == '2023/24'"}],
                        "mark": {
                            "type": "text",
                            "align": "left",
                            "dx": 10,
                            "dy": dy,
                            "font": FONT,
                            "fontSize": 12,
                            "fontWeight": 600,
                            "color": col,
                        },
                        "encoding": {
                            "x": {"field": "period", "type": "ordinal", "sort": ["2014–24", "2023/24"]},
                            "y": {"field": "share", "type": "quantitative"},
                            "text": {"field": "share_pct", "type": "nominal"},
                        },
                    }
                    for act, dy, col in [
                        ("All other activities", -8, MUTED),
                        ("Swimming and wading", 10, TERRA_CAT),
                        ("Boating", -4, TEAL_CAT),
                        ("Snorkelling", 8, OCHRE),
                    ]
                ],
                *[
                    {
                        "transform": [{"filter": f"datum.activity == '{act}' && datum.period == '2014–24'"}],
                        "mark": {
                            "type": "text",
                            "align": "right",
                            "dx": -10,
                            "dy": dy,
                            "font": FONT,
                            "fontSize": 12,
                            "fontWeight": 600,
                            "color": col,
                        },
                        "encoding": {
                            "x": {"field": "period", "type": "ordinal", "sort": ["2014–24", "2023/24"]},
                            "y": {"field": "share", "type": "quantitative"},
                            "text": {"field": "share_pct", "type": "nominal"},
                        },
                    }
                    for act, dy, col in [
                        ("All other activities", -4, MUTED),
                        ("Swimming and wading", 4, TERRA_CAT),
                        ("Boating", 0, TEAL_CAT),
                        ("Snorkelling", 0, OCHRE),
                    ]
                ],
            ],
            "config": config(),
        },
    )

    # 14. True Pictorial ISOTYPE Unit Chart (All 50 Human Figures + In-Chart Annotations)
    dump(
        "isotype.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "Pictorial ISOTYPE chart of 150 coastal drowning deaths using human figure glyphs (each icon = 3 deaths) with in-chart annotations.",
            "data": csv_data("isotype.csv"),
            "padding": {"left": 10, "right": 10, "top": 8, "bottom": 16},
            "transform": [
                {
                    "calculate": (
                        "datum.group == 'Men' ? 'Men · 86.0% (129 deaths)' : 'Women · 14.0% (21 deaths)'"
                    ),
                    "as": "group_header",
                }
            ],
            "facet": {
                "column": {
                    "field": "group_header",
                    "title": None,
                    "sort": ["Men · 86.0% (129 deaths)", "Women · 14.0% (21 deaths)"],
                    "header": {"labelFontSize": 13.5, "labelFontWeight": 700, "labelPadding": 8},
                }
            },
            "spec": {
                "width": 205,
                "height": 185,
                "layer": [
                    {
                        "mark": {
                            "type": "point",
                            "filled": True,
                            "shape": PERSON_PATH,
                            "size": 210,
                        },
                        "encoding": {
                            "x": {"field": "col", "type": "ordinal", "axis": None, "scale": {"padding": 0.35}},
                            "y": {
                                "field": "row",
                                "type": "ordinal",
                                "axis": None,
                                "sort": "descending",
                                "scale": {"padding": 0.35},
                            },
                            "color": {
                                "field": "group",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["Men", "Women"],
                                    "range": [INDIGO_MALE, AMBER_FEMALE],
                                },
                                "legend": None,
                            },
                            "tooltip": [
                                {"field": "group_header", "type": "nominal", "title": "Group (1 figure = 3 deaths)"},
                            ],
                        },
                    },
                    {
                        "transform": [
                            {"filter": "datum.col == 0 && datum.row == 0"},
                            {
                                "calculate": (
                                    "datum.group == 'Men' ? '43 figures = 129 (0.97 per 100k)' : '7 figures = 21 (0.15 per 100k)'"
                                ),
                                "as": "panel_note",
                            },
                        ],
                        "mark": {
                            "type": "text",
                            "align": "left",
                            "dx": -6,
                            "dy": 22,
                            "font": FONT,
                            "fontSize": 11,
                            "fontWeight": 600,
                            "color": INK,
                        },
                        "encoding": {
                            "x": {"field": "col", "type": "ordinal"},
                            "y": {"field": "row", "type": "ordinal", "sort": "descending"},
                            "text": {"field": "panel_note", "type": "nominal"},
                        },
                    },
                ],
            },
            "config": config(),
        },
    )

    # 15. 100% Normalized Gender Share Comparison (Distinct Categorical Hues, Not Luminance)
    dump(
        "sex_share.vg.json",
        {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "100% stacked horizontal comparison of sex share in patrolling members vs coastal drowning deaths using distinct categorical hues.",
            "width": 350,
            "height": 185,
            "padding": {"left": 14, "right": 16, "top": 10, "bottom": 10},
            "data": csv_data("sex_share.csv"),
            "transform": [
                {
                    "calculate": "format(datum.share, '.1f') + '% ' + datum.sex",
                    "as": "calc_sex_label",
                }
            ],
            "encoding": {
                "y": {
                    "field": "group",
                    "type": "nominal",
                    "sort": ["Patrolling members", "Drowning deaths"],
                    "title": None,
                    "axis": {"domain": False, "ticks": False, "labelFontSize": 12.5},
                },
                "x": {
                    "field": "share",
                    "type": "quantitative",
                    "stack": "zero",
                    "title": "Share of people (%)",
                    "scale": {"domain": [0, 100]},
                    "axis": {"values": [0, 20, 40, 50, 60, 80, 100]},
                },
                "order": {"field": "sex", "type": "nominal", "sort": "descending"},
            },
            "layer": [
                {
                    "mark": {"type": "bar", "height": {"band": 0.56}, "stroke": PAPER, "strokeWidth": 1.5},
                    "encoding": {
                        "color": {
                            "field": "sex",
                            "type": "nominal",
                            "sort": ["Male", "Female"],
                            "scale": {
                                "domain": ["Male", "Female"],
                                "range": [INDIGO_MALE, AMBER_FEMALE],
                            },
                            "legend": {"title": "Sex (dedicated categorical hues):", "orient": "bottom"},
                        },
                        "tooltip": [
                            {"field": "group", "type": "nominal", "title": "Population group"},
                            {"field": "sex", "type": "nominal", "title": "Sex"},
                            {"field": "share", "type": "quantitative", "title": "Share (%)", "format": ".1f"},
                        ],
                    },
                },
                {
                    "mark": {"type": "rule", "color": PAPER, "strokeWidth": 1.5, "strokeDash": [3, 3]},
                    "encoding": {"x": {"datum": 50}},
                },
                {
                    "transform": [{"filter": "datum.sex == 'Male'"}],
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "dx": 10,
                        "font": FONT,
                        "fontSize": 12,
                        "fontWeight": 600,
                        "color": "#ffffff",
                    },
                    "encoding": {
                        "x": {"value": 8},
                        "text": {"field": "calc_sex_label", "type": "nominal"},
                    },
                },
                {
                    "transform": [{"filter": "datum.sex == 'Female'"}],
                    "mark": {
                        "type": "text",
                        "align": "right",
                        "dx": -8,
                        "font": FONT,
                        "fontSize": 11.5,
                        "fontWeight": 600,
                        "color": "#ffffff",
                    },
                    "encoding": {
                        "x": {"datum": 99},
                        "text": {"field": "calc_sex_label", "type": "nominal"},
                    },
                },
            ],
            "config": config(),
        },
    )


if __name__ == "__main__":
    main()
