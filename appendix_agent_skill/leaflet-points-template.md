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

> "Using the points data already retrieved, build a Leaflet map artifact. Color the markers by code. Show a popup on click with point_id, code, station, and phase. Auto-fit the bounds."

If you want to filter first — for example, only weld points — say so before asking for the map:

> "Filter to WLD points only, then build the Leaflet map."

---

## The template

This is the complete artifact template. Your agent can use it directly or adapt it. The `POINTS` constant is a placeholder — replace it with the actual API response.

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<div style="padding: 1rem 0 0.5rem;">
  <div id="map" style="height: 420px; border-radius: 12px; border: 0.5px solid #ccc; overflow: hidden;"></div>
  <p id="status" style="font-size: 13px; color: #888; margin: 8px 0 0; text-align: right;"></p>
</div>

<script>
const POINTS = []; /* replace with API response */

const CODE_COLORS = {
  'WLD':  '#185FA5',
  'BND':  '#3B6D11',
  'CAS':  '#BA7517',
  'TIE':  '#A32D2D',
};
const DEFAULT_COLOR = '#5F5E5A';

function colorFor(code) {
  return CODE_COLORS[code] || DEFAULT_COLOR;
}

function markerFor(code) {
  const color = colorFor(code);
  return L.divIcon({
    className: '',
    html: `<div style="width:10px;height:10px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3);"></div>`,
    iconSize: [10, 10],
    iconAnchor: [5, 5],
  });
}

function renderMap(points) {
  if (!points.length) {
    document.getElementById('status').textContent = 'No points with coordinates.';
    return;
  }

  const lats = points.map(p => p.latitude);
  const lngs = points.map(p => p.longitude);
  const center = [
    (Math.min(...lats) + Math.max(...lats)) / 2,
    (Math.min(...lngs) + Math.max(...lngs)) / 2,
  ];

  const map = L.map('map').setView(center, 14);

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

  const bounds = L.latLngBounds(points.map(p => [p.latitude, p.longitude]));
  map.fitBounds(bounds, { padding: [32, 32] });

  const codeCounts = {};
  points.forEach(p => { codeCounts[p.code] = (codeCounts[p.code] || 0) + 1; });
  const summary = Object.entries(codeCounts).map(([c, n]) => `${c}: ${n}`).join(' · ');
  document.getElementById('status').textContent = `${points.length} points — ${summary}`;
}

renderMap(POINTS.filter(p => p.latitude != null && p.longitude != null));
</script>
```

---

## Customizing the color map

The `CODE_COLORS` object maps code strings to hex colors. Edit it to match your project's codes. Points with codes not in the map render in gray. Your agent can auto-populate this from the held code rules:

> "Build the Leaflet map and generate a CODE_COLORS entry for every on-line code in this project."

---

## Limitations

- This is a visual check, not a GIS export. For spatial analysis, use the KMZ or shapefile downloads.
- Large projects (thousands of points) will render slowly in a browser artifact. Filter to a phase or a code subset if performance is an issue.
- The map uses OpenStreetMap tiles. It requires an internet connection in the artifact's execution environment.
