# Atlas géographique du Maghreb

Geographic atlas of the Maghreb: Morocco, Algeria, Tunisia, Libya, Mauritania, and Western Sahara, shown as a separate geographic unit because its status is disputed.

The interface is in French, English, and Arabic.

Live site: https://merabah.github.io/atlas-geographique-algerie/

## Run locally

```bash
python3 server.py
```

Then open http://127.0.0.1:8765

`server.py` reads `public/`. The same static files are also at the repository root so GitHub Pages can serve them from `/`.

## Layers

Countries, Algerian wilayas, provinces and regions, second-level divisions for Morocco, Tunisia and Mauritania, physical regions, rivers and wadis, major rivers, lakes and chotts, dams, summits, place names, national parks, main roads, railways, airports, ports, surface geology, and aquifers.

Shaded relief and the terrain model use remote tiles. The INCT topographic sheet and the detailed ASGA / BNDG geological map stay unavailable because they are not open data. Full Maghreb contours are not included because of size. HydroBASINS is not republished because its licence restricts redistribution.

## Data

Open data for this atlas:

- SRTM / terrain tiles (Esri shaded relief, Terrarium elevation)
- OpenStreetMap rivers, water bodies, dams, and summits (ODbL)
- Natural Earth 10m countries, regions, major rivers, roads, railways, airports, and ports (public domain)
- geoBoundaries administrative divisions (ODbL)
- British Geological Survey / Africa Groundwater Atlas country hydrogeology maps, simplified (CC BY-SA 4.0)

INCT and ANRH remain the Algerian national references. The national parks layer is a short list of well-known parks with approximate locations, not a copy of the World Database on Protected Areas.
