// static/js/map.js
document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([55.751244, 37.618423], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    map.zoomControl.setPosition('topright');

    L.control.locate({
        position: 'topright',
        strings: {
            title: "Показать мое местоположение"
        },
        locateOptions: {
            maxZoom: 16
        }
    }).addTo(map);

    function createDropIcon(color) {
        return L.divIcon({
            html: `
    <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 0C9.82 0 4 9.92 4 13.92 4 17.74 7.22 21 12 21s8-3.26 8-7.08C20 9.92 14.18 0 12 0z"
              fill="${color}" stroke="#006400" stroke-width="2"/>
    </svg>`,
            className: '',
            iconSize: [24, 24],
            iconAnchor: [12, 24]
        });
    }

    fetch('/api/objects/')
        .then(response => response.json())
        .then(data => {
            data.objects.forEach(obj => {
                const marker = L.marker([obj.latitude, obj.longitude], { icon: createDropIcon(obj.type_object__color) })
                    .bindPopup(`<b>${obj.name}</b><br>${obj.description}`)
                    .addTo(map);
            });
        })
        .catch(error => console.error('Ошибка:', error));

    document.getElementById('btn-toggle').addEventListener('click', function () {
        var navbarTitle = document.querySelector('.navbar-title');
        var navbar = document.querySelector('.navbar');
        if (navbarTitle.style.display === 'none') {
            navbarTitle.style.display = 'flex';
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        } else {
            navbarTitle.style.display = 'none';
            navbar.style.backgroundColor = 'transparent';
        }
    });

    window.myMap = map;
    window.createDropIcon = createDropIcon;
});
