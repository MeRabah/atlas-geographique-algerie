#!/usr/bin/env python3
"""Build open Maghreb layers for the atlas.

Sources (see README): Natural Earth 10m (public domain), geoBoundaries gbOpen
(ODbL), OpenStreetMap via Overpass (ODbL), British Geological Survey Africa
Groundwater Atlas country maps (CC BY-SA 4.0). Algeria wilayas, detailed
rivers, and water bodies already in public/data are kept.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import shapefile
from shapely.geometry import LineString, Point, Polygon, mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" / "data"
NE = Path("/tmp/ne")
GB = Path("/tmp/gb")
BGS = Path("/tmp/bgs")
OSM = Path("/tmp/osm")

COUNTRY_A3 = {"DZA", "MAR", "TUN", "LBY", "MRT", "SAH"}
ISO2 = {"DZ": "DZA", "MA": "MAR", "TN": "TUN", "LY": "LBY", "MR": "MRT", "EH": "ESH"}

NAMES = {
    "DZA": {"name": "Algérie", "name_en": "Algeria", "name_fr": "Algérie", "name_ar": "الجزائر"},
    "MAR": {"name": "Maroc", "name_en": "Morocco", "name_fr": "Maroc", "name_ar": "المغرب"},
    "TUN": {"name": "Tunisie", "name_en": "Tunisia", "name_fr": "Tunisie", "name_ar": "تونس"},
    "LBY": {"name": "Libye", "name_en": "Libya", "name_fr": "Libye", "name_ar": "ليبيا"},
    "MRT": {"name": "Mauritanie", "name_en": "Mauritania", "name_fr": "Mauritanie", "name_ar": "موريتانيا"},
    "SAH": {
        "name": "Sahara occidental",
        "name_en": "Western Sahara",
        "name_fr": "Sahara occidental",
        "name_ar": "الصحراء الغربية",
        "note": "Unité géographique distincte (Natural Earth). Son statut est contesté.",
        "note_en": "Shown as a separate geographic unit (Natural Earth). Its status is disputed.",
        "note_fr": "Unité géographique distincte (Natural Earth). Son statut est contesté.",
        "note_ar": "وحدة جغرافية منفصلة (Natural Earth). وضعها محل نزاع.",
    },
    "ESH": {},
}

FLOW = {
    "U": "Unconsolidated sediments",
    "CSIF": "Consolidated sedimentary, intergranular and fracture flow",
    "CSIFK": "Consolidated sedimentary with karst, intergranular and fracture flow",
    "CSF": "Consolidated sedimentary, fracture flow",
    "CSFK": "Consolidated sedimentary with karst, fracture flow",
    "B": "Basement",
    "I": "Igneous or metamorphic",
}
FLOW_FR = {
    "U": "Sédiments non consolidés",
    "CSIF": "Sédimentaire consolidé, écoulement intergranulaire et de fracture",
    "CSIFK": "Sédimentaire consolidé karstique, écoulement intergranulaire et de fracture",
    "CSF": "Sédimentaire consolidé, écoulement de fracture",
    "CSFK": "Sédimentaire consolidé karstique, écoulement de fracture",
    "B": "Socle",
    "I": "Roches ignées ou métamorphiques",
}
FLOW_AR = {
    "U": "رواسب غير متماسكة",
    "CSIF": "صخور رسوبية متماسكة، تدفق بين الحبيبات والشقوق",
    "CSIFK": "صخور رسوبية كارستية متماسكة",
    "CSF": "صخور رسوبية متماسكة، تدفق عبر الشقوق",
    "CSFK": "صخور رسوبية كارستية، تدفق عبر الشقوق",
    "B": "قاعدة صخرية",
    "I": "صخور نارية أو متحولة",
}
PROD_WORDS = {
    "VH": "very high",
    "H": "high",
    "M": "moderate",
    "L": "low",
    "VL": "very low",
    "U": "unknown",
}
PROD_FR = {
    "very high": "très forte",
    "high": "forte",
    "moderate": "modérée",
    "low": "faible",
    "very low": "très faible",
    "unknown": "inconnue",
    "variable": "variable",
}
PROD_AR = {
    "very high": "عالية جداً",
    "high": "عالية",
    "moderate": "متوسطة",
    "low": "ضعيفة",
    "very low": "ضعيفة جداً",
    "unknown": "غير معروفة",
    "variable": "متغيرة",
}

LITHO_FR = {
    "Recent-Quaternary unconsolidated sediments": "Sédiments quaternaires non consolidés",
    "Precambrian Metasedimentary": "Métasédimentaire précambrien",
    "Cenozoic marine sedimentary": "Sédimentaire marin cénozoïque",
    "Palaeozoic": "Paléozoïque",
    "Cretaceous sedimentary - North": "Sédimentaire crétacé (nord)",
    "Late Tertiary to Quaternary": "Tertiaire supérieur à quaternaire",
    "Cambrian to Silurian sedimentary": "Sédimentaire cambrien à silurien",
    "Devonian sedimentary": "Sédimentaire dévonien",
    "Cretaceous-Tertiary sedimentary": "Sédimentaire crétacé-tertiaire",
    "Triassic and Jurassic": "Trias et Jurassique",
    "Tertiary": "Tertiaire",
    "Triassic to Jurassic - North; sedimentary": "Sédimentaire trias-jurassique (nord)",
    "Sedimentary - Cambrian-Carboniferous": "Sédimentaire cambrien-carbonifère",
    "Cretaceous sedimentary - South": "Sédimentaire crétacé (sud)",
    "Precambrian, undifferentiated": "Précambrien indifférencié",
    "Sedimentary - Cretaceous-Tertiary": "Sédimentaire crétacé-tertiaire",
    "Cretaceous - Tertiary": "Crétacé-tertiaire",
    "Carboniferous sedimentary": "Sédimentaire carbonifère",
    "Precambrian Basement": "Socle précambrien",
    "Unconsolidated": "Non consolidé",
    "Cenozoic Volcanic": "Volcanique cénozoïque",
    "Tertiary-Quaternary unconsolidated sediments": "Sédiments tertiaires-quaternaires non consolidés",
    "Mesozoic sedimentary": "Sédimentaire mésozoïque",
    "Igneous (Palaeozoic-Mesozoic)": "Igné (paléozoïque-mésozoïque)",
    "Igneous": "Igné",
    "Early Cretaceous": "Crétacé inférieur",
    "Precambrian": "Précambrien",
    "Neogene volcanic": "Volcanique néogène",
    "Triassic to Jurassic - South; sedimentary": "Sédimentaire trias-jurassique (sud)",
    "Surface water": "Eau de surface",
    "Cretaceous Tertiary CT CI": "Crétacé-tertiaire",
    "Sedimentary - Cambrian-Tertiary, undifferentiated": "Sédimentaire cambrien-tertiaire indifférencié",
}

PARKS = [
    {"name": "Parc national de l'Ahaggar", "name_en": "Ahaggar National Park", "name_fr": "Parc national de l'Ahaggar", "name_ar": "حظيرة الأهقار", "country": "DZA", "coordinates": [5.53, 23.2]},
    {"name": "Parc national du Tassili n'Ajjer", "name_en": "Tassili n'Ajjer National Park", "name_fr": "Parc national du Tassili n'Ajjer", "name_ar": "حظيرة الطاسيلي ناجر", "country": "DZA", "coordinates": [9.0, 25.5]},
    {"name": "Parc national du Djurdjura", "name_en": "Djurdjura National Park", "name_fr": "Parc national du Djurdjura", "name_ar": "الحديقة الوطنية لجرجرة", "country": "DZA", "coordinates": [4.15, 36.47]},
    {"name": "Parc national d'El Kala", "name_en": "El Kala National Park", "name_fr": "Parc national d'El Kala", "name_ar": "الحديقة الوطنية للقالة", "country": "DZA", "coordinates": [8.42, 36.86]},
    {"name": "Parc national de Theniet El Had", "name_en": "Theniet El Had National Park", "name_fr": "Parc national de Theniet El Had", "name_ar": "الحديقة الوطنية لثنية الحد", "country": "DZA", "coordinates": [1.96, 35.86]},
    {"name": "Parc national de Chréa", "name_en": "Chréa National Park", "name_fr": "Parc national de Chréa", "name_ar": "الحديقة الوطنية للشريعة", "country": "DZA", "coordinates": [2.88, 36.43]},
    {"name": "Parc national de Gouraya", "name_en": "Gouraya National Park", "name_fr": "Parc national de Gouraya", "name_ar": "الحديقة الوطنية لقورايا", "country": "DZA", "coordinates": [5.09, 36.77]},
    {"name": "Parc national de Taza", "name_en": "Taza National Park", "name_fr": "Parc national de Taza", "name_ar": "الحديقة الوطنية لتازة", "country": "DZA", "coordinates": [5.55, 36.68]},
    {"name": "Parc national de Belezma", "name_en": "Belezma National Park", "name_fr": "Parc national de Belezma", "name_ar": "الحديقة الوطنية بلزمة", "country": "DZA", "coordinates": [6.05, 35.58]},
    {"name": "Parc national du Toubkal", "name_en": "Toubkal National Park", "name_fr": "Parc national du Toubkal", "name_ar": "المنتزه الوطني لتوبقال", "country": "MAR", "coordinates": [-7.92, 31.06]},
    {"name": "Parc national de Souss-Massa", "name_en": "Souss-Massa National Park", "name_fr": "Parc national de Souss-Massa", "name_ar": "المنتزه الوطني لسوس ماسة", "country": "MAR", "coordinates": [-9.65, 30.1]},
    {"name": "Parc national d'Ifrane", "name_en": "Ifrane National Park", "name_fr": "Parc national d'Ifrane", "name_ar": "المنتزه الوطني لإفران", "country": "MAR", "coordinates": [-5.15, 33.42]},
    {"name": "Parc national de Talassemtane", "name_en": "Talassemtane National Park", "name_fr": "Parc national de Talassemtane", "name_ar": "المنتزه الوطني لتالاسمطان", "country": "MAR", "coordinates": [-5.14, 35.15]},
    {"name": "Parc national d'Iriqui", "name_en": "Iriqui National Park", "name_fr": "Parc national d'Iriqui", "name_ar": "المنتزه الوطني لإريقي", "country": "MAR", "coordinates": [-6.6, 29.8]},
    {"name": "Parc national de l'Ichkeul", "name_en": "Ichkeul National Park", "name_fr": "Parc national de l'Ichkeul", "name_ar": "الحديقة الوطنية بإشكل", "country": "TUN", "coordinates": [9.67, 37.16]},
    {"name": "Parc national de Bouhedma", "name_en": "Bouhedma National Park", "name_fr": "Parc national de Bouhedma", "name_ar": "الحديقة الوطنية ببوهدمة", "country": "TUN", "coordinates": [9.65, 34.47]},
    {"name": "Parc national de Chaambi", "name_en": "Chaambi National Park", "name_fr": "Parc national de Chaambi", "name_ar": "الحديقة الوطنية بالشعانبي", "country": "TUN", "coordinates": [8.68, 35.2]},
    {"name": "Parc national d'El Feija", "name_en": "El Feija National Park", "name_fr": "Parc national d'El Feija", "name_ar": "الحديقة الوطنية بالفايجة", "country": "TUN", "coordinates": [8.3, 36.5]},
    {"name": "Parc national de Jbil", "name_en": "Jbil National Park", "name_fr": "Parc national de Jbil", "name_ar": "الحديقة الوطنية بجبيل", "country": "TUN", "coordinates": [9.0, 33.0]},
    {"name": "Parc national d'El Kouf", "name_en": "El Kouf National Park", "name_fr": "Parc national d'El Kouf", "name_ar": "الحديقة الوطنية بالكوف", "country": "LBY", "coordinates": [21.5, 32.75]},
    {"name": "Parc national de Karabolli", "name_en": "Karabolli National Park", "name_fr": "Parc national de Karabolli", "name_ar": "الحديقة الوطنية قربولي", "country": "LBY", "coordinates": [14.2, 32.8]},
    {"name": "Parc national du Banc d'Arguin", "name_en": "Banc d'Arguin National Park", "name_fr": "Parc national du Banc d'Arguin", "name_ar": "حظيرة حوض أرغين", "country": "MRT", "coordinates": [-16.3, 20.2]},
    {"name": "Parc national du Diawling", "name_en": "Diawling National Park", "name_fr": "Parc national du Diawling", "name_ar": "حظيرة جاولينغ", "country": "MRT", "coordinates": [-16.4, 16.35]},
]


def fold(text: str) -> str:
    s = unicodedata.normalize("NFD", text or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def clean(props: dict) -> dict:
    out = {}
    for key, value in props.items():
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue
        out[key] = value
    return out


def dump(path: Path, features: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{path.name:24} {len(features):5}  {path.stat().st_size/1e6:.2f} MB")


def round_coords(obj, nd: int):
    if isinstance(obj, (list, tuple)):
        if obj and isinstance(obj[0], (int, float)) and not isinstance(obj[0], bool):
            return [round(float(obj[0]), nd), round(float(obj[1]), nd)]
        return [round_coords(x, nd) for x in obj]
    return obj


def as_geom(g):
    if g is None or g.is_empty:
        return []
    if g.geom_type == "GeometryCollection":
        out = []
        for part in g.geoms:
            out.extend(as_geom(part))
        return out
    return [g]


def feature(geom, props, nd=4):
    geom = geom if geom.is_valid else geom.buffer(0)
    parts = [g for g in as_geom(geom) if not g.is_empty]
    if not parts:
        return None
    if len(parts) == 1:
        body = mapping(parts[0])
    else:
        kind = parts[0].geom_type
        if all(p.geom_type == "Polygon" for p in parts):
            body = mapping(unary_union(parts))
        elif all(p.geom_type == "LineString" for p in parts):
            body = {"type": "MultiLineString", "coordinates": [p.coords[:] for p in parts]}
        elif all(p.geom_type == "Point" for p in parts):
            body = mapping(parts[0])
        else:
            body = mapping(parts[0])
    body["coordinates"] = round_coords(body["coordinates"], nd)
    return {"type": "Feature", "properties": clean(props), "geometry": body}


def shp_reader(path: Path):
    return shapefile.Reader(str(path))


def load_countries():
    reader = shp_reader(NE / "ne_10m_admin_0_countries.shp")
    features = []
    geoms = []
    for rec in reader.iterShapeRecords():
        code = rec.record["ADM0_A3"]
        if code not in COUNTRY_A3:
            continue
        geom = shape(rec.shape.__geo_interface__)
        geom = geom.simplify(0.01, preserve_topology=True)
        meta = dict(NAMES[code])
        meta.update({
            "iso_a3": "ESH" if code == "SAH" else code,
            "type": rec.record["TYPE"] or "country",
            "pop_est": int(rec.record["POP_EST"] or 0),
        })
        if not meta.get("name_en"):
            meta["name_en"] = rec.record["NAME_EN"] or rec.record["NAME"]
        if not meta.get("name_fr"):
            meta["name_fr"] = rec.record["NAME_FR"] or meta["name"]
        if not meta.get("name_ar"):
            meta["name_ar"] = rec.record["NAME_AR"] or ""
        item = feature(geom, meta, 4)
        if item:
            features.append(item)
            geoms.append(geom)
    mask = unary_union(geoms).buffer(0.15)
    return features, mask


def clip_poly(geom, mask, tol):
    geom = geom.simplify(tol, preserve_topology=True)
    if not geom.intersects(mask):
        return None
    return geom.intersection(mask)


def provinces(mask):
    features = []
    # Algeria keeps the more recent 58-wilaya file, drawn on its own layer.
    for code, level in (("MAR", "ADM1"), ("TUN", "ADM1"), ("LBY", "ADM1"), ("MRT", "ADM1")):
        data = json.loads((GB / f"{code}_{level}.geojson").read_text())
        for raw in data["features"]:
            geom = clip_poly(shape(raw["geometry"]), mask, 0.012)
            if geom is None:
                continue
            props = raw.get("properties") or {}
            name = props.get("shapeName") or ""
            item = feature(geom, {
                "name": name,
                "name_en": name,
                "name_fr": name,
                "name_ar": name if any("\u0600" <= ch <= "\u06ff" for ch in name) else "",
                "iso": props.get("shapeISO") or "",
                "country": code,
                "level": "ADM1",
                "type": "province",
            }, 4)
            if item:
                features.append(item)
    # Natural Earth still has a Western Sahara unit; keep it with the provinces
    # so the territory is selectable even where Moroccan regions overlap it.
    reader = shp_reader(NE / "ne_10m_admin_1_states_provinces.shp")
    for rec in reader.iterShapeRecords():
        if rec.record["adm0_a3"] != "SAH":
            continue
        geom = clip_poly(shape(rec.shape.__geo_interface__), mask, 0.012)
        if geom is None:
            continue
        name = rec.record["name"] or "Western Sahara"
        item = feature(geom, {
            "name": NAMES["SAH"]["name_fr"],
            "name_en": rec.record["name_en"] or NAMES["SAH"]["name_en"],
            "name_fr": rec.record["name_fr"] or NAMES["SAH"]["name_fr"],
            "name_ar": rec.record["name_ar"] or NAMES["SAH"]["name_ar"],
            "country": "ESH",
            "level": "ADM1",
            "type": "territory",
            "note_en": NAMES["SAH"]["note_en"],
            "note_fr": NAMES["SAH"]["note_fr"],
            "note_ar": NAMES["SAH"]["note_ar"],
        }, 4)
        if item:
            features.append(item)
    return features


def adm2(mask):
    features = []
    # Algeria ADM2 in this geoBoundaries release repeats wilayas, so it is skipped.
    for code in ("MAR", "TUN", "MRT"):
        data = json.loads((GB / f"{code}_ADM2.geojson").read_text())
        for raw in data["features"]:
            geom = clip_poly(shape(raw["geometry"]), mask, 0.008)
            if geom is None:
                continue
            props = raw.get("properties") or {}
            name = props.get("shapeName") or ""
            arabic = any("\u0600" <= ch <= "\u06ff" for ch in name)
            item = feature(geom, {
                "name": name,
                "name_en": name,
                "name_fr": name,
                "name_ar": name if arabic else "",
                "country": code,
                "level": "ADM2",
                "type": "second-level",
            }, 4)
            if item:
                features.append(item)
    return features


def regions(mask):
    reader = shp_reader(NE / "ne_10m_geography_regions_polys.shp")
    features = []
    for rec in reader.iterShapeRecords():
        geom = shape(rec.shape.__geo_interface__)
        if not geom.intersects(mask):
            continue
        piece = geom.intersection(mask).simplify(0.02, preserve_topology=True)
        if piece.is_empty or piece.area < 0.05:
            continue
        name = rec.record["NAME"] or ""
        item = feature(piece, {
            "name": rec.record["NAME_FR"] or name,
            "name_en": rec.record["NAME_EN"] or name,
            "name_fr": rec.record["NAME_FR"] or name,
            "name_ar": rec.record["NAME_AR"] or "",
            "kind": "physical-region",
            "region": rec.record["REGION"] or "",
        }, 3)
        if item:
            features.append(item)
    return features


def lines_from_shp(shp_name, mask, name_fn, tol=0.02, kinds=("LineString", "MultiLineString")):
    reader = shp_reader(NE / shp_name)
    features = []
    for rec in reader.iterShapeRecords():
        geom = shape(rec.shape.__geo_interface__)
        if not geom.intersects(mask):
            continue
        piece = geom.intersection(mask).simplify(tol, preserve_topology=True)
        props = name_fn(rec.record)
        if not props:
            continue
        for part in as_geom(piece):
            if part.geom_type not in kinds or part.is_empty:
                continue
            if part.geom_type in ("LineString", "MultiLineString") and part.length < 0.05:
                continue
            item = feature(part, props, 3)
            if item:
                features.append(item)
    return features


def polys_from_shp(shp_name, mask, name_fn, tol=0.02, min_area=0.002):
    reader = shp_reader(NE / shp_name)
    features = []
    for rec in reader.iterShapeRecords():
        geom = shape(rec.shape.__geo_interface__)
        if not geom.intersects(mask):
            continue
        piece = geom.intersection(mask).simplify(tol, preserve_topology=True)
        props = name_fn(rec.record)
        if not props:
            continue
        for part in as_geom(piece):
            if part.geom_type not in ("Polygon", "MultiPolygon") or part.area < min_area:
                continue
            item = feature(part, props, 3)
            if item:
                features.append(item)
    return features


def points_in(mask, shp_name, keep, props_fn):
    reader = shp_reader(NE / shp_name)
    features = []
    for rec in reader.iterShapeRecords():
        geom = shape(rec.shape.__geo_interface__)
        if geom.geom_type != "Point":
            geom = geom.centroid
        if not mask.covers(geom):
            continue
        if not keep(rec.record):
            continue
        item = feature(geom, props_fn(rec.record), 4)
        if item:
            features.append(item)
    return features


def decode_hg(code: str):
    raw = (code or "").strip()
    if not raw or raw.lower() == "n/a":
        return None
    flow, _, prod = raw.partition("-")
    flow = flow.strip()
    prod = prod.strip()
    # Strip uncertainty marks for the class, keep them in the note.
    uncertain = any(mark in prod for mark in ("?", "*", "(", ")"))
    prod_clean = prod.replace("?", "").replace("*", "").replace("(", "").replace(")", "").replace("V", "")
    # V was used both as very and as variable marker inside parentheses already removed.
    parts = [p for p in prod.replace("?", "").replace("*", "").replace("(", "/").replace(")", "").split("/") if p and p not in ("V",)]
    words = [PROD_WORDS.get(p, p.lower()) for p in parts] or ["unknown"]
    if len(words) == 2:
        level = f"{words[0]} to {words[1]}"
    else:
        level = words[0]
    if uncertain or "(V)" in prod or prod.endswith("V"):
        level = level + ", variable" if "variable" not in level else level
    flow_en = FLOW.get(flow, flow)
    flow_fr = FLOW_FR.get(flow, flow_en)
    flow_ar = FLOW_AR.get(flow, "")
    # Productivity bucket for the choropleth.
    if any(p in parts for p in ("VH", "H")) and not any(p in parts for p in ("L", "VL")):
        bucket = "H"
    elif "M" in parts and "L" not in parts and "VL" not in parts:
        bucket = "M"
    elif parts and all(p in ("L", "VL") for p in parts):
        bucket = "L"
    elif "H" in parts or "VH" in parts:
        bucket = "V"
    else:
        bucket = "U"
    fr_level = " à ".join(PROD_FR.get(w, w) for w in words)
    ar_level = " إلى ".join(PROD_AR.get(w, w) for w in words)
    return {
        "name": f"{flow_en} — {level} productivity",
        "name_en": f"{flow_en} — {level} productivity",
        "name_fr": f"{flow_fr} — productivité {fr_level}",
        "name_ar": f"{flow_ar} — إنتاجية {ar_level}".strip(" —"),
        "code": raw,
        "prod": bucket,
        "type": "aquifer",
    }


def hydro_and_geology(mask):
    aquifers = []
    geology = []
    for shp in sorted(BGS.rglob("*.shp")):
        reader = shapefile.Reader(str(shp))
        fields = [f[0] for f in reader.fields if f[0] != "DeletionFlag"]
        hg = next(f for f in fields if f.endswith("HGComb"))
        glg = next(f for f in fields if "GLG" in f)
        country = {
            "Algeria": "DZA",
            "Morocco": "MAR",
            "Tunisia": "TUN",
            "Mauritania": "MRT",
            "WesternSahara": "ESH",
        }.get(shp.stem.split("_")[0], "")
        for rec in reader.iterShapeRecords():
            geom = shape(rec.shape.__geo_interface__)
            if not geom.intersects(mask):
                continue
            piece = geom.simplify(0.04, preserve_topology=True).intersection(mask)
            if piece.is_empty:
                continue
            decoded = decode_hg(rec.record[hg] or "")
            lith = (rec.record[glg] or "").strip()
            if decoded:
                props = dict(decoded)
                props["country"] = country
                props["lithology"] = lith
                item = feature(piece, props, 3)
                if item:
                    aquifers.append(item)
            if lith and lith.lower() != "surface water":
                item = feature(piece, {
                    "name": lith,
                    "name_en": lith,
                    "name_fr": LITHO_FR.get(lith, lith),
                    "country": country,
                    "type": "geology",
                    "era": era_of(lith),
                }, 3)
                if item:
                    geology.append(item)
    return aquifers, geology


def era_of(lith: str) -> str:
    text = lith.lower()
    if "quaternary" in text or "unconsolidated" in text or "recent" in text:
        return "cenozoic"
    if "cenozoic" in text or "tertiary" in text or "neogene" in text:
        return "cenozoic"
    if "cretaceous" in text or "jurassic" in text or "triassic" in text or "mesozoic" in text:
        return "mesozoic"
    if "palaeozoic" in text or "paleozoic" in text or "devonian" in text or "carboniferous" in text or "silurian" in text or "cambrian" in text:
        return "paleozoic"
    if "precambrian" in text or "basement" in text:
        return "precambrian"
    if "igneous" in text or "volcanic" in text:
        return "igneous"
    return "other"


def osm_points(path: Path, mask, kind: str):
    data = json.loads(path.read_text())
    features = []
    for el in data.get("elements") or []:
        tags = el.get("tags") or {}
        lat = el.get("lat") or (el.get("center") or {}).get("lat")
        lon = el.get("lon") or (el.get("center") or {}).get("lon")
        if lat is None or lon is None:
            continue
        point = Point(float(lon), float(lat))
        if not mask.covers(point):
            continue
        name = tags.get("name") or tags.get("name:fr") or tags.get("name:en") or tags.get("name:ar")
        ele = None
        if kind == "peak":
            raw = str(tags.get("ele") or "").lower().replace("m", "").replace(",", ".").strip()
            token = raw.split()[0] if raw else ""
            try:
                ele = float(token)
            except ValueError:
                ele = None
            if ele is None or ele < 800:
                continue
        elif kind == "dam" and not name:
            continue
        props = {
            "name": tags.get("name:fr") or tags.get("name:en") or name,
            "name_en": tags.get("name:en") or name,
            "name_fr": tags.get("name:fr") or tags.get("name") or name,
            "name_ar": tags.get("name:ar") or "",
            "type": kind,
        }
        if ele is not None:
            props["ele"] = round(ele)
        if tags.get("wikidata"):
            props["wikidata"] = tags["wikidata"]
        item = feature(point, props, 4)
        if item:
            features.append(item)
    return features


def highest_per_country(peaks, countries):
    """Keep high summits, plus each territory's highest peak even if it is lower."""
    chosen = []
    best = {}
    for feat in peaks:
        ele = feat["properties"].get("ele") or 0
        point = shape(feat["geometry"])
        code = None
        for iso, geom in countries:
            if geom.covers(point):
                code = iso
                break
        feat["properties"]["country"] = code or ""
        if code and ele > best.get(code, (-1, None))[0]:
            best[code] = (ele, feat)
        if ele >= 2500:
            chosen.append(feat)
    seen = {id(f) for f in chosen}
    for _iso, (ele, feat) in best.items():
        if feat is not None and id(feat) not in seen:
            chosen.append(feat)
            seen.add(id(feat))
    # Deduplicate stacked OSM nodes.
    unique = []
    used = set()
    for feat in sorted(chosen, key=lambda f: -(f["properties"].get("ele") or 0)):
        coords = feat["geometry"]["coordinates"]
        key = (round(coords[0], 2), round(coords[1], 2), fold(feat["properties"].get("name") or "")[:24])
        if key in used:
            continue
        used.add(key)
        unique.append(feat)
    return unique


def merge_named(existing_path: Path, extra: list, distance=0.08):
    if not existing_path.exists():
        return extra
    data = json.loads(existing_path.read_text())
    kept = list(data["features"])
    index = []
    for feat in kept:
        geom = feat.get("geometry") or {}
        if geom.get("type") == "Point":
            index.append((Point(geom["coordinates"]), fold(str((feat.get("properties") or {}).get("name") or ""))))
    for feat in extra:
        point = shape(feat["geometry"])
        name = fold(str(feat["properties"].get("name") or ""))
        if any(point.distance(other) < distance and (not name or name in other_name or other_name in name) for other, other_name in index):
            continue
        kept.append(feat)
        index.append((point, name))
    return kept


def country_geoms(country_features):
    pairs = []
    for feat in country_features:
        iso = feat["properties"].get("iso_a3")
        pairs.append((iso, shape(feat["geometry"])))
    return pairs


def osm_ways(path: Path, mask, kind: str, algeria):
    """Named OSM ways clipped to the Maghreb, skipping features already covered by the Algeria extract."""
    data = json.loads(path.read_text())
    features = []
    for el in data.get("elements") or []:
        tags = el.get("tags") or {}
        coords = [(p["lon"], p["lat"]) for p in el.get("geometry") or [] if "lon" in p and "lat" in p]
        if len(coords) < 2:
            continue
        closed = coords[0] == coords[-1] and len(coords) >= 4
        if kind == "water" and closed:
            geom = Polygon(coords)
        else:
            geom = LineString(coords)
        if not geom.is_valid:
            geom = geom.buffer(0)
        if geom.is_empty or not geom.intersects(mask):
            continue
        piece = geom.intersection(mask).simplify(0.008, preserve_topology=True)
        if piece.is_empty:
            continue
        if algeria is not None:
            if piece.geom_type in ("LineString", "MultiLineString"):
                overlap = algeria.intersection(piece).length
                if overlap > 0.6 * max(piece.length, 1e-9):
                    continue
            else:
                overlap = algeria.intersection(piece).area
                if overlap > 0.6 * max(piece.area, 1e-12):
                    continue
        name = tags.get("name:fr") or tags.get("name:en") or tags.get("name") or tags.get("name:ar")
        if not name:
            continue
        props = {
            "name": name,
            "name_en": tags.get("name:en") or tags.get("name") or name,
            "name_fr": tags.get("name:fr") or tags.get("name") or name,
            "name_ar": tags.get("name:ar") or "",
            "type": tags.get("water") or tags.get("natural") or tags.get("waterway") or kind,
            "source": "osm",
        }
        for part in as_geom(piece):
            if part.is_empty:
                continue
            if part.geom_type in ("LineString", "MultiLineString") and part.length < 0.03:
                continue
            if part.geom_type in ("Polygon", "MultiPolygon") and part.area < 0.0003:
                continue
            item = feature(part, props, 4)
            if item:
                features.append(item)
    return features


def append_new(path: Path, extra: list) -> list:
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"features": []}
    kept = [f for f in data.get("features") or [] if (f.get("properties") or {}).get("source") != "osm"]
    kept.extend(extra)
    return kept


def main():
    countries, mask = load_countries()
    dump(PUBLIC / "countries.geojson", countries)
    dump(PUBLIC / "provinces.geojson", provinces(mask))
    dump(PUBLIC / "adm2.geojson", adm2(mask))
    dump(PUBLIC / "regions.geojson", regions(mask))
    dump(PUBLIC / "rivers_major.geojson", lines_from_shp(
        "ne_10m_rivers_lake_centerlines.shp",
        mask,
        lambda r: {
            "name": r["name_fr"] or r["name_en"] or r["name"] or "Cours d’eau",
            "name_en": r["name_en"] or r["name"] or "",
            "name_fr": r["name_fr"] or r["name"] or "",
            "name_ar": r["name_ar"] or "",
            "type": "river",
        },
    ))
    dump(PUBLIC / "lakes.geojson", polys_from_shp(
        "ne_10m_lakes.shp",
        mask,
        lambda r: {
            "name": r["name_fr"] or r["name_en"] or r["name"] or "Lac",
            "name_en": r["name_en"] or r["name"] or "",
            "name_fr": r["name_fr"] or r["name"] or "",
            "name_ar": r["name_ar"] or "",
            "type": r["featurecla"] or "lake",
        },
        tol=0.01,
        min_area=0.0005,
    ))
    dump(PUBLIC / "roads.geojson", lines_from_shp(
        "ne_10m_roads.shp",
        mask,
        lambda r: {
            "name": r["name"] or r["type"] or "Route",
            "name_en": r["name"] or r["type"] or "Road",
            "name_fr": r["name"] or r["type"] or "Route",
            "type": r["type"] or "road",
        } if (r["type"] or "") in ("Major Highway", "Secondary Highway", "Primary Highway", "Beltway") or (r["expressway"] or 0) == 1 else None,
        tol=0.03,
    ))
    dump(PUBLIC / "rail.geojson", lines_from_shp(
        "ne_10m_railroads.shp",
        mask,
        lambda r: {"name": "Chemin de fer", "name_en": "Railway", "name_fr": "Chemin de fer", "type": "rail"},
        tol=0.03,
    ))
    dump(PUBLIC / "airports.geojson", points_in(
        mask,
        "ne_10m_airports.shp",
        lambda r: True,
        lambda r: {
            "name": r["name_fr"] or r["name_en"] or r["name"],
            "name_en": r["name_en"] or r["name"],
            "name_fr": r["name_fr"] or r["name"],
            "name_ar": r["name_ar"] or "",
            "iata": r["iata_code"] or "",
            "type": r["type"] or "airport",
        },
    ))
    dump(PUBLIC / "ports.geojson", points_in(
        mask,
        "ne_10m_ports.shp",
        lambda r: True,
        lambda r: {
            "name": r["name"] or "Port",
            "name_en": r["name"] or "Port",
            "name_fr": r["name"] or "Port",
            "type": "port",
        },
    ))
    aquifers, geology = hydro_and_geology(mask)
    dump(PUBLIC / "aquifers.geojson", aquifers)
    dump(PUBLIC / "geology_bgs.geojson", geology)

    algeria = next(shape(f["geometry"]) for f in countries if f["properties"].get("iso_a3") == "DZA")
    extra_rivers = osm_ways(OSM / "rivers.json", mask, "river", algeria)
    dump(PUBLIC / "rivers.geojson", append_new(PUBLIC / "rivers.geojson", extra_rivers))
    extra_waters = osm_ways(OSM / "waters.json", mask, "water", algeria)
    water_features = append_new(PUBLIC / "waters.geojson", extra_waters)
    dump(PUBLIC / "waters.geojson", water_features)
    lakes = []
    for feat in water_features:
        if feat["geometry"]["type"] not in ("Polygon", "MultiPolygon"):
            continue
        try:
            area = shape(feat["geometry"]).area
        except Exception:
            continue
        if area >= 0.008:
            lakes.append(feat)
    dump(PUBLIC / "lakes.geojson", lakes)

    peaks = osm_points(OSM / "peaks.json", mask, "peak")
    peaks = highest_per_country(peaks, country_geoms(countries))
    # Preserve the curated notes for the Algerian summits already in the atlas.
    notes = {
        "tahat": "Plus haut sommet d’Algérie, dans le Hoggar. L’altitude publiée diverge selon les sources (environ 2 908 m à 3 003 m).",
        "chelia": "Point culminant des Aurès et du nord de l’Algérie.",
        "khedidja": "Point culminant du Djurdjura et de l’Atlas tellien.",
    }
    notes_en = {
        "tahat": "Highest summit in Algeria, in the Hoggar. Published elevations differ by source (about 2,908 m to 3,003 m).",
        "chelia": "Highest summit of the Aurès and of northern Algeria.",
        "khedidja": "Highest summit of the Djurdjura and the Tell Atlas.",
    }
    for feat in peaks:
        blob = fold(feat["properties"].get("name") or "")
        for key, note in notes.items():
            if key in blob:
                feat["properties"]["note_fr"] = note
                feat["properties"]["note"] = note
                feat["properties"]["note_en"] = notes_en[key]
    dump(PUBLIC / "peaks.geojson", peaks)

    dams = osm_points(OSM / "dams.json", mask, "dam")
    dump(PUBLIC / "dams.geojson", merge_named(PUBLIC / "dams.geojson", dams, 0.05))

    places = points_in(
        mask,
        "ne_10m_populated_places.shp",
        lambda r: (r["ADM0CAP"] or 0) == 1 or (r["POP_MAX"] or 0) >= 150000,
        lambda r: {
            "name": r["NAME"],
            "name_en": r["NAMEASCII"] or r["NAME"],
            "name_fr": r["NAME"],
            "adm0": r["ADM0_A3"] or "",
            "pop": int(r["POP_MAX"] or 0),
            "capital": int(r["ADM0CAP"] or 0),
            "type": "place",
        },
    )
    dump(PUBLIC / "places.geojson", merge_named(PUBLIC / "places.geojson", places, 0.25))

    # Static bundle used when GitHub Pages has no API.
    keys = [
        "wilayas", "rivers", "waters", "dams", "peaks", "places", "regions",
        "countries", "provinces", "adm2", "rivers_major", "lakes", "roads",
        "rail", "airports", "ports", "aquifers", "geology_bgs", "parks",
    ]
    parks = []
    for park in PARKS:
        parks.append({
            "type": "Feature",
            "properties": clean({
                "name": park["name_fr"],
                "name_en": park["name_en"],
                "name_fr": park["name_fr"],
                "name_ar": park["name_ar"],
                "country": park["country"],
                "type": "park",
            }),
            "geometry": {"type": "Point", "coordinates": [round(park["coordinates"][0], 4), round(park["coordinates"][1], 4)]},
        })
    dump(PUBLIC / "parks.geojson", parks)

    bundle = {}
    for key in keys:
        filename = "geology_bgs.geojson" if key == "geology_bgs" else f"{key}.geojson"
        bundle[key] = json.loads((PUBLIC / filename).read_text(encoding="utf-8"))
    text = "window.ATLAS_DATA=" + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";\n"
    out = ROOT / "public" / "atlas-data.js"
    out.write_text(text, encoding="utf-8")
    print(f"atlas-data.js {out.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
