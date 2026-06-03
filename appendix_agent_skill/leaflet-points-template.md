# Leaflet Points Map Template

The `json-points/` response includes `latitude` and `longitude` on every point dict. This template renders them in an interactive Leaflet map as a Claude artifact.

---

## When to use this

Use it when you want a quick visual check of where points actually fell — alignment coverage, phase distribution, or just a sanity check before exporting. It is not a GIS tool. It is a map.

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

Once you have the point data in hand, paste this prompt to your agent:

> "Using the points data already retrieved, build a Leaflet map artifact. Color the markers by code. Show a popup on click with point_id, code, station, and phase. Auto-fit the bounds. Show a color legend below the map."

If you want to filter first — for example, only on-line points — say so before asking for the map:

> "Filter to on-line codes only, then build the Leaflet map."

---

## The template

This is the complete artifact template. Your agent can use it directly or adapt it. The `POINTS` constant is a placeholder — replace it with the actual API response.

`CODE_COLORS` should be populated from the project's actual on-line codes. The agent can do this automatically from the held code rules (see prompt below). The defaults shown cover common on-line codes — any code not in the map renders gray.

**Note on rendering:** The map tile background does not render inside the Claude chat artifact sandbox, but is visible when the artifact is downloaded as an HTML file. This is expected behavior — the map controls, markers, and popups all work normally in both contexts.

```html
<!DOCTYPE html>
<html style="height:100%;margin:0;">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
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
const POINTS = []; /* replace with API response */

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

function colorFor(code) {
  return CODE_COLORS[code] || DEFAULT_COLOR;
}

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
  if (!points.length) {
    document.getElementById('legend').textContent = 'No points with coordinates.';
    return;
  }

  const map = L.map('map');

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map);

  points.forEach(p => {
    L.marker([p.latitude, p.longitude], { icon: markerFor(p.code) })
      .bindPopup(`
        <strong>${p.point_id}</strong><br>
        Code: ${p.code}<br>
        Station: ${p.raw_station || '—'}<br>
        Phase: ${p.phase || '—'}
      `)
      .addTo(map);
  });

  map.fitBounds(L.latLngBounds(points.map(p => [p.latitude, p.longitude])), { padding: [32, 32] });

  const codeCounts = {};
  points.forEach(p => { codeCounts[p.code] = (codeCounts[p.code] || 0) + 1; });
  const legend = document.getElementById('legend');
  Object.entries(CODE_COLORS)
    .filter(([c]) => codeCounts[c])
    .forEach(([c, col]) => {
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

`CODE_COLORS` maps code strings to hex colors. Edit it to match your project's on-line codes. The agent can auto-populate it from the held code rules:

> "Build the Leaflet map and generate a CODE_COLORS entry for every on-line code in this project."

---

## Limitations

- This is a visual check, not a GIS export. For spatial analysis, use the KMZ or shapefile downloads.
- Large projects (thousands of points) will render slowly in a browser artifact. Filter to on-line codes or a single phase if performance is an issue.
- The map uses OpenStreetMap tiles. It requires an internet connection in the artifact's execution environment.
