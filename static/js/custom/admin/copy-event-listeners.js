window.addEventListener("load", function () {
    (function ($) {
        $('.result_list .action-select').on('click', function () {
            $(this).parent('td').parent('tr').toggleClass('selected');
        })
    })(django.jQuery);
});