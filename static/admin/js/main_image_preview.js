window.addEventListener('load', () => {
    const getSelectedLink = () => {
        return selectElem.options[selectElem.selectedIndex].text;
    }

    const selectElem = document.getElementById('id_main_image');
    const image = document.createElement('img');

    if (!selectElem) {
        return;
    }

    image.classList.add('main_image_preview');
    selectElem.parentNode.insertBefore(image, selectElem.nextSibling);

    image.src = '/media/' + getSelectedLink();

    selectElem.addEventListener('change', () => {
        image.src = '/media/' + getSelectedLink();
    });
})
