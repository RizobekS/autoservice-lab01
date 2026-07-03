$(function () {
    // Find all available letters an mark them as available
    let letters = new Set();
    $('.tab-pane li').each(function () {
        letters.add($(this).text()[0].toUpperCase());
    });
    $('#calendar_wrap td').each(function () {
        if (letters.has($(this).text().toUpperCase())) {
            let letter = $(this).text();
            $(this).addClass('available');
            $(this).html(`<a href="#" aria-label="Записи на букву ${letter}">${letter}</a>`);
        }
    })

    // Handle filtering on click
    const $availables = $('#calendar_wrap td.available');
    let $current_selected = null;
    $availables.on('click', function (e) {
        e.preventDefault();
        let letter = $(this).children('a').text().toUpperCase();
        $current_selected = $(this);
        $('.tab-pane li').each(function () {
            $(this).css('display', $(this).text().toUpperCase().startsWith(letter) ? 'block' : 'none');
        });
        $('#calendar_wrap caption').text(`Статьи на букву "${letter}"`);
    });


    // Handle selecting next
    $('#calendar_wrap #next').on('click', function (e) {
        e.preventDefault();
        if ($current_selected) {
            let current_index = $availables.index($current_selected);
            $availables[++current_index % $availables.length].click();
        } else {
            $availables.first().trigger('click');
        }
    });

    // Handle selecting previous
    $('#calendar_wrap #prev').on('click', function (e) {
        e.preventDefault();
        if ($current_selected) {
            let current_index = $availables.index($current_selected);
            let new_index = current_index === 0 ? $availables.length - 1 : current_index - 1;
            $availables[new_index].click();
        } else {
            $availables.last().trigger('click');
        }
    });


    // Handle filter clearing
    $('#clear-filter').on('click', function (e) {
        e.preventDefault();
        $('.tab-pane li').css('display', 'block');
        $('#calendar_wrap caption').text('Все записи');
    });
});