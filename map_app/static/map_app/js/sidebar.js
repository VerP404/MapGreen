// static/js/sidebar.js
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

function filterObjectsByType(typeId) {
    map.eachLayer(function(layer) {
        if (layer instanceof L.CircleMarker) {
            map.removeLayer(layer);
        }
    });

    var filteredObjects = objects.filter(function(obj) {
        return obj.type_object_id == typeId;
    });

    filteredObjects.forEach(function(obj) {
        L.circleMarker([obj.latitude, obj.longitude], {
            radius: 9,
            fillColor: obj.type_object__color,
            color: '#003153',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map)
        .bindPopup('<b>' + obj.name + '</b><br />' + obj.description);
    });
}

function resetFilters() {
    map.eachLayer(function(layer) {
        if (layer instanceof L.CircleMarker) {
            map.removeLayer(layer);
        }
    });

    objects.forEach(function(obj) {
        L.circleMarker([obj.latitude, obj.longitude], {
            radius: 9,
            fillColor: obj.type_object__color,
            color: '#003153',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map)
        .bindPopup('<b>' + obj.name + '</b><br />' + obj.description);
    });
}
