#!/usr/bin/env python3
"""Atlas géographique du Maghreb — API + static file server."""

from __future__ import annotations

import argparse
import json
import re
from functools import cached_property
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
DATA = PUBLIC / "data"

def _labels(fr: str, ar: str, en: str) -> dict:
    return {"label_fr": fr, "label_ar": ar, "label_en": en}


def _missing(fr: str, ar: str, en: str, reason: str = "missing") -> dict:
    return {"available": False, "reason": reason, "message_fr": fr, "message_ar": ar, "message_en": en}


LAYERS = {
    "countries": {"file": "countries.geojson", "kind": "country", "available": True, **_labels("Pays du Maghreb", "بلدان المغرب الكبير", "Maghreb countries")},
    "wilayas": {"file": "wilayas.geojson", "kind": "admin", "available": True, **_labels("Wilayas d’Algérie", "ولايات الجزائر", "Algerian wilayas")},
    "provinces": {"file": "provinces.geojson", "kind": "admin", "available": True, **_labels("Provinces et régions", "الولايات والأقاليم", "Provinces and regions")},
    "adm2": {"file": "adm2.geojson", "kind": "admin", "available": True, **_labels("Découpage de second niveau", "التقسيم الإداري الثاني", "Second-level divisions")},
    "regions": {"file": "regions.geojson", "kind": "region", "available": True, **_labels("Régions physiques", "المناطق الطبيعية", "Physical regions")},
    "rivers": {"file": "rivers.geojson", "kind": "river", "available": True, **_labels("Cours d’eau et oueds", "الأودية والمجاري", "Rivers and wadis")},
    "rivers_major": {"file": "rivers_major.geojson", "kind": "river", "available": True, **_labels("Grands fleuves", "الأنهار الكبرى", "Major rivers")},
    "waters": {"file": "waters.geojson", "kind": "water", "available": True, **_labels("Lacs, chotts et sebkhas", "البحيرات والشطوط والسبخات", "Lakes, chotts and sebkhas")},
    "lakes": {"file": "lakes.geojson", "kind": "water", "available": True, **_labels("Grands plans d’eau", "المسطحات المائية الكبرى", "Large water bodies")},
    "dams": {"file": "dams.geojson", "kind": "dam", "available": True, **_labels("Barrages", "السدود", "Dams")},
    "peaks": {"file": "peaks.geojson", "kind": "peak", "available": True, **_labels("Sommets", "القمم", "Summits")},
    "places": {"file": "places.geojson", "kind": "place", "available": True, **_labels("Toponymie", "الأسماء الجغرافية", "Place names")},
    "parks": {"file": "parks.geojson", "kind": "park", "available": True, **_labels("Parcs nationaux", "الحدائق الوطنية", "National parks")},
    "roads": {"file": "roads.geojson", "kind": "road", "available": True, **_labels("Routes principales", "الطرق الرئيسية", "Main roads")},
    "rail": {"file": "rail.geojson", "kind": "rail", "available": True, **_labels("Chemins de fer", "السكك الحديدية", "Railways")},
    "airports": {"file": "airports.geojson", "kind": "airport", "available": True, **_labels("Aéroports", "المطارات", "Airports")},
    "ports": {"file": "ports.geojson", "kind": "port", "available": True, **_labels("Ports", "الموانئ", "Ports")},
    "aquifers": {"file": "aquifers.geojson", "kind": "aquifer", "available": True, "index": False, **_labels("Aquifères", "الطبقات المائية", "Aquifers")},
    "geology_bgs": {"file": "geology_bgs.geojson", "kind": "geology", "available": True, "index": False, **_labels("Géologie de surface", "الجيولوجيا السطحية", "Surface geology")},
    "inct": _missing("La carte topographique INCT est commercialisée et n’est pas librement téléchargeable.", "الخريطة الطبوغرافية INCT غير متاحة للتنزيل الحر وتتطلب ترخيصاً.", "The INCT topographic map is sold commercially and is not freely downloadable.", "license"),
    "contours": _missing("Les courbes de niveau de tout le Maghreb sont trop volumineuses pour cet atlas.", "منحنيات التسوية لكامل المغرب الكبير أكبر من طاقة هذا الأطلس.", "Contours for the whole Maghreb are too large for this atlas."),
    "slope": _missing("Aucune tuile ouverte de pente n’est branchée.", "لا توجد طبقة انحدار مفتوحة.", "No open slope tiles are connected."),
    "basins": _missing("HydroBASINS ne peut pas être republié sous sa licence.", "لا يسمح ترخيص HydroBASINS بإعادة النشر.", "HydroBASINS cannot be republished under its licence."),
    "dairas": _missing("Les communes d’Algérie ne sont pas dans le jeu ouvert utilisé ici. Le second niveau couvre le Maroc, la Tunisie et la Mauritanie.", "بلديات الجزائر غير موجودة في البيانات المفتوحة المستخدمة هنا.", "Algerian communes are not in the open dataset used here. Second-level divisions cover Morocco, Tunisia and Mauritania."),
    "geology": _missing("La géologie détaillée ASGA / BNDG nécessite une licence. La couche ouverte est la carte BGS au 1:5 000 000.", "الجيولوجيا التفصيلية ASGA / BNDG تتطلب ترخيصاً.", "Detailed ASGA / BNDG geology needs a licence. The open layer is the BGS 1:5,000,000 map.", "license"),
}

FACTS = [
    {
        "match": re.compile(r"chelif|chélif|cheliff|chlef|chleff|وادي الشلف|واد الشلف|الشلف", re.I),
        "kicker": {"fr": "Cours d’eau", "ar": "مجرى مائي"},
        "title": {"fr": "Oued Chelif", "ar": "وادي الشلف"},
        "chips": {"fr": ["Hydrographie", "Tell", "Méditerranée"], "ar": ["هيدروغرافيا", "التل", "البحر الأبيض المتوسط"]},
        "meta": {
            "fr": [["Type", "Oued"], ["Longueur", "725 km"], ["Exutoire", "Méditerranée"], ["Près de", "Mostaganem"]],
            "ar": [["النوع", "واد"], ["الطول", "725 كم"], ["المصب", "البحر الأبيض المتوسط"], ["بالقرب من", "مستغانم"]],
        },
        "note": {
            "fr": "Plus long cours d’eau d’Algérie. Il traverse le Tell et se jette dans la Méditerranée près de Mostaganem (certaines sources indiquent 733 km).",
            "ar": "أطول مجرى مائي في الجزائر. يعبر التل ويصب في البحر الأبيض المتوسط قرب مستغانم.",
        },
    },
    {
        "match": re.compile(r"tahat|تاهات", re.I),
        "kicker": {"fr": "Sommet", "ar": "قمة"},
        "title": {"fr": "Mont Tahat", "ar": "جبل تاهات"},
        "chips": {"fr": ["Topographie", "Hoggar"], "ar": ["تضاريس", "الهقار"]},
        "meta": {
            "fr": [["Type", "Sommet"], ["Chaîne", "Hoggar"]],
            "ar": [["النوع", "قمة"], ["السلسلة", "الهقار"]],
        },
        "note": {
            "fr": "Plus haut sommet d’Algérie, dans le Hoggar. L’altitude publiée diverge selon les sources (environ 2 908 m à 3 003 m), elle n’est donc pas affichée ici comme une valeur unique.",
            "ar": "أعلى قمة في الجزائر، في الهقار. تختلف الارتفاعات المنشورة حسب المصادر (حوالي 2908 م إلى 3003 م).",
        },
    },
]

KIND_LABEL = {
    "river": {"fr": "Cours d’eau", "ar": "مجرى مائي", "en": "River"},
    "water": {"fr": "Plan d’eau", "ar": "مسطح مائي", "en": "Water body"},
    "dam": {"fr": "Barrage", "ar": "سد", "en": "Dam"},
    "peak": {"fr": "Sommet", "ar": "قمة", "en": "Summit"},
    "admin": {"fr": "Limite administrative", "ar": "حدود إدارية", "en": "Administrative area"},
    "place": {"fr": "Lieu", "ar": "مكان", "en": "Place"},
    "region": {"fr": "Région", "ar": "منطقة", "en": "Region"},
    "country": {"fr": "Pays", "ar": "بلد", "en": "Country"},
    "park": {"fr": "Parc", "ar": "حديقة", "en": "Park"},
    "road": {"fr": "Route", "ar": "طريق", "en": "Road"},
    "rail": {"fr": "Chemin de fer", "ar": "سكة حديدية", "en": "Railway"},
    "airport": {"fr": "Aéroport", "ar": "مطار", "en": "Airport"},
    "port": {"fr": "Port", "ar": "ميناء", "en": "Port"},
    "aquifer": {"fr": "Aquifère", "ar": "طبقة مائية", "en": "Aquifer"},
    "geology": {"fr": "Géologie", "ar": "جيولوجيا", "en": "Geology"},
}


def empty_fc():
    return {"type": "FeatureCollection", "features": []}


STOP = {
    "oued", "oueds", "wadi", "wad", "nahr", "jebel", "djebel", "mont", "monts",
    "mountain", "wilaya", "lac", "chott", "sebkha", "barrage", "ed", "el", "al",
    "ain", "the", "de", "du", "le", "la", "واد", "وادي", "جبل", "ولاية", "شط", "سبخة", "سد",
}


def fold(text: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", text or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace("'", " ").replace("’", " ").replace("-", " ")


def alias_extra(text: str) -> str:
    if re.search(r"chelif|cheliff|chlef|chleff|chelef|الشلف", fold(text) + " " + (text or ""), re.I):
        return "oued chelif oued chlef chelif chlef وادي الشلف الشلف"
    return ""


ALIAS = {
    "chelif": "chelif",
    "cheliff": "chelif",
    "chlef": "chelif",
    "chleff": "chelif",
    "chelef": "chelif",
    "الشلف": "chelif",
}


def word_tokens(text: str) -> list[str]:
    parts = [t for t in re.split(r"[^a-z0-9\u0600-\u06ff]+", fold(text)) if len(t) >= 2 and t not in STOP]
    return [ALIAS.get(t, t) for t in parts]


def canonicalize(name: str) -> str:
    return " ".join(word_tokens(name))


def matches_query(item: dict, query: str) -> bool:
    blob = fold(" ".join([item.get("name") or "", item.get("name_ar") or "", item.get("name_fr") or "", item.get("extra") or ""]))
    qf = fold(query)
    if qf and qf in blob:
        return True
    q_toks = word_tokens(query)
    if not q_toks:
        return False
    n_toks = word_tokens(blob)
    return all(any(nt == qt or (len(qt) >= 3 and nt.startswith(qt)) for nt in n_toks) for qt in q_toks)


class AtlasStore:
    def __init__(self) -> None:
        self._cache: dict[str, dict] = {}

    def geojson(self, layer: str) -> dict:
        meta = LAYERS.get(layer)
        if not meta or not meta.get("available"):
            raise KeyError(layer)
        if layer not in self._cache:
            path = DATA / meta["file"]
            if not path.exists():
                self._cache[layer] = empty_fc()
            else:
                self._cache[layer] = json.loads(path.read_text(encoding="utf-8"))
        return self._cache[layer]

    @cached_property
    def index(self) -> list[dict]:
        items = []
        for layer, meta in LAYERS.items():
            if not meta.get("available") or meta.get("index") is False:
                continue
            kind = meta["kind"]
            for feat in self.geojson(layer).get("features") or []:
                props = feat.get("properties") or {}
                name = props.get("name") or props.get("name_fr") or props.get("name_ar")
                if not name:
                    continue
                items.append(
                    {
                        "name": name,
                        "name_ar": props.get("name_ar") or "",
                        "name_fr": props.get("name_fr") or props.get("name") or "",
                        "kind": kind,
                        "layer": layer,
                        "wilaya": props.get("wilaya") or props.get("code") or "",
                        "type": props.get("type") or kind,
                        "extra": alias_extra(" ".join([name, props.get("name_ar") or "", props.get("name_fr") or ""])),
                    }
                )
        return items

    def search(self, query: str, limit: int = 12) -> list[dict]:
        q = (query or "").strip()
        if len(q) < 2:
            return []
        hits = []
        seen: set[str] = set()
        rank = {"river": 0, "water": 1, "dam": 2, "peak": 3, "place": 4, "admin": 5, "region": 6}
        for item in self.index:
            if not matches_query(item, q):
                continue
            key = f"{item['kind']}::{canonicalize(item['name'])}"
            if key in seen:
                continue
            seen.add(key)
            hits.append(item)
        hits.sort(key=lambda x: (rank.get(x["kind"], 9), x["name"]))
        return hits[:limit]

    def inspect(self, query: str, lang: str = "fr", kind: str = "") -> dict | None:
        lang = lang if lang in ("fr", "en", "ar") else "fr"
        text = query or ""
        for fact in FACTS:
            if fact["match"].search(text):
                return {
                    "found": True,
                    "special": True,
                    "kicker": fact["kicker"].get(lang) or fact["kicker"]["fr"],
                    "title": fact["title"].get(lang) or fact["title"]["fr"],
                    "chips": fact["chips"].get(lang) or fact["chips"]["fr"],
                    "meta": fact["meta"].get(lang) or fact["meta"]["fr"],
                    "note": fact["note"].get(lang) or fact["note"]["fr"],
                    "source": source_line(lang),
                }
        hits = self.search(text, limit=1)
        if not hits and kind:
            return None
        item = hits[0] if hits else None
        if not item:
            return None
        k = item["kind"] or kind or "place"
        meta = []
        type_label = {"ar": "النوع", "en": "Type", "fr": "Type"}[lang]
        wilaya_label = {"ar": "الولاية", "en": "Wilaya", "fr": "Wilaya"}[lang]
        if item.get("type"):
            meta.append([type_label, item["type"]])
        if item.get("wilaya"):
            meta.append([wilaya_label, item["wilaya"]])
        title = item["name_ar"] if lang == "ar" and item["name_ar"] else item["name"]
        kind_label = (KIND_LABEL.get(k) or KIND_LABEL["place"]).get(lang) or KIND_LABEL["place"]["fr"]
        return {
            "found": True,
            "special": False,
            "kicker": kind_label,
            "title": title,
            "chips": [kind_label],
            "meta": meta or [[type_label, kind_label]],
            "note": "",
            "source": source_line(lang),
            "kind": k,
            "layer": item["layer"],
        }


def source_line(lang: str) -> str:
    if lang == "ar":
        return "بيانات مفتوحة (SRTM، OpenStreetMap، Natural Earth، geoBoundaries، أطلس المياه الجوفية لأفريقيا BGS). تبقى INCT وANRH المرجعان الوطنيان للجزائر."
    if lang == "en":
        return "Open data (SRTM terrain tiles, OpenStreetMap, Natural Earth, geoBoundaries, BGS Africa Groundwater Atlas). INCT and ANRH remain the Algerian national references."
    return "Données ouvertes (tuiles SRTM, OpenStreetMap, Natural Earth, geoBoundaries, Africa Groundwater Atlas du BGS). INCT et ANRH restent les références nationales algériennes."


STORE = AtlasStore()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        sys_stderr = __import__("sys").stderr
        sys_stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/api/health":
            return self._json(200, {"ok": True, "name": "Atlas géographique du Maghreb"})
        if path == "/api/layers":
            return self._layers(parsed)
        if path.startswith("/api/geojson/"):
            return self._geojson(path.rsplit("/", 1)[-1])
        if path == "/api/search":
            return self._search(parsed)
        if path == "/api/inspect":
            return self._inspect(parsed)
        if path == "/api" or path == "/api/":
            return self._json(200, {
                "ok": True,
                "endpoints": ["/api/health", "/api/layers", "/api/geojson/{layer}", "/api/search?q=", "/api/inspect?q="],
            })
        return super().do_GET()

    def _layers(self, parsed) -> None:
        qs = parse_qs(parsed.query)
        raw = (qs.get("lang") or ["fr"])[0]
        lang = raw if raw in ("fr", "en", "ar") else "fr"
        items = []
        for key, meta in LAYERS.items():
            label_key = f"label_{lang}"
            msg_key = f"message_{lang}"
            items.append({
                "id": key,
                "available": bool(meta.get("available")),
                "kind": meta.get("kind"),
                "label": meta.get(label_key) or key,
                "reason": meta.get("reason"),
                "message": meta.get(msg_key),
                "count": len(STORE.geojson(key).get("features") or []) if meta.get("available") else 0,
            })
        self._json(200, {"layers": items})

    def _geojson(self, layer: str) -> None:
        layer = layer.strip()
        meta = LAYERS.get(layer)
        if not meta:
            return self._json(404, {"error": "unknown_layer", "layer": layer})
        if not meta.get("available"):
            return self._json(404, {
                "error": meta.get("reason") or "unavailable",
                "layer": layer,
                "message": meta.get("message_fr"),
            })
        self._json(200, STORE.geojson(layer))

    def _search(self, parsed) -> None:
        qs = parse_qs(parsed.query)
        q = (qs.get("q") or [""])[0]
        try:
            limit = int((qs.get("limit") or ["12"])[0])
        except ValueError:
            limit = 12
        limit = max(1, min(limit, 25))
        self._json(200, {"query": q, "results": STORE.search(q, limit)})

    def _inspect(self, parsed) -> None:
        qs = parse_qs(parsed.query)
        q = (qs.get("q") or [""])[0]
        lang = (qs.get("lang") or ["fr"])[0]
        kind = (qs.get("kind") or [""])[0]
        card = STORE.inspect(q, lang, kind)
        if not card:
            return self._json(404, {"found": False, "query": q})
        self._json(200, card)

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Atlas géographique du Maghreb")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    # Warm the index so the first search is fast.
    _ = STORE.index
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Atlas running at http://{args.host}:{args.port}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
