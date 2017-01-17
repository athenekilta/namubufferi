function ajaxMyShit (formId, callback, callback_on_error) {
    'use strict';
    // https://api.jquery.com/jquery.post/
    // Attach a submit handler to the form
    $(formId).submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        // Select this form
        var $form = $(this);
        // Send the data using post
        console.log($form.serialize());
        var posting = $.post($form.attr( "action" ), $form.serialize());
        // Call callback with the results
        posting.done( function (data) {
            parseMyAjaxShit(data);
            $form.find(":input").parent().removeClass("has-error");
            if (!data.errors) {
                $form.find(":input").val('');
                callback(data);
            } else {
                for (var field in data.errors) {
                    for (var i = 0; i < data.errors[field].length; i++) {
                        console.log(data.errors[field][i].message);
                        console.log(data.errors[field][i].code);
                        $form.find("input[name='"+field+"']").parent().addClass("has-error");
                    }
                }
                if (typeof(callback_on_error) === typeof(Function))
                  callback_on_error(data);
            }
        });
    });
}

function parseMyAjaxShit(data) {
    console.log(data);
    $(".balance").text(data.balance + '€');
    if(data.balance < 0) {
        $(".balance").addClass("text-danger");
    } else {
        $(".balance").removeClass("text-danger");
    }
    $("#messageModalBody").html(data.modalMessage);
    //$("#messages").prepend(data.message);
    $("#receiptModal").data("transactionkey", data.transactionkey);

}


$(document).ready(function() {
    'use strict';

    ajaxMyShit('#buy-form', function (data) {
        $('#productModal').modal('hide');
        $("#receiptModal").modal('show');
    });
    ajaxMyShit('#money-form', function (data) {
        $('#moneyModal').modal('hide');
        $("#receiptModal").modal('show');
    });
    ajaxMyShit('#cancelform', function (data) {
        $('#receiptModal').modal('hide');
        $('#messageModal').modal('show');
    });
    ajaxMyShit('#register-form', function (data) {
        $('#authModal').modal('hide');
        $('#messageModal').modal('show');
    });
    ajaxMyShit('#magic-auth-form', function (data) {
        $('#messageModal').modal('show');
    });
});
