$(function () {
    /*
        This script scrolls document to the first element with .scroll-to class found
     */

    let $element = $('.scroll-to').first();
    if ($element.length) {
        if ($element.hasClass('smooth-scroll'))
            $("html, body").animate({scrollTop: $element.offset().top - $element.height()});
        else
            $("html, body").scrollTop($element.offset().top - $element.height());
    }
});