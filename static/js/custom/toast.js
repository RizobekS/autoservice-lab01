function launch_toast() {
    var x = document.getElementById("appointment-toast")
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 5000);
}
