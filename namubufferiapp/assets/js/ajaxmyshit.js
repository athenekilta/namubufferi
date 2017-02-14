/*
 * Ajaxify an form
 * 
 * Prevents default form action and sends form by post.
 * Adds has-error -class to form if request returns errors, 
 * also replaces messageModal's html with data got from request.
 *
 * Callbacks can be attached to successfull and failed states.
 *
 */

function ajaxMyShit (formId, callback, callback_on_error) {
    "use strict";
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
                $form.find(":input").val("");
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
    $("#messageModalBody").html(data.modalMessage);
}

module.exports = ajaxMyShit;
