(function () {
  let DATA = window.ATLAS_DATA || {};
  const I18N = {
    fr: {
      layers: "Couches",
      base: "Fond de carte",
      relief: "Relief ombré",
      ortho: "Orthophoto",
      inct: "Carte topographique INCT",
      topo: "Topographie",
      mnt: "Modèle numérique de terrain",
      contours: "Courbes de niveau",
      slope: "Pente",
      hydro: "Hydrographie",
      rivers: "Cours d’eau et oueds",
      waters: "Lacs, chotts et sebkhas",
      dams: "Barrages",
      nappes: "Nappes phréatiques",
      basins: "Bassins versants",
      limits: "Limites et références",
      wilayas: "Wilayas",
      dairas: "Dairas et communes",
      geology: "Géologie (ASGA / BNDG)",
      places: "Toponymie",
      hint: "Cliquer un sommet, un oued ou un barrage pour l’inspecter.",
      search: "Rechercher un lieu, un oued, une wilaya",
      statusMid: "58 wilayas · 2 381 741 km²",
      scale: "Échelle",
      type: "Type",
      wilaya: "Wilaya",
      length: "Longueur",
      outlet: "Exutoire",
      near: "Près de",
      elevation: "Altitude",
      river: "Cours d’eau",
      water: "Plan d’eau",
      dam: "Barrage",
      peak: "Sommet",
      admin: "Limite administrative",
      basinBtn: "Voir le bassin versant",
      noBasin: "Les bassins versants ne sont pas encore chargés.",
      src: "Données ouvertes pour le prototype (SRTM / tuiles de terrain, cours d’eau OSM, limites administratives). INCT et ANRH restent les références nationales.",
      errInct: "La carte topographique INCT est commercialisée et n’est pas librement téléchargeable. Licence requise — impossible de charger cette couche.",
      errGeneric: "Impossible de charger cette couche.",
      errNappes: "Aucun jeu ouvert de nappes phréatiques n’est encore branché.",
      errBasins: "Les bassins versants ne sont pas encore branchés.",
      errContours: "Les courbes de niveau ne sont pas encore branchées.",
      errSlope: "La couche de pente n’est pas encore branchée.",
      errDairas: "Les contours des dairas et communes ne sont pas encore branchés.",
      errGeology: "La géologie ASGA / BNDG nécessite une licence. Impossible de charger cette couche.",
      retry: "Réessayer",
    },
    ar: {
      layers: "الطبقات",
      base: "خلفية الخريطة",
      relief: "تضاريس مظللة",
      ortho: "صورة جوية",
      inct: "الخريطة الطبوغرافية INCT",
      topo: "التضاريس",
      mnt: "النموذج الرقمي للارتفاع",
      contours: "منحنيات التسوية",
      slope: "الانحدار",
      hydro: "الهيدروغرافيا",
      rivers: "الأودية والمجاري",
      waters: "البحيرات والشطوط والسبخات",
      dams: "السدود",
      nappes: "المياه الجوفية",
      basins: "الأحواض المائية",
      limits: "الحدود والمراجع",
      wilayas: "الولايات",
      dairas: "الدوائر والبلديات",
      geology: "الجيولوجيا (ASGA / BNDG)",
      places: "الأسماء الجغرافية",
      hint: "انقر على قمة أو وادٍ أو سد لعرض التفاصيل.",
      search: "ابحث عن مكان أو وادٍ أو ولاية",
      statusMid: "58 ولاية · 2 381 741 كم²",
      scale: "المقياس",
      type: "النوع",
      wilaya: "الولاية",
      length: "الطول",
      outlet: "المصب",
      near: "بالقرب من",
      elevation: "الارتفاع",
      river: "مجرى مائي",
      water: "مسطح مائي",
      dam: "سد",
      peak: "قمة",
      admin: "حدود إدارية",
      basinBtn: "عرض الحوض المائي",
      noBasin: "الأحواض المائية غير محمّلة بعد.",
      src: "بيانات مفتوحة للنموذج الأولي (SRTM، مجاري OpenStreetMap، الحدود الإدارية). تبقى INCT وANRH المرجعان الوطنيان.",
      errInct: "الخريطة الطبوغرافية INCT غير متاحة للتنزيل الحر وتتطلب ترخيصاً.",
      errGeneric: "تعذّر تحميل هذه الطبقة.",
      errNappes: "لم تُربط بعد طبقة مفتوحة للمياه الجوفية.",
      errBasins: "لم تُربط بعد طبقة الأحواض المائية.",
      errContours: "لم تُربط بعد منحنيات التسوية.",
      errSlope: "لم تُربط بعد طبقة الانحدار.",
      errDairas: "لم تُربط بعد حدود الدوائر والبلديات.",
      errGeology: "بيانات الجيولوجيا ASGA / BNDG تتطلب ترخيصاً.",
      retry: "إعادة المحاولة",
    },
  };

  const FACTS = {
    chelif: {
      match: /chelif|chélif|cheliff|chlef|chleff|وادي الشلف|واد الشلف|الشلف/i,
      kickerKey: "river",
      title: { fr: "Oued Chelif", ar: "وادي الشلف" },
      chips: { fr: ["Hydrographie", "Tell", "Méditerranée"], ar: ["هيدروغرافيا", "التل", "البحر الأبيض المتوسط"] },
      meta: {
        fr: [
          ["Type", "Oued"],
          ["Longueur", "725 km"],
          ["Exutoire", "Méditerranée"],
          ["Près de", "Mostaganem"],
        ],
        ar: [
          ["النوع", "واد"],
          ["الطول", "725 كم"],
          ["المصب", "البحر الأبيض المتوسط"],
          ["بالقرب من", "مستغانم"],
        ],
      },
      note: {
        fr: "Plus long cours d’eau d’Algérie. Il traverse le Tell et se jette dans la Méditerranée près de Mostaganem (certaines sources indiquent 733 km).",
        ar: "أطول مجرى مائي في الجزائر. يعبر التل ويصب في البحر الأبيض المتوسط قرب مستغانم.",
      },
    },
    tahat: {
      match: /tahat|تاهات/i,
      kickerKey: "peak",
      title: { fr: "Mont Tahat", ar: "جبل تاهات" },
      chips: { fr: ["Topographie", "Hoggar"], ar: ["تضاريس", "الهقار"] },
      meta: {
        fr: [
          ["Type", "Sommet"],
          ["Chaîne", "Hoggar"],
        ],
        ar: [
          ["النوع", "قمة"],
          ["السلسلة", "الهقار"],
        ],
      },
      note: {
        fr: "Plus haut sommet d’Algérie, dans le Hoggar. L’altitude publiée diverge selon les sources (environ 2 908 m à 3 003 m), elle n’est donc pas affichée ici comme une valeur unique.",
        ar: "أعلى قمة في الجزائر، في الهقار. تختلف الارتفاعات المنشورة حسب المصادر (حوالي 2908 م إلى 3003 م).",
      },
    },
  };

  let lang = "fr";
  const t = (k) => I18N[lang][k] || k;

  function applyI18n() {
    document.documentElement.lang = lang === "ar" ? "ar" : "fr";
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      el.placeholder = t(el.getAttribute("data-i18n-placeholder"));
    });
    document.querySelectorAll(".lang button").forEach((b) => {
      b.classList.toggle("on", b.dataset.lang === lang);
    });
    updateScale();
    if (selected) showInspector(selected);
    if (map.getLayer("place-labels")) {
      map.setLayoutProperty("place-labels", "text-field", ["coalesce", lang === "ar" ? ["get", "name_ar"] : ["get", "name"], ["get", "name"]]);
    }
    if (map.getLayer("peak-labels")) {
      map.setLayoutProperty("peak-labels", "text-field", ["coalesce", lang === "ar" ? ["get", "name_ar"] : ["get", "name"], ["get", "name"]]);
    }
  }

  const UNAVAILABLE = {
    inct: "errInct",
    contours: "errContours",
    slope: "errSlope",
    nappes: "errNappes",
    basins: "errBasins",
    dairas: "errDairas",
    geology: "errGeology",
  };

  const BASES = ["relief", "ortho"];
  const state = {
    relief: true,
    ortho: false,
    inct: false,
    mnt: true,
    rivers: true,
    waters: true,
    dams: false,
    wilayas: true,
    places: true,
  };

  const style = {
    version: 8,
    glyphs: "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",
    sources: {
      relief: {
        type: "raster",
        tiles: ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}"],
        tileSize: 256,
        attribution: "Esri, USGS",
        maxzoom: 13,
      },
      ortho: {
        type: "raster",
        tiles: ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
        tileSize: 256,
        attribution: "Esri",
        maxzoom: 19,
      },
      terrain: {
        type: "raster-dem",
        tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],
        encoding: "terrarium",
        tileSize: 256,
        maxzoom: 15,
      },
    },
    layers: [
      { id: "bg", type: "background", paint: { "background-color": "#8fb7b4" } },
      { id: "relief", type: "raster", source: "relief", paint: { "raster-opacity": 1 } },
      { id: "ortho", type: "raster", source: "ortho", layout: { visibility: "none" }, paint: { "raster-opacity": 1 } },
      {
        id: "hillshade",
        type: "hillshade",
        source: "terrain",
        paint: { "hillshade-exaggeration": 0.45, "hillshade-shadow-color": "#3d4a36" },
      },
    ],
  };

  const map = new maplibregl.Map({
    container: "map",
    style,
    center: [3, 28],
    zoom: 4.7,
    minZoom: 4,
    maxZoom: 14,
    maxBounds: [[-12, 16], [16, 40]],
    attributionControl: false,
  });

  let selected = null;

  function addDataLayers() {
    map.addSource("wilayas", { type: "geojson", data: DATA.wilayas });
    map.addSource("rivers", { type: "geojson", data: DATA.rivers });
    map.addSource("waters", { type: "geojson", data: DATA.waters });
    map.addSource("dams", { type: "geojson", data: DATA.dams });
    map.addSource("peaks", { type: "geojson", data: DATA.peaks });
    map.addSource("places", { type: "geojson", data: DATA.places });
    map.addSource("highlight", { type: "geojson", data: { type: "FeatureCollection", features: [] } });

    map.addLayer({
      id: "wilayas-fill",
      type: "fill",
      source: "wilayas",
      paint: { "fill-color": "#1d4a3a", "fill-opacity": 0.04 },
    });
    map.addLayer({
      id: "wilayas-line",
      type: "line",
      source: "wilayas",
      paint: { "line-color": "#1d4a3a", "line-width": 1, "line-opacity": 0.65 },
    });
    map.addLayer({
      id: "waters-fill",
      type: "fill",
      source: "waters",
      paint: { "fill-color": "#4aa3b5", "fill-opacity": 0.45 },
    });
    map.addLayer({
      id: "waters-line",
      type: "line",
      source: "waters",
      paint: { "line-color": "#1f6f86", "line-width": 1.2 },
    });
    map.addLayer({
      id: "rivers-line",
      type: "line",
      source: "rivers",
      paint: { "line-color": "#1f6f86", "line-width": 1.4, "line-opacity": 0.9 },
    });
    map.addLayer({
      id: "dams-circle",
      type: "circle",
      source: "dams",
      layout: { visibility: "none" },
      paint: { "circle-radius": 5, "circle-color": "#2b4f8c", "circle-stroke-color": "#f6f1e8", "circle-stroke-width": 1.2 },
    });
    map.addLayer({
      id: "peaks-circle",
      type: "circle",
      source: "peaks",
      paint: { "circle-radius": 5, "circle-color": "#b85a2a", "circle-stroke-color": "#f6f1e8", "circle-stroke-width": 1.3 },
    });
    map.addLayer({
      id: "places-circle",
      type: "circle",
      source: "places",
      paint: { "circle-radius": 3.2, "circle-color": "#1a241e", "circle-stroke-color": "#f6f1e8", "circle-stroke-width": 1.4 },
    });
    map.addLayer({
      id: "place-labels",
      type: "symbol",
      source: "places",
      layout: {
        "text-field": ["coalesce", ["get", "name"], ["get", "name_ar"]],
        "text-size": 12,
        "text-offset": [0.9, 0],
        "text-anchor": "left",
        "text-font": ["Open Sans Regular", "Arial Unicode MS Regular"],
      },
      paint: { "text-color": "#2a3328", "text-halo-color": "rgba(246,241,232,0.85)", "text-halo-width": 1.4 },
    });
    map.addLayer({
      id: "peak-labels",
      type: "symbol",
      source: "peaks",
      layout: {
        "text-field": ["get", "name"],
        "text-size": 11,
        "text-offset": [0, 0.95],
        "text-anchor": "top",
        "text-font": ["Open Sans Regular", "Arial Unicode MS Regular"],
      },
      paint: { "text-color": "#3d4a44", "text-halo-color": "rgba(246,241,232,0.85)", "text-halo-width": 1.4 },
    });
    map.addLayer({
      id: "highlight-line",
      type: "line",
      source: "highlight",
      paint: { "line-color": "#1f6f86", "line-width": 3.2 },
    });
    map.addLayer({
      id: "highlight-fill",
      type: "fill",
      source: "highlight",
      filter: ["==", ["geometry-type"], "Polygon"],
      paint: { "fill-color": "#1f6f86", "fill-opacity": 0.15 },
    });
    map.addLayer({
      id: "highlight-circle",
      type: "circle",
      source: "highlight",
      filter: ["==", ["geometry-type"], "Point"],
      paint: {
        "circle-radius": 7,
        "circle-color": "#1f6f86",
        "circle-stroke-color": "#f6f1e8",
        "circle-stroke-width": 2,
      },
    });

    const clickable = ["rivers-line", "waters-fill", "dams-circle", "peaks-circle", "wilayas-fill", "places-circle"];
    clickable.forEach((id) => {
      map.on("click", id, (e) => {
        if (e.originalEvent) e.originalEvent._atlasHit = true;
        if (!e.features || !e.features[0]) return;
        const f = e.features[0];
        const kind =
          id.startsWith("rivers") ? "river" :
          id.startsWith("waters") ? "water" :
          id.startsWith("dams") ? "dam" :
          id.startsWith("peaks") ? "peak" :
          id.startsWith("wilayas") ? "admin" : "place";
        selectFeature(f, kind);
      });
      map.on("mouseenter", id, () => { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", id, () => { map.getCanvas().style.cursor = ""; });
    });
  }

  function setVisibility(layerIds, on) {
    layerIds.forEach((id) => {
      if (map.getLayer(id)) map.setLayoutProperty(id, "visibility", on ? "visible" : "none");
    });
  }

  function setBase(kind) {
    state.relief = kind === "relief";
    state.ortho = kind === "ortho";
    if (map.getLayer("relief")) map.setLayoutProperty("relief", "visibility", state.relief ? "visible" : "none");
    if (map.getLayer("ortho")) map.setLayoutProperty("ortho", "visibility", state.ortho ? "visible" : "none");
    syncLayerRows();
  }

  function setMnt(on) {
    state.mnt = on;
    if (map.getLayer("hillshade")) map.setLayoutProperty("hillshade", "visibility", on ? "visible" : "none");
  }

  function toggleData(key, on) {
    state[key] = on;
    if (key === "rivers") setVisibility(["rivers-line"], on);
    if (key === "waters") setVisibility(["waters-fill", "waters-line"], on);
    if (key === "dams") setVisibility(["dams-circle"], on);
    if (key === "wilayas") setVisibility(["wilayas-fill", "wilayas-line"], on);
    if (key === "places") setVisibility(["places-circle", "place-labels", "peaks-circle", "peak-labels"], on);
  }

  function showLayerError(key) {
    const row = document.querySelector(`.layer[data-layer="${key}"]`);
    const msg = document.getElementById("msg-" + key);
    if (row) row.classList.add("err");
    if (msg) {
      msg.textContent = t(UNAVAILABLE[key] || "errGeneric") + " ";
      const retry = document.createElement("button");
      retry.type = "button";
      retry.textContent = t("retry");
      retry.style.cssText = "border:0;background:none;color:inherit;text-decoration:underline;cursor:pointer;font:inherit;padding:0";
      retry.onclick = () => showLayerError(key);
      msg.appendChild(retry);
      msg.classList.add("show");
    }
  }

  function syncLayerRows() {
    document.querySelectorAll(".layer[data-layer]").forEach((row) => {
      const key = row.dataset.layer;
      row.classList.toggle("on", !!state[key]);
    });
  }

  document.querySelectorAll(".layer[data-layer]").forEach((row) => {
    row.addEventListener("click", () => {
      const key = row.dataset.layer;
      if (UNAVAILABLE[key]) {
        showLayerError(key);
        return;
      }
      if (key === "relief" || key === "ortho") {
        setBase(key);
        return;
      }
      if (key === "mnt") {
        setMnt(!state.mnt);
        syncLayerRows();
        return;
      }
      toggleData(key, !state[key]);
      syncLayerRows();
    });
  });

  function lookupFacts(name) {
    if (!name) return null;
    for (const fact of Object.values(FACTS)) {
      if (fact.match.test(name)) return fact;
    }
    return null;
  }

  function selectFeature(feature, kind, group) {
    const features = (group && group.length) ? group : [feature];
    selected = { feature, kind };
    map.getSource("highlight").setData({ type: "FeatureCollection", features: features });
    showInspector(selected);
    try {
      const bbs = features.map((f) => bboxOf(f.geometry)).filter(Boolean);
      if (bbs.length) {
        const sw = [Math.min(...bbs.map((b) => b[0][0])), Math.min(...bbs.map((b) => b[0][1]))];
        const ne = [Math.max(...bbs.map((b) => b[1][0])), Math.max(...bbs.map((b) => b[1][1]))];
        map.fitBounds([sw, ne], {
          padding: { top: 96, bottom: 64, left: 320, right: 48 },
          maxZoom: kind === "river" ? 8 : 9,
          duration: 700,
        });
      }
    } catch (e) { /* ignore */ }
  }

  function bboxOf(geom) {
    if (!geom) return null;
    const coords = [];
    (function walk(n) {
      if (!n) return;
      if (typeof n[0] === "number") coords.push(n);
      else n.forEach(walk);
    })(geom.coordinates);
    if (!coords.length) return null;
    const xs = coords.map((c) => c[0]);
    const ys = coords.map((c) => c[1]);
    return [[Math.min(...xs), Math.min(...ys)], [Math.max(...xs), Math.max(...ys)]];
  }

  function showInspector({ feature, kind }) {
    const p = feature.properties || {};
    const name = (lang === "ar" && p.name_ar) ? p.name_ar : (p.name || p.name_fr || "—");
    const fact = lookupFacts([p.name, p.name_ar, p.name_fr].filter(Boolean).join(" "));
    const inspector = document.getElementById("inspector");
    let kicker = t(kind === "place" ? "admin" : kind);
    let title = name;
    let chips = [t(kind)];
    let meta = [];
    let note = p.note || "";
    if (p.wilaya) meta.push([t("wilaya"), p.wilaya]);
    if (p.type && kind !== "peak") meta.push([t("type"), p.type]);
    if (p.ele) meta.push([t("elevation"), p.ele + " m"]);
    if (fact) {
      kicker = t(fact.kickerKey);
      title = fact.title[lang] || title;
      chips = fact.chips[lang];
      meta = fact.meta[lang];
      note = fact.note[lang];
    }
    if (!meta.length) meta.push([t("type"), kicker]);
    inspector.innerHTML =
      `<div class="kicker">${esc(kicker)}</div>` +
      `<h1>${esc(title)}</h1>` +
      `<div class="chips">${chips.map((c) => `<span class="chip">${esc(c)}</span>`).join("")}</div>` +
      `<div class="meta">${meta.map(([a, b]) => `<div><small>${esc(a)}</small><b>${esc(b)}</b></div>`).join("")}</div>` +
      (note ? `<p class="note">${esc(note)}</p>` : "") +
      `<p class="src">${esc(t("src"))}</p>` +
      `<button class="btn" ${kind === "river" ? "" : "disabled"} id="basin-btn">${esc(t("basinBtn"))}</button>`;
    inspector.classList.add("show");
    const btn = document.getElementById("basin-btn");
    if (btn) {
      btn.onclick = () => {
        showLayerError("basins");
        btn.textContent = t("noBasin");
        btn.disabled = true;
      };
    }
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  const STOP = new Set(["oued","oueds","wadi","wad","nahr","jebel","djebel","mont","monts","mountain","wilaya","lac","chott","sebkha","barrage","ed","el","al","ain","the","de","du","le","la","wad","واد","وادي","جبل","ولاية","شط","سبخة","سد"]);

  function fold(s) {
    return String(s || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/['’`\-]/g, " ");
  }

  function aliasExtra(text) {
    const f = fold(text);
    if (/chelif|cheliff|chlef|chleff|الشلف/.test(f) || /الشلف/.test(text || "")) {
      return "oued chelif oued chlef chelif chlef وادي الشلف الشلف";
    }
    return "";
  }

  const ALIAS = {
    chelif: "chelif", cheliff: "chelif", chlef: "chelif", chleff: "chelif", chelef: "chelif",
    "الشلف": "chelif",
  };

  function normToken(t) { return ALIAS[t] || t; }

  function wordTokens(s) {
    return fold(s).split(/[^a-z0-9\u0600-\u06ff]+/).filter((t) => t.length >= 2 && !STOP.has(t)).map(normToken);
  }

  function canonicalize(name) {
    return wordTokens(name).join(" ");
  }

  function matchesQuery(item, q) {
    const hay = fold([item.label, item.name_ar, item.extra].filter(Boolean).join(" "));
    const qFold = fold(q);
    if (hay.includes(qFold)) return true;
    const qToks = wordTokens(q);
    if (!qToks.length) return false;
    const nameToks = wordTokens(hay);
    return qToks.every((qt) => nameToks.some((nt) => nt === qt || (qt.length >= 3 && nt.startsWith(qt))));
  }

  const index = [];
  function buildIndex() {
    index.length = 0;
    const seen = new Map();
    const push = (fc, kind) => {
      (fc.features || []).forEach((f) => {
        const p = f.properties || {};
        const label = p.name || p.name_ar || p.name_fr;
        if (!label) return;
        const key = kind + "::" + canonicalize(label);
        if (seen.has(key)) {
          seen.get(key).features.push(f);
          return;
        }
        const item = { label, name_ar: p.name_ar, kind, feature: f, features: [f], extra: aliasExtra([label, p.name_ar].filter(Boolean).join(" ")) };
        seen.set(key, item);
        index.push(item);
      });
    };
    push(DATA.rivers, "river");
    push(DATA.waters, "water");
    push(DATA.dams, "dam");
    push(DATA.wilayas, "admin");
    push(DATA.peaks, "peak");
    push(DATA.places, "place");
  }

  const searchInput = document.getElementById("search");
  const results = document.getElementById("results");
  searchInput.addEventListener("input", () => {
    const q = searchInput.value.trim();
    results.innerHTML = "";
    if (q.length < 2) {
      results.classList.remove("show");
      return;
    }
    const hits = index.filter((it) => matchesQuery(it, q)).slice(0, 12);
    hits.forEach((it) => {
      const fact = lookupFacts([it.label, it.name_ar].filter(Boolean).join(" "));
      const display = fact ? (fact.title[lang] || it.label) : ((lang === "ar" && it.name_ar) ? it.name_ar : it.label);
      const b = document.createElement("button");
      b.type = "button";
      b.innerHTML = `${esc(display)}<small>${esc(t(it.kind === "place" ? "admin" : it.kind))}</small>`;
      b.onclick = () => {
        results.classList.remove("show");
        searchInput.value = display;
        selectFeature(it.feature, it.kind, it.features);
      };
      results.appendChild(b);
    });
    results.classList.toggle("show", hits.length > 0);
  });

  document.querySelectorAll(".lang button").forEach((btn) => {
    btn.addEventListener("click", () => {
      lang = btn.dataset.lang;
      applyI18n();
    });
  });

  function fmtCoord(lng, lat) {
    const ns = lat >= 0 ? "N" : "S";
    const ew = lng >= 0 ? "E" : "O";
    const fmt = (n) => Math.abs(n).toFixed(2).replace(".", ",");
    return `${fmt(lat)}° ${ns} · ${fmt(lng)}° ${ew}`;
  }

  function updateScale() {
    const y = map.getContainer().clientHeight / 2;
    const left = map.unproject([0, y]);
    const right = map.unproject([100, y]);
    const mpp = left.distanceTo(right) / 100;
    let rf = mpp / (0.0254 / 96);
    if (rf >= 1e6) rf = Math.round(rf / 1e5) * 1e5;
    else if (rf >= 1e5) rf = Math.round(rf / 1e4) * 1e4;
    else rf = Math.round(rf / 1e3) * 1e3;
    const pretty = rf.toLocaleString(lang === "ar" ? "ar" : "fr-FR");
    document.getElementById("scale").textContent = `${t("scale")} 1 : ${pretty}`;
  }

  function frameAlgeria() {
    map.fitBounds([[-8.7, 18.96], [12.0, 37.1]], {
      padding: { top: 96, bottom: 64, left: 320, right: 48 },
      duration: 0,
    });
  }

  map.on("mousemove", (e) => {
    document.getElementById("coords").textContent = fmtCoord(e.lngLat.lng, e.lngLat.lat);
  });
  map.on("zoom", updateScale);
  map.on("click", (e) => {
    if (e.originalEvent && e.originalEvent._atlasHit) return;
    const hits = map.queryRenderedFeatures(e.point, {
      layers: ["rivers-line", "waters-fill", "dams-circle", "peaks-circle", "wilayas-fill", "places-circle"].filter((id) => map.getLayer(id)),
    });
    if (!hits.length) {
      selected = null;
      document.getElementById("inspector").classList.remove("show");
      if (map.getSource("highlight")) map.getSource("highlight").setData({ type: "FeatureCollection", features: [] });
    }
  });

  async function loadAtlasData() {
    const keys = ["wilayas", "rivers", "waters", "dams", "peaks", "places"];
    try {
      const health = await fetch("/api/health", { cache: "no-store" });
      if (!health.ok) throw new Error("no api");
      const loaded = {};
      await Promise.all(keys.map(async (k) => {
        const r = await fetch("/api/geojson/" + k);
        if (!r.ok) throw new Error(k);
        loaded[k] = await r.json();
      }));
      DATA = loaded;
    } catch (err) {
      DATA = window.ATLAS_DATA || DATA;
    }
  }

  map.on("load", () => {
    loadAtlasData().then(() => {
      addDataLayers();
      buildIndex();
      frameAlgeria();
      applyI18n();
      updateScale();
    });
  });
})();
