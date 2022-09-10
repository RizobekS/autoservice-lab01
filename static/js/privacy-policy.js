"use strict";

$('.privacy-policy .privacy-policy-trigger').on('click', function (e) {
    let $modalBody = $('#modalPrivacyPolicy .modal-body');

    if ($modalBody.attr('data-content-loaded') === 'false') {
        const url = $modalBody.attr('data-content-url');
        console.log('fetching privacy policy...');
        fetch(url).then(response => {
            response.text().then(html => {
                $modalBody.html(html);
                $modalBody.attr('data-content-loaded', 'true');
            })
        });
    }
})
