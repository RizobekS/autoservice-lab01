$(function () {
    $('.product-remove .remove').on('click', function () {
        let url = $(this).attr('href');
        $.ajax({
            url: url,
            type: 'GET',
            cache: false,
            contentType: false,
            processData: false,
            success: function () {
                console.log('Successfully deleted!');
            },
            error: function () {
                window.location.reload();
            },
        });
    })
});
