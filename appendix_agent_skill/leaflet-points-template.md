# Leaflet Points Map Template

The `json-points/` response includes `latitude` and `longitude` on every point dict. This template builds an interactive Leaflet map as a downloadable HTML file.

---

## How this works

The agent fetches your point data, inlines it into a standalone HTML file, and offers it as a download. You open the file in any browser — no server, no login, no connection to your platform required beyond the initial fetch.

**The map does not render as a chat artifact.** The Claude chat sandbox blocks external CDN scripts, so Leaflet cannot load inline. The download is the deliverable.

---

## The API call

```python
import requests
data = {
    'username': '<username>',
    'password': '<password>',
    'project_alias': '<alias>'
}
response = requests.post('https://<server_name>/points/json-points/', data=data)
points = response.json()
```

Each point dict includes `latitude` and `longitude` alongside the standard fields.

---

## What to tell your agent

```
Using the points already retrieved, build a Leaflet map as a downloadable HTML file.
Filter to on-line codes only. Color markers by code. Popup on click: point_id, code,
station, phase. Auto-fit bounds. Color legend at the bottom. Full dataset — no sampling.
```

The agent will produce a file ready to open in a browser. A project with 1,500+ on-line points generates and downloads in seconds; browser load time is fast.

---

## The template

The agent uses this as its starting point. `POINTS` is replaced with the actual filtered API response. `CODE_COLORS` should be populated from the project's on-line codes — the agent can derive these from the held code rules.

```html
<!DOCTYPE html>
<html style="height:100%;margin:0;">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><!-- project title --></title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    html, body { height: 100%; margin: 0; padding: 0; font-family: sans-serif; }
    #map { position: absolute; top: 0; left: 0; right: 0; bottom: 28px; }
    #legend { position: absolute; bottom: 0; left: 0; right: 0; height: 24px; padding: 4px 8px; font-size: 12px; color: #666; display: flex; align-items: center; gap: 12px; background: #fff; border-top: 0.5px solid #ddd; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="legend"></div>

<script>
const POINTS = []; /* replaced with filtered API response */

const CODE_COLORS = {
  'WELD': '#185FA5',
  'WLD':  '#185FA5',
  'BND':  '#3B6D11',
  'LE':   '#A32D2D',
  'FLN':  '#BA7517',
  'TEE':  '#533AB9',
  'VLV':  '#0F6E56',
};
const DEFAULT_COLOR = '#5F5E5A';

function colorFor(code) { return CODE_COLORS[code] || DEFAULT_COLOR; }

function markerFor(code) {
  const color = colorFor(code);
  return L.divIcon({
    className: '',
    html: `<div style="width:9px;height:9px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3);"></div>`,
    iconSize: [9, 9],
    iconAnchor: [4, 4],
  });
}

function renderMap(points) {
  if (!points.length) { document.getElementById('legend').textContent = 'No points.'; return; }

  const map = L.map('map');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map);

  points.forEach(p => {
    L.marker([p.latitude, p.longitude], { icon: markerFor(p.code) })
      .bindPopup(`<strong>${p.point_id}</strong><br>Code: ${p.code}<br>Station: ${p.raw_station || '—'}<br>Phase: ${p.phase || '—'}`)
      .addTo(map);
  });

  map.fitBounds(L.latLngBounds(points.map(p => [p.latitude, p.longitude])), { padding: [32, 32] });

  const codeCounts = {};
  points.forEach(p => { codeCounts[p.code] = (codeCounts[p.code] || 0) + 1; });
  const legend = document.getElementById('legend');
  Object.entries(CODE_COLORS).filter(([c]) => codeCounts[c]).forEach(([c, col]) => {
    const span = document.createElement('span');
    span.style.cssText = 'display:inline-flex;align-items:center;gap:4px;';
    span.innerHTML = `<span style="width:8px;height:8px;border-radius:50%;background:${col};display:inline-block;"></span>${c}: ${codeCounts[c]}`;
    legend.appendChild(span);
  });
}

renderMap(POINTS.filter(p => p.latitude != null && p.longitude != null));
</script>
</body>
</html>
```

---

## Customizing the color map

`CODE_COLORS` maps code strings to hex colors. The agent can auto-populate it from the held code rules:

> "Build the Leaflet map and generate a CODE_COLORS entry for every on-line code in this project."

Any code not in the map renders gray.

---

## Limitations

- This is a visual check, not a GIS export. For spatial analysis, use the KMZ or shapefile downloads.
- Requires an internet connection when opened in a browser (for OpenStreetMap tiles).
- The file is self-contained otherwise — the point data is inlined, no platform connection needed after download.
