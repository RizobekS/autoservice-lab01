$(function () {
    const searchFormSelector = 'form.searchform, form.search-form, form.search-popup__form';

    function getResultsContainer($form) {
        const $searchPopup = $form.closest('.search-popup');

        if ($searchPopup.length) {
            return $searchPopup.find('.search-popup__results');
        }

        const $searchModal = $('#search_modal');
        $searchModal.find('div.searchform-respond').remove();
        $searchModal.append('<div class="searchform-respond"></div>');
        return $searchModal.find('div.searchform-respond');
    }

    function getSearchField($form) {
        return $form.find('[type="text"], [type="search"]').first();
    }

    $(document).on('submit', searchFormSelector, function (e) {
        e.preventDefault();

        const $form = $(this);
        const $searchField = getSearchField($form);
        const $results = getResultsContainer($form);
        const ajaxUrl = $form.attr('action');

        $results.empty();
        $searchField.removeClass('invalid');

        if (!$searchField.val().trim().length) {
            $searchField
                .addClass('invalid')
                .one('focus', function () {
                    $searchField.removeClass('invalid');
                });
            return;
        }

        if (!$form.closest('.search-popup').length) {
            $('#search_modal').modal('show');
        }

        $.get(ajaxUrl, $form.serialize())
            .done(function (data) {
                $results.html(data);
            })
            .fail(function () {
                $results.html('<p class="mb-0 text-heading">Что-то пошло не так...</p>');
            });
    });
});
