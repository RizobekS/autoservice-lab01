$(function () {
    const $works = $('div.work');
    $works.on('click', function (e) {
        e.stopPropagation();
        window.location = $(this).attr('data-url');
    })
});