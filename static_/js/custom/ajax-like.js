$(function () {
    const $like = $('#like');
    $like.on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
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
