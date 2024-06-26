document.addEventListener('DOMContentLoaded', function () {
    const addObjectBtn = document.getElementById('addObjectBtn');
    const objectFormModal = document.getElementById('objectFormModal');
    const selectPointMessage = document.getElementById('selectPointMessage');
    const confirmSelectionMessage = document.getElementById('confirmSelectionMessage');
    const successMessage = document.getElementById('successMessage');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const closeFormModalBtn = document.getElementById('closeFormModalBtn');
    const categorySelect = document.getElementById('category');
    const typeObjectSelect = document.getElementById('type_object');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    let marker;

    function showModal(modal) {
        modal.style.display = 'block';
    }

    function hideModal(modal) {
        modal.style.display = 'none';
    }

    function loadImage(event, id) {
        const input = event.target;
        const reader = new FileReader();
        reader.onload = function () {
            const imageContainer = document.getElementById(id);
            const imgElement = document.createElement('img');
            imgElement.src = reader.result;
            imgElement.style.width = '100%';
            imgElement.style.height = '100%';
            imgElement.style.objectFit = 'cover';
            imageContainer.innerHTML = '';
            imageContainer.appendChild(imgElement);
            const deleteIcon = document.createElement('span');
            deleteIcon.className = 'delete-icon';
            deleteIcon.innerHTML = '&times;';
            deleteIcon.onclick = function () {
                removeImage(id);
            };
            imageContainer.appendChild(deleteIcon);
        };
        reader.readAsDataURL(input.files[0]);
    }

    function removeImage(id) {
        const imageContainer = document.getElementById(id);
        imageContainer.innerHTML = '<input type="file" accept="image/*" onchange="loadImage(event, \'' + id + '\')">' +
                                   '<span class="delete-icon" onclick="removeImage(\'' + id + '\')">&times;</span>';
    }

    if (addObjectBtn) {
        addObjectBtn.addEventListener('click', function () {
            selectPointMessage.style.display = 'block';
            document.getElementById('map').style.cursor = 'crosshair';
        });
    }

    if (closeFormModalBtn) {
        closeFormModalBtn.addEventListener('click', function () {
            hideModal(objectFormModal);
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            confirmSelectionMessage.style.display = 'none';
            showModal(objectFormModal);
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            confirmSelectionMessage.style.display = 'none';
            if (marker) {
                map.removeLayer(marker);
                marker = null;
            }
            document.getElementById('map').style.cursor = '';
        });
    }

    const map = window.myMap;
    const createDropIcon = window.createDropIcon;

    if (map) {
        map.on('click', function (e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;

            if (marker) {
                map.removeLayer(marker);
            }

            marker = L.marker([lat, lng], {icon: createDropIcon('#FF0000')}).addTo(map);

            latitudeInput.value = lat;
            longitudeInput.value = lng;

            selectPointMessage.style.display = 'none';
            confirmSelectionMessage.style.display = 'block';
            document.getElementById('map').style.cursor = '';
        });
    }

    categorySelect.addEventListener('change', function () {
        const categoryId = this.value;
        typeObjectSelect.innerHTML = '<option value="">Выберите тип объекта</option>';

        if (categoryId) {
            fetch(`/api/type_objects/${categoryId}/`)
                .then(response => response.json())
                .then(data => {
                    data.type_objects.forEach(typeObject => {
                        const option = document.createElement('option');
                        option.value = typeObject.id;
                        option.textContent = typeObject.name;
                        typeObjectSelect.appendChild(option);
                    });
                });
        }
    });

    document.getElementById('objectForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    hideModal(objectFormModal);
                    successMessage.style.display = 'block';
                    setTimeout(() => {
                        successMessage.style.display = 'none';
                    }, 3000);
                } else {
                    console.log(data.errors);
                }
            })
            .catch(error => console.error('Ошибка:', error));
    });
});

// Attach the loadImage function to window so it can be called from inline event handlers
window.loadImage = loadImage;
window.removeImage = removeImage;
