console.log('imported')
window.addEventListener("load", function () {
    (function ($) {
        $('.result_list .action-select').on('click', function () {
            console.log($(this))
            console.log($(this).parent('td').parent('tr'))
            $(this).parent('td').parent('tr').toggleClass('selected');
        })
    })(django.jQuery);
});