document.addEventListener('DOMContentLoaded', function () {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    const defaultCenter = [20.5937, 78.9629];
    const map = L.map('map').setView(defaultCenter, 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    let marker;

    map.on('click', function (event) {
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker(event.latlng).addTo(map);
        reverseGeocode(event.latlng);
    });

    setTimeout(function () {
        map.invalidateSize();
    }, 200);

    function reverseGeocode(latlng) {
        const locationInput = document.querySelector('input[name="location_name"]');
        if (!locationInput) return;

        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`;
        fetch(url, {
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                const address = data.address;
                const place = data.display_name || '';
                const nameParts = [];
                if (address.road) nameParts.push(address.road);
                if (address.neighbourhood) nameParts.push(address.neighbourhood);
                if (address.suburb) nameParts.push(address.suburb);
                if (address.city) nameParts.push(address.city);
                if (address.state) nameParts.push(address.state);
                if (nameParts.length === 0 && place) {
                    locationInput.value = place;
                } else if (nameParts.length > 0) {
                    locationInput.value = nameParts.join(', ');
                } else {
                    locationInput.value = 'Selected location';
                }
            })
            .catch(() => {
                locationInput.value = 'Selected location';
            });
    }
});

const chartCanvas = document.getElementById('reportsChart');
if (chartCanvas) {
    const initializeChart = () => {
        if (typeof Chart === 'undefined') return;
        const ctx = chartCanvas.getContext('2d');
        const labels = typeof reportChartLabels !== 'undefined' ? reportChartLabels : ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'];
        const data = typeof reportChartData !== 'undefined' ? reportChartData : [24, 30, 22, 28, 35, 32];
        const chartType = typeof reportChartType !== 'undefined' ? reportChartType : 'line';
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    label: 'Issue Reports',
                    data: data,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff',
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#fff',
                        titleColor: '#0f172a',
                        bodyColor: '#0f172a',
                        borderColor: 'rgba(148, 163, 184, 0.3)',
                        borderWidth: 1,
                        boxPadding: 8
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b' },
                        border: { color: 'rgba(148, 163, 184, 0.2)' }
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.18)' },
                        ticks: { color: '#64748b', stepSize: 1 },
                        border: { color: 'rgba(148, 163, 184, 0.2)' }
                    }
                }
            }
        });
    };

    if (typeof Chart !== 'undefined') {
        initializeChart();
    } else {
        const scriptObserver = new MutationObserver(() => {
            if (typeof Chart !== 'undefined') {
                initializeChart();
                scriptObserver.disconnect();
            }
        });
        scriptObserver.observe(document, { childList: true, subtree: true });
    }
}
