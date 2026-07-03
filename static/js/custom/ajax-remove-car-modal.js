$(function () {
    const $counter = $('#garage_counter');
    const $items = $('.garage_modal_item');

    $('.shop-item .remove').on('click', function () {
        let url = $(this).attr('href');
        $.ajax({
            url: url,
            type: 'GET',
            cache: false,
            contentType: false,
            processData: false,
            success: function () {
                console.log('Successfully deleted!');
                reload_list();
            },
            error: function () {
                window.location.reload();
            },
        });
    });

    function reload_list() {
        let counter = 0;
        $items.each(function () {
            if (counter >= 3) {
                $(this).css('display', 'none');
            }
            counter++;
        });
        $counter.text(counter);
    }

    reload_list();
});
