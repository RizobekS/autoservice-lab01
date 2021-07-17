$(function () {
    const $form = $('form#search');
    const AJAX_URL = $form.attr('action'), METHOD = $form.attr('method')

    $('form.searchform, form.search-form').on('submit', function (e) {

        e.preventDefault();
        // var $form = $(this);
        var $searchModal = $('#search_modal');
        $searchModal.find('div.searchform-respond').remove();

        //checking on empty values
        $($form).find('[type="text"], [type="search"]').each(function (index) {
            var $thisField = $(this);
            if (!$thisField.val().length) {
                $thisField
                    .addClass('invalid')
                    .on('focus', function () {
                        $thisField.removeClass('invalid')
                    });
            }
        });
        //if one of form fields is empty - exit
        if ($form.find('[type="text"]').hasClass('invalid')) {
            return;
        }

        $searchModal.modal('show');
        //sending form data to PHP server if fields are not empty
        var request = $form.serialize();
        var ajax = jQuery.get(AJAX_URL, request)
            .done(function (data) {
                $searchModal.append('<div class="searchform-respond">' + data + '</div>');
            })
            .fail(function (data) {
                $searchModal.append('<div class="searchform-respond">Что-то пошло не так...</div>');
            })
    });
})
