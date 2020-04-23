$(function() {
    $('#add_computer_btn').on('click', function (e) {
        e.preventDefault(); // disable the default form submit event

        var $form = $('#replyForm');

        $.ajax({
            url: $form.attr("action"),
            type: $form.attr("method"),
            data: $form.serialize(),
            success: function (response) {
                alert('response received');
                // ajax success callback
            },
            error: function (response) {
                alert('ajax failed');
                // ajax error callback
            },
        });
    });
});