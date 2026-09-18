document.addEventListener('DOMContentLoaded', function () {
    const mapContainer = document.getElementById('properties-map');
    if (mapContainer) {
        initPropertiesMap(mapContainer);
    }

    const detailMap = document.getElementById('detail-map');
    if (detailMap) {
        initDetailMap(detailMap);
    }
});

function priceIcon(rent) {
    const label = rent >= 1000 ? Math.round(rent / 1000) + 'K' : rent;
    return L.divIcon({
        className: 'price-marker',
        html: `<div class="price-bubble">${label}</div>`,
        iconSize: [50, 30],
    });
}

function initPropertiesMap(container) {
    // Default center: Dharan, Nepal
    const map = L.map(container).setView([26.8125, 87.2833], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
    }).addTo(map);

    const dataUrl = container.dataset.propertiesUrl;
    fetch(dataUrl)
        .then((res) => res.json())
        .then((data) => {
            const markers = [];
            data.properties.forEach((p) => {
                const marker = L.marker([p.lat, p.lng], { icon: priceIcon(p.rent) }).addTo(map);
                marker.bindPopup(
                    `<strong>${p.title}</strong><br>Rs. ${p.rent}/month<br><a href="${p.url}">View Details</a>`
                );
                markers.push(marker);
            });
            if (markers.length) {
                const group = L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.2));
            }
        })
        .catch((err) => console.error('Failed to load map data:', err));
}

function initDetailMap(container) {
    const lat = parseFloat(container.dataset.lat);
    const lng = parseFloat(container.dataset.lng);

    const map = L.map(container).setView([lat, lng], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
    }).addTo(map);

    L.marker([lat, lng]).addTo(map);
}
