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

    var markers = L.markerClusterGroup();

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

    function loadObjects(categoryId = '', typeId = '') {
        let url = `/api/objects/?category=${categoryId}`;
        if (typeId) {
            url += `&type=${typeId}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                markers.clearLayers();

                data.objects.forEach(obj => {
                    if (!obj.id) {
                        console.error('Object ID is undefined:', obj);
                        return;
                    }

                    const marker = L.marker([obj.latitude, obj.longitude], { icon: createDropIcon(obj.type_object__color) })
                        .on('click', function () {
                            $.fancybox.open({
                                src: `/object/${obj.id}/modal/`,
                                type: 'ajax',
                                opts: {
                                    afterShow: function (instance, current) {
                                        console.info('Modal opened for object:', obj.id);
                                    }
                                }
                            });
                        });
                    markers.addLayer(marker);
                });

                map.addLayer(markers);
            })
            .catch(error => console.error('Ошибка:', error));
    }

    document.querySelectorAll('.category-filter').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;
            loadObjects(categoryId);

            const subMenuList = this.closest('.menu-item').querySelector('.sub-menu-list');
            if (subMenuList) {
                subMenuList.style.display = 'block';
            }
        });
    });

    document.querySelectorAll('.type-filter').forEach(button => {
        button.addEventListener('click', function () {
            const typeId = this.dataset.typeId;
            const categoryId = this.closest('.sub-menu').querySelector('.category-filter').dataset.categoryId;
            loadObjects(categoryId, typeId);
        });
    });

    document.getElementById('resetFiltersBtn').addEventListener('click', function () {
        loadObjects('');
    });

    window.myMap = map;
    window.createDropIcon = createDropIcon;

    loadObjects('');
});
