$(function () {
    const $form = $('form#startform');
    const $submit_button = $('button#submit-filter');
    let url;
    let choices = {};

    if ($form.length) {
        // Map choices[] indexes to Choices object
        for (let i = 0; i < window.choices.length; i++) {
            let id = window.choices[i].passedElement.element.id;
            if (id === 'vendor') {
                choices['vendor'] = window.choices[i];
            } else if (id === 'model') {
                choices['model'] = window.choices[i];
            } else if (id === 'year') {
                choices['year'] = window.choices[i];
            } else if (id === 'modification') {
                choices['modification'] = window.choices[i];
            }
        }

        $submit_button.on('click', function () {
            let complete = true;

            // Show dropdown of unselected field
            for (let key in choices) {
                if (choices[key].getValue(true) === '') {
                    choices[key].showDropdown();
                    complete = false;
                    break;
                }
            }
            // Redirect to specified url
            if (complete) {
                // data-redirect-url attribute is more important than generated url
                let attr_url = $form.attr('data-redirect-url');
                if (attr_url)
                    window.location.href = attr_url;
                else
                    window.location.href = url;
            }
        });

        // Attach event listener on select value change
        $form.on('change', '.ajax-filter-trigger', {}, ajax);

        // Set 'No choices text'
        choices['model'].config.noChoicesText = 'Укажите Марку';
        choices['year'].config.noChoicesText = 'Укажите Модель';
        choices['modification'].config.noChoicesText = 'Укажите Год выпуска';

        function ajax(e) {
            const AJAX_URL = $form.attr('data-ajax-url'), METHOD = $form.attr('method');

            // console.log('fired');
            let data = new FormData($form[0]);
            $submit_button.attr('disabled', 'true');
            $.ajax({
                url: AJAX_URL,
                type: METHOD,
                data: data,
                dataType: "json",
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    choices['vendor'].setChoices(data['vendor'], 'value', 'label', true);
                    choices['model'].setChoices(data['model'], 'value', 'label', true);
                    choices['year'].setChoices(data['year'], 'value', 'label', true);
                    choices['modification'].setChoices(data['modification'], 'value', 'label', true);
                    if (data['url'])
                        url = data['url'];
                },
                error: function (data) {
                    console.log("Something went wrong");
                    console.log(data);
                },
                complete: function () {
                    $submit_button.removeAttr('disabled');
                },
            });
        }

        ajax();
    }
});
