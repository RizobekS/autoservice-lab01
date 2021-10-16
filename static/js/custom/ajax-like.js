$(function () {
    const $like = $('#like');
    $like.on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).data('ajax-url'),
            type: 'GET',
            cache: false,
            contentType: 'html',
            processData: false,
            success: function (data) {
                $like.html(data);
            },
            error: function (data) {
                console.log('err', data);
            }
        });
    })
});
