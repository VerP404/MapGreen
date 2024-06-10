$(document).ready(function() {
    $('.category-toggle').on('click', function(e) {
        e.preventDefault();
        $(this).next('.type-list').toggle();
    });

    $('.type-filter').on('click', function(e) {
        e.preventDefault();
        var typeId = $(this).data('type-id');
        filterObjectsByType(typeId);
    });

    $('#resetFilters').on('click', function() {
        resetFilters();
    });
});

function createDropIcon(color) {
    return L.divIcon({
        html: `<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 0C9.82 0 4 9.92 4 13.92 4 17.74 7.22 21 12 21s8-3.26 8-7.08C20 9.92 14.18 0 12 0z" 
                      fill="${color}" stroke="#006400" stroke-width="2"/>
               </svg>`,
        className: '',
        iconSize: [24, 24],
        iconAnchor: [12, 24]
    });
}

function filterObjectsByType(typeId) {
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    var filteredObjects = objects.filter(function(obj) {
        return obj.type_object_id == typeId;
    });

    filteredObjects.forEach(function(obj) {
        L.marker([obj.latitude, obj.longitude], {
            icon: createDropIcon(obj.type_object__color)
        }).addTo(map)
        .bindPopup('<b>' + obj.name + '</b><br />' + obj.description);
    });
}

function resetFilters() {
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    objects.forEach(function(obj) {
        L.marker([obj.latitude, obj.longitude], {
            icon: createDropIcon(obj.type_object__color)
        }).addTo(map)
        .bindPopup('<b>' + obj.name + '</b><br />' + obj.description);
    });
}
