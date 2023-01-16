const $form = $('#online-appointment-form'),
    closeBtn = document.querySelector('#modalRegisterForm button.close'),
    fullNameSelector = document.querySelector('input[name=full_name]'),
    carSelector = document.querySelector('input[name=car]'),
    phoneSelector = document.querySelector('input[name=phone]'),
    captchaSelector = document.querySelector('#id_captcha'),
    branchSelector = document.querySelector('#id_branch');

const mapping = {
    full_name: {
        populateErrors: (errors) => {
            populateInputWithErrors(errors, fullNameSelector)
        },
        clear: () => {
            fullNameSelector.value = '';
            fullNameSelector.parentElement.querySelector('small.text-warning')?.remove()
        },
        setValue: (value) => {
            fullNameSelector.value = value
        }
    },
    car: {
        populateErrors: (errors) => {
            populateInputWithErrors(errors, carSelector)
        },
        clear: () => {
            carSelector.value = '';
            carSelector.parentElement.querySelector('small.text-warning')?.remove()
        },
        setValue: (value) => {
            carSelector.value = value
        }
    },
    phone: {
        populateErrors: (errors) => {
            populateInputWithErrors(errors, phoneSelector)
        },
        clear: () => {
            phoneSelector.value = '';
            phoneSelector.parentElement.querySelector('small.text-warning')?.remove()
        },
        setValue: (value) => {
            phoneSelector.value = value
        }
    },
    captcha: {
        populateErrors: (errors) => {
            populateInputWithErrors(errors, captchaSelector)
        },
        clear: () => {
            grecaptcha.reset();
            captchaSelector.parentElement.querySelector('small.text-warning')?.remove()
        },
    },
    branch: {
        populateErrors: (errors) => {
            populateInputWithErrors(errors, branchSelector.parentElement.parentElement.parentElement.parentElement)
        },
        clear: () => {
            branchSelector.querySelector('option').value = '';
            branchSelector.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('small.text-warning')?.remove()
        },
    }

}

function populateInputWithErrors(errors, selector) {
    console.log(errors, ' for ', name)
    console.log(selector)
    for (const error of errors) {
        selector.insertAdjacentHTML('afterend', `<small class="text-warning">${error}</small>`);
    }
}

$form.on('submit', function (e) {
    e.preventDefault();

    $.ajax($form.attr('action'), {
        type: $form.attr('method'),
        data: $form.serializeArray(),
        success: function (data, status, xhr) {
            console.log(data)
            const {success, ...errors} = data;

            if (success) {
                for (const [name, obj] of Object.entries(mapping)) {
                    if (Object.hasOwn(data, name))
                        obj.setValue(data[name])
                    else
                        obj.clear();
                }
                closeBtn.click();
                launch_toast();
            } else {
                for (const [name, fieldErrors] of Object.entries(errors)) {
                    mapping[name].populateErrors(fieldErrors);
                    console.log(document.querySelector(`input[name=${name}]`))
                    document.querySelector(`input[name=${name}]`)
                }
            }
        }
    })
})
