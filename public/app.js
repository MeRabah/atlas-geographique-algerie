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
      nappes: "Aquifères",
      basins: "Bassins versants",
      limits: "Limites et références",
      wilayas: "Wilayas d’Algérie",
      dairas: "Dairas et communes",
      geology: "Géologie (ASGA / BNDG)",
      places: "Toponymie",
      countries: "Pays du Maghreb",
      provinces: "Provinces et régions",
      adm2: "Découpage de second niveau",
      regions: "Régions physiques",
      major: "Grands fleuves",
      lakes: "Grands plans d’eau",
      peaks: "Sommets",
      airports: "Aéroports",
      ports: "Ports",
      roads: "Routes principales",
      rail: "Chemins de fer",
      parks: "Parcs nationaux",
      bgs: "Géologie de surface",
      country: "Pays",
      population: "Population",
      lithology: "Lithologie",
      place: "Lieu",
      territory: "Territoire",
      region: "Région",
      aquifer: "Aquifère",
      road: "Route",
      hint: "Cliquer un lieu, un oued, un sommet ou une limite pour l’inspecter.",
      search: "Rechercher dans le Maghreb",
      statusMid: "Maghreb · six pays et territoires",
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
      src: "Données ouvertes (tuiles SRTM, OpenStreetMap, Natural Earth, geoBoundaries, Africa Groundwater Atlas du BGS). INCT et ANRH restent les références nationales algériennes.",
      errInct: "La carte topographique INCT est commercialisée et n’est pas librement téléchargeable. Licence requise — impossible de charger cette couche.",
      errGeneric: "Impossible de charger cette couche.",
      errNappes: "Aucun jeu ouvert de nappes phréatiques n’est encore branché.",
      errBasins: "Aucun bassin versant redistribuable n’est branché. HydroBASINS ne peut pas être republié sous sa licence.",
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
      countries: "بلدان المغرب الكبير",
      provinces: "الولايات والأقاليم",
      adm2: "التقسيم الإداري الثاني",
      regions: "المناطق الطبيعية",
      major: "الأنهار الكبرى",
      lakes: "المسطحات المائية الكبرى",
      peaks: "القمم",
      airports: "المطارات",
      ports: "الموانئ",
      roads: "الطرق الرئيسية",
      rail: "السكك الحديدية",
      parks: "الحدائق الوطنية",
      bgs: "الجيولوجيا السطحية",
      country: "البلد",
      population: "السكان",
      lithology: "الليثولوجيا",
      place: "مكان",
      territory: "إقليم",
      region: "منطقة",
      aquifer: "طبقة مائية",
      road: "طريق",
      hint: "انقر على مكان أو وادٍ أو قمة أو حد لعرض التفاصيل.",
      search: "ابحث في المغرب الكبير",
      statusMid: "المغرب الكبير · ستة بلدان وأقاليم",
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
      errBasins: "لا توجد طبقة أحواض قابلة لإعادة النشر. ترخيص HydroBASINS لا يسمح بإعادة نشر البيانات.",
      errContours: "لم تُربط بعد منحنيات التسوية.",
      errSlope: "لم تُربط بعد طبقة الانحدار.",
      errDairas: "لم تُربط بعد حدود الدوائر والبلديات.",
      errGeology: "بيانات الجيولوجيا ASGA / BNDG تتطلب ترخيصاً. طبقة الجيولوجيا السطحية المفتوحة هي خريطة BGS.",
      retry: "إعادة المحاولة",
    },
    en: {
      layers: "Layers",
      base: "Basemap",
      relief: "Shaded relief",
      ortho: "Imagery",
      inct: "INCT topographic map",
      topo: "Topography",
      mnt: "Terrain model",
      contours: "Contours",
      slope: "Slope",
      hydro: "Hydrography",
      rivers: "Rivers and wadis",
      waters: "Lakes, chotts and sebkhas",
      dams: "Dams",
      nappes: "Aquifers",
      basins: "Drainage basins",
      limits: "Boundaries and reference",
      wilayas: "Algerian wilayas",
      dairas: "Second-level divisions",
      geology: "Geology (ASGA / BNDG)",
      places: "Place names",
      countries: "Maghreb countries",
      provinces: "Provinces and regions",
      adm2: "Second-level divisions",
      regions: "Physical regions",
      major: "Major rivers",
      lakes: "Large water bodies",
      peaks: "Summits",
      airports: "Airports",
      ports: "Ports",
      roads: "Main roads",
      rail: "Railways",
      parks: "National parks",
      bgs: "Surface geology",
      country: "Country",
      population: "Population",
      lithology: "Lithology",
      place: "Place",
      territory: "Territory",
      region: "Region",
      aquifer: "Aquifer",
      road: "Road",
      hint: "Click a place, river, summit, or boundary to inspect it.",
      search: "Search the Maghreb",
      statusMid: "Maghreb · six countries and territories",
      scale: "Scale",
      type: "Type",
      wilaya: "Wilaya",
      length: "Length",
      outlet: "Outlet",
      near: "Near",
      elevation: "Elevation",
      river: "River",
      water: "Water body",
      dam: "Dam",
      peak: "Summit",
      admin: "Administrative area",
      basinBtn: "Show the drainage basin",
      noBasin: "Drainage basins are not loaded.",
      src: "Open data for this atlas (SRTM terrain tiles, OpenStreetMap, Natural Earth, geoBoundaries, BGS Africa Groundwater Atlas). INCT and ANRH remain the Algerian national references.",
      errInct: "The INCT topographic map is sold commercially and cannot be downloaded freely.",
      errGeneric: "This layer could not be loaded.",
      errNappes: "No open aquifer layer is connected.",
      errBasins: "No redistributable basin dataset is connected. HydroBASINS cannot be republished under its licence.",
      errContours: "Contour lines are not connected. A full Maghreb contour extract is too large for this atlas.",
      errSlope: "No open slope tiles are connected.",
      errDairas: "Second-level divisions are not connected.",
      errGeology: "The ASGA / BNDG geological map needs a licence. The open surface-geology layer is the BGS map.",
      retry: "Try again",
    },
  };

  const FACTS = {
    chelif: {
      match: /chelif|chélif|cheliff|chlef|chleff|وادي الشلف|واد الشلف|الشلف/i,
      kickerKey: "river",
      title: { fr: "Oued Chelif", ar: "وادي الشلف", en: "Chelif River" },
      chips: { fr: ["Hydrographie", "Tell", "Méditerranée"], ar: ["هيدروغرافيا", "التل", "البحر الأبيض المتوسط"], en: ["Hydrography", "Tell", "Mediterranean"] },
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
        en: [
          ["Type", "Wadi"],
          ["Length", "725 km"],
          ["Outlet", "Mediterranean"],
          ["Near", "Mostaganem"],
        ],
      },
      note: {
        fr: "Plus long cours d’eau d’Algérie. Il traverse le Tell et se jette dans la Méditerranée près de Mostaganem (certaines sources indiquent 733 km).",
        ar: "أطول مجرى مائي في الجزائر. يعبر التل ويصب في البحر الأبيض المتوسط قرب مستغانم.",
        en: "Longest river in Algeria. It crosses the Tell and reaches the Mediterranean near Mostaganem (some sources say 733 km).",
      },
    },
    tahat: {
      match: /tahat|تاهات/i,
      kickerKey: "peak",
      title: { fr: "Mont Tahat", ar: "جبل تاهات", en: "Mount Tahat" },
      chips: { fr: ["Topographie", "Hoggar"], ar: ["تضاريس", "الهقار"], en: ["Topography", "Hoggar"] },
      meta: {
        fr: [
          ["Type", "Sommet"],
          ["Chaîne", "Hoggar"],
        ],
        ar: [
          ["النوع", "قمة"],
          ["السلسلة", "الهقار"],
        ],
        en: [
          ["Type", "Summit"],
          ["Range", "Hoggar"],
        ],
      },
      note: {
        fr: "Plus haut sommet d’Algérie, dans le Hoggar. L’altitude publiée diverge selon les sources (environ 2 908 m à 3 003 m), elle n’est donc pas affichée ici comme une valeur unique.",
        ar: "أعلى قمة في الجزائر، في الهقار. تختلف الارتفاعات المنشورة حسب المصادر (حوالي 2908 م إلى 3003 م).",
        en: "Highest summit in Algeria, in the Hoggar. Published elevations differ by source (about 2,908 m to 3,003 m), so no single figure is shown.",
      },
    },
    toubkal: {
      match: /toubkal|توبقال/i,
      kickerKey: "peak",
      title: { fr: "Jbel Toubkal", ar: "جبل توبقال", en: "Jbel Toubkal" },
      chips: { fr: ["Topographie", "Haut Atlas"], ar: ["تضاريس", "الأطلس الكبير"], en: ["Topography", "High Atlas"] },
      meta: {
        fr: [["Type", "Sommet"], ["Chaîne", "Haut Atlas"], ["Altitude", "4 167 m"]],
        ar: [["النوع", "قمة"], ["السلسلة", "الأطلس الكبير"], ["الارتفاع", "4167 م"]],
        en: [["Type", "Summit"], ["Range", "High Atlas"], ["Elevation", "4,167 m"]],
      },
      note: {
        fr: "Plus haut sommet du Maghreb et de l’Afrique du Nord, dans le Haut Atlas marocain.",
        ar: "أعلى قمة في المغرب الكبير وشمال أفريقيا، في الأطلس الكبير.",
        en: "Highest summit of the Maghreb and of North Africa, in Morocco’s High Atlas.",
      },
    },
  };

  let lang = "fr";
  const t = (k) => I18N[lang][k] || k;

  function labelField() {
    if (lang === "ar") return ["coalesce", ["get", "name_ar"], ["get", "name"]];
    if (lang === "en") return ["coalesce", ["get", "name_en"], ["get", "name"]];
    return ["coalesce", ["get", "name_fr"], ["get", "name"]];
  }

  function applyI18n() {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.title = lang === "en"
      ? "Geographic Atlas of the Maghreb"
      : lang === "ar"
        ? "الأطلس الجغرافي للمغرب الكبير"
        : "Atlas géographique du Maghreb";
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
    ["place-labels", "peak-labels"].forEach((id) => {
      if (map.getLayer(id)) map.setLayoutProperty(id, "text-field", labelField());
    });
  }

  const UNAVAILABLE = {
    inct: "errInct",
    contours: "errContours",
    slope: "errSlope",
    basins: "errBasins",
    geology: "errGeology",
  };

  const BASES = ["relief", "ortho"];
  const state = {
    relief: true,
    ortho: false,
    inct: false,
    mnt: true,
    peaks: true,
    regions: false,
    rivers: true,
    major: true,
    waters: true,
    lakes: false,
    dams: false,
    nappes: false,
    countries: true,
    wilayas: true,
    provinces: true,
    adm2: false,
    bgs: false,
    places: true,
    parks: false,
    roads: false,
    rail: false,
    airports: false,
    ports: false,
  };

  const LAYER_IDS = {
    rivers: ["rivers-line"],
    major: ["rivers-major-line"],
    waters: ["waters-fill", "waters-line"],
    lakes: ["lakes-fill", "lakes-line"],
    dams: ["dams-circle"],
    wilayas: ["wilayas-fill", "wilayas-line"],
    places: ["places-circle", "place-labels"],
    peaks: ["peaks-circle", "peak-labels"],
    countries: ["countries-line", "countries-esh"],
    provinces: ["provinces-fill", "provinces-line"],
    adm2: ["adm2-fill", "adm2-line"],
    regions: ["regions-fill", "regions-line"],
    nappes: ["aquifers-fill", "aquifers-line"],
    bgs: ["geology-fill", "geology-line"],
    airports: ["airports-circle"],
    ports: ["ports-circle"],
    roads: ["roads-line"],
    rail: ["rail-line"],
    parks: ["parks-circle"],
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
    center: [3, 27],
    zoom: 3.9,
    minZoom: 3.3,
    maxZoom: 14,
    maxBounds: [[-19, 13.2], [27, 39]],
    attributionControl: false,
  });

  let selected = null;

  function fc(key) {
    const data = DATA[key];
    return data && data.type ? data : { type: "FeatureCollection", features: [] };
  }

  function shown(key) {
    return state[key] ? "visible" : "none";
  }

  function addFill(id, source, color, opacity, key) {
    map.addLayer({
      id,
      type: "fill",
      source,
      layout: { visibility: shown(key) },
      paint: { "fill-color": color, "fill-opacity": opacity },
    });
  }

  function addLine(id, source, color, width, key) {
    map.addLayer({
      id,
      type: "line",
      source,
      layout: { visibility: shown(key) },
      paint: { "line-color": color, "line-width": width, "line-opacity": 0.9 },
    });
  }

  function addDot(id, source, color, radius, key) {
    map.addLayer({
      id,
      type: "circle",
      source,
      layout: { visibility: shown(key) },
      paint: {
        "circle-radius": radius,
        "circle-color": color,
        "circle-stroke-color": "#f6f1e8",
        "circle-stroke-width": 1.15,
      },
    });
  }

  function addDataLayers() {
    ["wilayas", "rivers", "waters", "dams", "peaks", "places", "countries", "provinces", "adm2", "regions", "rivers_major", "lakes", "roads", "rail", "airports", "ports", "aquifers", "geology_bgs", "parks"].forEach((key) => {
      map.addSource(key, { type: "geojson", data: fc(key) });
    });
    map.addSource("highlight", { type: "geojson", data: { type: "FeatureCollection", features: [] } });

    map.addLayer({
      id: "geology-fill",
      type: "fill",
      source: "geology_bgs",
      layout: { visibility: shown("bgs") },
      paint: {
        "fill-color": ["match", ["get", "era"], "cenozoic", "#e6d3a1", "mesozoic", "#8fb7b4", "paleozoic", "#c4a36a", "precambrian", "#b85a2a", "igneous", "#8d6b8a", "#d7d0c4"],
        "fill-opacity": 0.55,
      },
    });
    addLine("geology-line", "geology_bgs", "#8a7a62", 0.4, "bgs");
    map.addLayer({
      id: "aquifers-fill",
      type: "fill",
      source: "aquifers",
      layout: { visibility: shown("nappes") },
      paint: {
        "fill-color": ["match", ["get", "prod"], "H", "#1f6f86", "M", "#4aa3b5", "L", "#c4a36a", "V", "#7a8a7e", "#b7c9ce"],
        "fill-opacity": 0.45,
      },
    });
    addLine("aquifers-line", "aquifers", "#1f6f86", 0.35, "nappes");
    addFill("regions-fill", "regions", "#8aa07a", 0.18, "regions");
    addLine("regions-line", "regions", "#3d4a36", 1, "regions");
    addFill("provinces-fill", "provinces", "#2a6b52", 0.06, "provinces");
    addLine("provinces-line", "provinces", "#2a6b52", 1.05, "provinces");
    addFill("wilayas-fill", "wilayas", "#1d4a3a", 0.05, "wilayas");
    addLine("wilayas-line", "wilayas", "#1d4a3a", 1, "wilayas");
    addFill("adm2-fill", "adm2", "#7a8a7e", 0.04, "adm2");
    addLine("adm2-line", "adm2", "#5c6b62", 0.7, "adm2");
    map.addLayer({
      id: "countries-line",
      type: "line",
      source: "countries",
      filter: ["!=", ["get", "iso_a3"], "ESH"],
      layout: { visibility: shown("countries") },
      paint: { "line-color": "#1a241e", "line-width": 1.8 },
    });
    map.addLayer({
      id: "countries-esh",
      type: "line",
      source: "countries",
      filter: ["==", ["get", "iso_a3"], "ESH"],
      layout: { visibility: shown("countries") },
      paint: { "line-color": "#1a241e", "line-width": 1.6, "line-dasharray": [2, 1.4] },
    });
    addFill("waters-fill", "waters", "#4aa3b5", 0.45, "waters");
    addLine("waters-line", "waters", "#1f6f86", 1, "waters");
    addFill("lakes-fill", "lakes", "#164e61", 0.28, "lakes");
    addLine("lakes-line", "lakes", "#164e61", 1.2, "lakes");
    addLine("rivers-line", "rivers", "#1f6f86", 1.15, "rivers");
    addLine("rivers-major-line", "rivers_major", "#164e61", 2.6, "major");
    addLine("roads-line", "roads", "#5c6b62", 1.15, "roads");
    addLine("rail-line", "rail", "#6b5a3a", 1.25, "rail");
    addDot("dams-circle", "dams", "#2b4f8c", 4.5, "dams");
    addDot("airports-circle", "airports", "#3d4a44", 4, "airports");
    addDot("ports-circle", "ports", "#1f6f86", 4.5, "ports");
    addDot("parks-circle", "parks", "#1d4a3a", 5, "parks");
    addDot("peaks-circle", "peaks", "#b85a2a", 4.4, "peaks");
    addDot("places-circle", "places", "#1a241e", 3.1, "places");
    map.addLayer({
      id: "place-labels",
      type: "symbol",
      source: "places",
      layout: {
        visibility: shown("places"),
        "text-field": labelField(),
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
        visibility: shown("peaks"),
        "text-field": labelField(),
        "text-size": 11,
        "text-offset": [0, 0.9],
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
      paint: { "circle-radius": 7, "circle-color": "#1f6f86", "circle-stroke-color": "#f6f1e8", "circle-stroke-width": 2 },
    });

    const clickable = [
      ["rivers-line", "river"],
      ["rivers-major-line", "major"],
      ["waters-fill", "water"],
      ["lakes-fill", "lakes"],
      ["dams-circle", "dam"],
      ["peaks-circle", "peak"],
      ["wilayas-fill", "admin"],
      ["provinces-fill", "provinces"],
      ["adm2-fill", "adm2"],
      ["countries-line", "countries"],
      ["countries-esh", "territory"],
      ["places-circle", "place"],
      ["regions-fill", "regions"],
      ["aquifers-fill", "nappes"],
      ["geology-fill", "bgs"],
      ["roads-line", "roads"],
      ["rail-line", "rail"],
      ["airports-circle", "airports"],
      ["ports-circle", "ports"],
      ["parks-circle", "parks"],
    ];
    clickable.forEach(([id, kind]) => {
      map.on("click", id, (e) => {
        if (e.originalEvent) e.originalEvent._atlasHit = true;
        if (!e.features || !e.features[0]) return;
        selectFeature(e.features[0], kind);
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
    setVisibility(LAYER_IDS[key] || [], on);
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
    const name = (lang === "ar" && p.name_ar) ? p.name_ar
      : (lang === "en" && p.name_en) ? p.name_en
      : (lang === "fr" && p.name_fr) ? p.name_fr
      : (p.name || p.name_en || p.name_fr || "—");
    const fact = lookupFacts([p.name, p.name_ar, p.name_en, p.name_fr].filter(Boolean).join(" "));
    const inspector = document.getElementById("inspector");
    let kicker = t(kind);
    let title = name;
    let chips = [t(kind)];
    let meta = [];
    let note = (lang === "ar" && p.note_ar) ? p.note_ar : (lang === "en" && p.note_en) ? p.note_en : (p.note_fr || p.note || "");
    if (p.country) meta.push([t("country"), p.country]);
    if (p.wilaya) meta.push([t("wilaya"), p.wilaya]);
    if (p.type && kind !== "peak") meta.push([t("type"), p.type]);
    if (p.ele) meta.push([t("elevation"), p.ele + " m"]);
    if (p.pop) meta.push([t("population"), Number(p.pop).toLocaleString(lang === "en" ? "en-GB" : lang === "ar" ? "ar" : "fr-FR")]);
    if (p.iata) meta.push(["IATA", p.iata]);
    if (p.lithology) meta.push([t("lithology"), p.lithology]);
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
      `<button class="btn" ${kind === "river" || kind === "major" ? "" : "disabled"} id="basin-btn">${esc(t("basinBtn"))}</button>`;
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
    const hay = fold([item.label, item.name_ar, item.name_en, item.name_fr, item.extra].filter(Boolean).join(" "));
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
        const label = p.name || p.name_en || p.name_fr || p.name_ar;
        if (!label) return;
        const key = kind + "::" + canonicalize(label);
        if (seen.has(key)) {
          seen.get(key).features.push(f);
          return;
        }
        const item = {
          label,
          name_ar: p.name_ar,
          name_en: p.name_en,
          name_fr: p.name_fr,
          kind,
          feature: f,
          features: [f],
          extra: aliasExtra([label, p.name_ar, p.name_en, p.name_fr].filter(Boolean).join(" ")),
        };
        seen.set(key, item);
        index.push(item);
      });
    };
    [
      ["rivers", "river"],
      ["rivers_major", "major"],
      ["waters", "water"],
      ["lakes", "lakes"],
      ["dams", "dam"],
      ["wilayas", "admin"],
      ["provinces", "provinces"],
      ["countries", "countries"],
      ["adm2", "adm2"],
      ["peaks", "peak"],
      ["places", "place"],
      ["regions", "regions"],
      ["parks", "parks"],
      ["airports", "airports"],
      ["ports", "ports"],
    ].forEach(([key, kind]) => {
      if (DATA[key]) push(DATA[key], kind);
    });
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
      const localized = lang === "ar" ? it.name_ar : lang === "en" ? it.name_en : it.name_fr;
      const display = fact ? (fact.title[lang] || it.label) : (localized || it.label);
      const b = document.createElement("button");
      b.type = "button";
      b.innerHTML = `${esc(display)}<small>${esc(t(it.kind))}</small>`;
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
    const ns = lat >= 0 ? (lang === "ar" ? "ش" : "N") : (lang === "ar" ? "ج" : "S");
    const ew = lng >= 0
      ? (lang === "ar" ? "ق" : "E")
      : (lang === "ar" ? "غ" : lang === "en" ? "W" : "O");
    const fmt = (n) => {
      const text = Math.abs(n).toFixed(2);
      return lang === "en" ? text : text.replace(".", ",");
    };
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
    const pretty = rf.toLocaleString(lang === "ar" ? "ar" : lang === "en" ? "en-GB" : "fr-FR");
    document.getElementById("scale").textContent = `${t("scale")} 1 : ${pretty}`;
  }

  function frameMaghreb() {
    map.fitBounds([[-17.15, 14.65], [25.2, 37.6]], {
      padding: { top: 80, bottom: 56, left: 340, right: 36 },
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
      layers: ["rivers-line", "rivers-major-line", "waters-fill", "lakes-fill", "dams-circle", "peaks-circle", "wilayas-fill", "provinces-fill", "adm2-fill", "countries-line", "countries-esh", "places-circle", "regions-fill", "aquifers-fill", "geology-fill", "roads-line", "rail-line", "airports-circle", "ports-circle", "parks-circle"].filter((id) => map.getLayer(id)),
    });
    if (!hits.length) {
      selected = null;
      document.getElementById("inspector").classList.remove("show");
      if (map.getSource("highlight")) map.getSource("highlight").setData({ type: "FeatureCollection", features: [] });
    }
  });

  async function loadAtlasData() {
    const keys = ["wilayas", "rivers", "waters", "dams", "peaks", "places", "regions", "countries", "provinces", "adm2", "rivers_major", "lakes", "roads", "rail", "airports", "ports", "aquifers", "geology_bgs", "parks"];
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
      frameMaghreb();
      applyI18n();
      updateScale();
    });
  });
})();
