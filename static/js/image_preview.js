window.addEventListener('load', () => {
    const insertTooltipHtml = () => {
        const elem = document.createElement('div',);
        elem.id = 'image-preview-tooltip';
        document.body.appendChild(elem);
        return elem;
    }

    let toolTip = insertTooltipHtml();
    let copy = document.querySelector("body");
    let ttImages = document.querySelectorAll("a.image-preview");

    const track = (e) => {
        //  run function on mouse move
        let mouseX = e.clientX + document.body.scrollLeft + 1; //  get x position of mouse
        let mouseY = e.clientY + document.body.scrollTop - 40; //  get y position of mouse
        toolTip.setAttribute("style", "top:" + mouseY + "px; left:" + mouseX + "px;"); //  set the x and y of tooltip based on mouse position
    };
    window.addEventListener("mousemove", track); //  listen for mouse movement

    const showTt = (e) => {
        if (Array.prototype.includes.call(ttImages, e.target)) {
            toolTip.setAttribute("class", "show"); //  show the tooltip
            let ttImage = e.target.href; //  get the data attribute of hovered span
            toolTip.innerHTML = `<img src="${ttImage}" alt="image">`; //  populate the tooltip with an image tag + retrieved data attribute
        } else {
            toolTip.setAttribute("class", ""); //  hide the tooltip
        }
    };
    copy.addEventListener("mouseover", showTt); //  copy hover function

//  preload the images

    let allCities = [];
    let cities = [];

    for (let i = 0; i < ttImages.length; i++) {
        allCities.push(ttImages[i].href);  //  build array of img urls
    }

    for (let i = 0; i < allCities.length; i++) {
        //  loop through the cities array
        cities[i] = new Image();
        cities[i].src = allCities[i];
    }
})
