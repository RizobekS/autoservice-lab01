$(function () {
    $('#record-search input[name="search"]').on('keyup', function () {
        $('#tab01').trigger('click');  // Switch to main tab
        let search_value = $(this).val().toLowerCase();
        $('#tab01_pane li').each(function () {
            $(this).css('display', $(this).text().toLowerCase().includes(search_value) ? 'block' : 'none');
        })
    });
});