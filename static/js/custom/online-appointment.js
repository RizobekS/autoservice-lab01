(function ($) {
    const formSelector = '#online-appointment-form, #home-appointment-form';

    function showToast() {
        if (typeof launch_toast === 'function') {
            launch_toast();
            return;
        }

        if (typeof toastMessage === 'function') {
            toastMessage(
                'success',
                'Success',
                'Заявка успешно отправлена!',
                'fa-solid fa-circle-check'
            );
        }
    }

    function getFieldContainer($field) {
        const $group = $field.closest('.form-group, .col-sm-6, .col-sm-12, .col-11, .col-12');
        return $group.length ? $group : $field.parent();
    }

    function clearErrors($form) {
        $form.find('small.text-warning.js-ajax-field-error').remove();
    }

    function clearForm($form, data) {
        $form.find('input, textarea').not('[type="hidden"], [name="csrfmiddlewaretoken"]').val('');
        $form.find('select').prop('selectedIndex', 0);

        if (data.full_name) {
            $form.find('[name="full_name"]').val(data.full_name);
        }

        if (data.car) {
            $form.find('[name="car"]').val(data.car);
        }

        if (typeof grecaptcha !== 'undefined') {
            $form.find('.g-recaptcha').each(function () {
                const widgetId = $(this).data('widget-id');
                try {
                    if (widgetId !== undefined) {
                        grecaptcha.reset(widgetId);
                    } else {
                        grecaptcha.reset();
                    }
                } catch (error) {
                    grecaptcha.reset();
                }
            });
        }
    }

    function populateErrors($form, errors) {
        Object.entries(errors).forEach(function ([name, fieldErrors]) {
            const $field = $form.find(`[name="${name}"]`).first();
            const $container = $field.length ? getFieldContainer($field) : $form;

            fieldErrors.forEach(function (error) {
                $container.append(`<small class="text-warning js-ajax-field-error">${error}</small>`);
            });
        });
    }

    $(document).on('submit', formSelector, function (e) {
        e.preventDefault();

        const $form = $(this);

        clearErrors($form);

        $.ajax($form.attr('action'), {
            type: $form.attr('method') || 'POST',
            data: $form.serializeArray(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function (data) {
                const {success, ...errors} = data;

                if (success) {
                    clearForm($form, data);
                    $('#modalRegisterForm button.close').trigger('click');
                    showToast();
                } else {
                    populateErrors($form, errors);
                }
            },
            error: function () {
                populateErrors($form, {
                    __all__: ['Не удалось отправить заявку. Попробуйте еще раз.']
                });
            }
        });
    });
})(jQuery);
