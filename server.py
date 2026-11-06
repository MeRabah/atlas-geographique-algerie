#!/usr/bin/env python3
"""Atlas géographique de l'Algérie — API + static file server."""

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

LAYERS = {
    "wilayas": {"file": "wilayas.geojson", "kind": "admin", "available": True, "label_fr": "Wilayas", "label_ar": "الولايات"},
    "rivers": {"file": "rivers.geojson", "kind": "river", "available": True, "label_fr": "Cours d’eau et oueds", "label_ar": "الأودية والمجاري"},
    "waters": {"file": "waters.geojson", "kind": "water", "available": True, "label_fr": "Lacs, chotts et sebkhas", "label_ar": "البحيرات والشطوط والسبخات"},
    "dams": {"file": "dams.geojson", "kind": "dam", "available": True, "label_fr": "Barrages", "label_ar": "السدود"},
    "peaks": {"file": "peaks.geojson", "kind": "peak", "available": True, "label_fr": "Sommets", "label_ar": "القمم"},
    "places": {"file": "places.geojson", "kind": "place", "available": True, "label_fr": "Toponymie", "label_ar": "الأسماء الجغرافية"},
    "regions": {"file": "regions.geojson", "kind": "region", "available": True, "label_fr": "Régions physiques", "label_ar": "المناطق الطبيعية"},
    "inct": {"available": False, "reason": "license", "message_fr": "La carte topographique INCT est commercialisée et n’est pas librement téléchargeable.", "message_ar": "الخريطة الطبوغرافية INCT غير متاحة للتنزيل الحر وتتطلب ترخيصاً."},
    "contours": {"available": False, "reason": "missing", "message_fr": "Les courbes de niveau ne sont pas encore branchées.", "message_ar": "لم تُربط بعد منحنيات التسوية."},
    "slope": {"available": False, "reason": "missing", "message_fr": "La couche de pente n’est pas encore branchée.", "message_ar": "لم تُربط بعد طبقة الانحدار."},
    "nappes": {"available": False, "reason": "missing", "message_fr": "Aucun jeu ouvert de nappes phréatiques n’est encore branché.", "message_ar": "لم تُربط بعد طبقة مفتوحة للمياه الجوفية."},
    "basins": {"available": False, "reason": "missing", "message_fr": "Les bassins versants ne sont pas encore branchés.", "message_ar": "لم تُربط بعد طبقة الأحواض المائية."},
    "dairas": {"available": False, "reason": "missing", "message_fr": "Les contours des dairas et communes ne sont pas encore branchés.", "message_ar": "لم تُربط بعد حدود الدوائر والبلديات."},
    "geology": {"available": False, "reason": "license", "message_fr": "La géologie ASGA / BNDG nécessite une licence.", "message_ar": "بيانات الجيولوجيا ASGA / BNDG تتطلب ترخيصاً."},
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
    "river": {"fr": "Cours d’eau", "ar": "مجرى مائي"},
    "water": {"fr": "Plan d’eau", "ar": "مسطح مائي"},
    "dam": {"fr": "Barrage", "ar": "سد"},
    "peak": {"fr": "Sommet", "ar": "قمة"},
    "admin": {"fr": "Limite administrative", "ar": "حدود إدارية"},
    "place": {"fr": "Lieu", "ar": "مكان"},
    "region": {"fr": "Région", "ar": "منطقة"},
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
            if not meta.get("available"):
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
        lang = "ar" if lang == "ar" else "fr"
        text = query or ""
        for fact in FACTS:
            if fact["match"].search(text):
                return {
                    "found": True,
                    "special": True,
                    "kicker": fact["kicker"][lang],
                    "title": fact["title"][lang],
                    "chips": fact["chips"][lang],
                    "meta": fact["meta"][lang],
                    "note": fact["note"][lang],
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
        if item.get("type"):
            meta.append(["النوع" if lang == "ar" else "Type", item["type"]])
        if item.get("wilaya"):
            meta.append(["الولاية" if lang == "ar" else "Wilaya", item["wilaya"]])
        title = item["name_ar"] if lang == "ar" and item["name_ar"] else item["name"]
        return {
            "found": True,
            "special": False,
            "kicker": KIND_LABEL.get(k, KIND_LABEL["place"])[lang],
            "title": title,
            "chips": [KIND_LABEL.get(k, KIND_LABEL["place"])[lang]],
            "meta": meta or [["النوع" if lang == "ar" else "Type", KIND_LABEL.get(k, KIND_LABEL["place"])[lang]]],
            "note": "",
            "source": source_line(lang),
            "kind": k,
            "layer": item["layer"],
        }


def source_line(lang: str) -> str:
    if lang == "ar":
        return "بيانات مفتوحة للنموذج الأولي (SRTM، مجاري OpenStreetMap، الحدود الإدارية). تبقى INCT وANRH المرجعان الوطنيان."
    return "Données ouvertes pour le prototype (SRTM / tuiles de terrain, cours d’eau OSM, limites administratives). INCT et ANRH restent les références nationales."


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
            return self._json(200, {"ok": True, "name": "Atlas géographique de l’Algérie"})
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
        lang = "ar" if (qs.get("lang") or ["fr"])[0] == "ar" else "fr"
        items = []
        for key, meta in LAYERS.items():
            label_key = "label_ar" if lang == "ar" else "label_fr"
            msg_key = "message_ar" if lang == "ar" else "message_fr"
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
    parser = argparse.ArgumentParser(description="Atlas géographique de l’Algérie")
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
