$(function () {
    const close_tag = '<span class="ml-2 text-danger" style="cursor: pointer;" id="remove_reply">❌</span>'
    const
        $form = $('#commentform'),
        $reply_input_field = $('#id_reply_to'),
        $reply_to_tag = $('#answer_to');

    // Change <input name="reply_to" /> value to data-reply-id attribute of pressed link,
    $('a.reply-button').on('click', function (e) {
        e.preventDefault();

        $reply_input_field.val($(this).attr('data-reply-id'));
        $reply_to_tag.html($(this).attr('aria-label') + close_tag)

        // Scroll to $form and focus text field
        $("html, body").animate({scrollTop: $form.offset().top - $form.height()});
        $('#id_text').focus();
    });

    // Abort reply_to
    $form.on('click', '#remove_reply', {}, function () {
        $reply_input_field.val(undefined);
        $reply_to_tag.html('');
    });
});
