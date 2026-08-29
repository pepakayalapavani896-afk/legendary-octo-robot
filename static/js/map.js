/**
 * GramSetu — Interactive Problem Map & Geospatial Hotspot Engine
 * Built with Leaflet.js and real GPS coordinate clustering
 */

let MAP_INSTANCE = null;
let MARKERS_LAYER = null;
let HOTSPOTS_LAYER = null;
let ALL_MAP_COMPLAINTS = [];

async function initProblemMap() {
  const container = document.getElementById("problemMapContainer");
  if (!container) return;

  if (!MAP_INSTANCE) {
    // Default center (Hyderabad coordinates or fallback, adjusted dynamically)
    MAP_INSTANCE = L.map("problemMapContainer").setView([17.385044, 78.486671], 14);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(MAP_INSTANCE);

    MARKERS_LAYER = L.layerGroup().addTo(MAP_INSTANCE);
    HOTSPOTS_LAYER = L.layerGroup().addTo(MAP_INSTANCE);
  }

  await loadMapData();
}

async function loadMapData() {
  try {
    const res = await fetch("/api/map/complaints");
    const data = await res.json();

    if (data.success) {
      ALL_MAP_COMPLAINTS = data.complaints || [];
      renderHotspotBanners(data.hotspots, data.repeated_resources);
      renderMapMarkers(ALL_MAP_COMPLAINTS);
      renderHotspotCircles(data.hotspots);

      // Fit bounds if complaints exist
      if (ALL_MAP_COMPLAINTS.length > 0 && MARKERS_LAYER) {
        const group = L.featureGroup(MARKERS_LAYER.getLayers());
        if (group.getLayers().length > 0) {
          MAP_INSTANCE.fitBounds(group.getBounds().pad(0.15));
        }
      }
    }
  } catch (err) {
    console.error("Failed to load map data:", err);
  }
}

function renderMapMarkers(complaints) {
  if (!MARKERS_LAYER) return;
  MARKERS_LAYER.clearLayers();

  const catFilter = document.getElementById("mapCategoryFilter") ? document.getElementById("mapCategoryFilter").value : "all";
  const statusFilter = document.getElementById("mapStatusFilter") ? document.getElementById("mapStatusFilter").value : "all";

  complaints.forEach(c => {
    if (catFilter !== "all" && c.category !== catFilter) return;
    if (statusFilter !== "all" && c.status !== statusFilter) return;

    const lat = parseFloat(c.latitude);
    const lon = parseFloat(c.longitude);
    if (isNaN(lat) || isNaN(lon)) return;

    // Custom colored pin SVG
    let pinColor = "#10B981"; // Low (Green)
    if (c.priority === "HIGH") pinColor = "#EF4444"; // High (Red)
    else if (c.priority === "MEDIUM") pinColor = "#F59E0B"; // Medium (Orange)

    const iconHtml = `
      <div style="
        background: ${pinColor}; 
        width: 28px; 
        height: 28px; 
        border-radius: 50% 50% 50% 0; 
        transform: rotate(-45deg); 
        border: 2.5px solid #FFFFFF; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <div style="width: 8px; height: 8px; background: #FFFFFF; border-radius: 50%;"></div>
      </div>
    `;

    const customIcon = L.divIcon({
      html: iconHtml,
      className: "custom-leaflet-pin",
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -28]
    });

    const marker = L.marker([lat, lon], { icon: customIcon });

    // Popup with exact photo integrity
    let photoHtml = "";
    if (c.image_url) {
      photoHtml = `
        <div style="margin-top: 6px; border-radius: 6px; overflow: hidden; max-height: 120px;">
          <img src="${c.image_url}" style="width: 100%; height: 100px; object-fit: cover;" alt="Complaint Photo">
        </div>
      `;
    } else if (c.is_demo) {
      photoHtml = `<div style="margin-top: 4px; font-size: 0.7rem; color: #64748B; font-weight: bold;">[DEMO DATA - PROTOTYPE]</div>`;
    } else {
      photoHtml = `<div style="margin-top: 4px; font-size: 0.72rem; color: #94A3B8; font-style: italic;">No photo evidence submitted.</div>`;
    }

    const popupContent = `
      <div style="min-width: 200px; font-family: sans-serif;">
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 4px;">
          <strong style="color: #0B2239; font-size: 0.88rem;">${c.complaint_id}</strong>
          <span style="font-size: 0.7rem; padding: 2px 6px; border-radius: 99px; background: ${pinColor}; color: #FFFFFF; font-weight: bold;">${c.priority}</span>
        </div>
        <div style="font-weight: 700; color: #1E3A8A; font-size: 0.85rem; margin-bottom: 2px;">${c.category}</div>
        <div style="font-size: 0.75rem; color: #475569; margin-bottom: 4px;">📍 ${c.location_name}</div>
        <div style="font-size: 0.75rem; color: #059669; font-weight: bold;">Status: ${c.status}</div>
        ${photoHtml}
      </div>
    `;

    marker.bindPopup(popupContent);
    MARKERS_LAYER.addLayer(marker);
  });
}

function renderHotspotCircles(hotspots) {
  if (!HOTSPOTS_LAYER) return;
  HOTSPOTS_LAYER.clearLayers();

  if (!hotspots || hotspots.length === 0) return;

  hotspots.forEach(hs => {
    const circle = L.circle([hs.latitude, hs.longitude], {
      color: "#DC2626",
      fillColor: "#EF4444",
      fillOpacity: 0.22,
      radius: hs.radius_meters,
      weight: 2,
      dashArray: "6, 6"
    });

    circle.bindPopup(`
      <div style="min-width: 220px;">
        <div style="font-weight: 800; color: #991B1B; font-size: 0.92rem; margin-bottom: 4px;">
          🚨 ${hs.alert_title}
        </div>
        <div style="font-size: 0.8rem; color: #374151; margin-bottom: 4px;">
          ${hs.recommendation}
        </div>
        <div style="font-size: 0.75rem; color: #6B7280;">
          Cluster ID: ${hs.hotspot_id} | Radius: ${hs.radius_meters}m
        </div>
      </div>
    `);

    HOTSPOTS_LAYER.addLayer(circle);
  });
}

function renderHotspotBanners(hotspots, repeated) {
  const container = document.getElementById("mapAlertsContainer");
  if (!container) return;

  let html = "";

  if (hotspots && hotspots.length > 0) {
    hotspots.forEach(hs => {
      html += `
        <div class="hotspot-banner">
          <div style="font-size: 1.6rem;">🚨</div>
          <div>
            <h4>${hs.alert_title}</h4>
            <p>${hs.recommendation} <strong>(Area: ${hs.location_name})</strong></p>
          </div>
        </div>
      `;
    });
  }

  if (repeated && repeated.length > 0) {
    repeated.forEach(rep => {
      html += `
        <div class="hotspot-banner" style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-color: #FCD34D;">
          <div style="font-size: 1.6rem;">⚡</div>
          <div>
            <h4 style="color: #92400E;">${rep.message}</h4>
            <p style="color: #78350F;">Complaints Count: <strong>${rep.count}</strong> on same ${rep.category} infrastructure.</p>
          </div>
        </div>
      `;
    });
  }

  container.innerHTML = html;
}

function filterMapLayers() {
  renderMapMarkers(ALL_MAP_COMPLAINTS);
}
