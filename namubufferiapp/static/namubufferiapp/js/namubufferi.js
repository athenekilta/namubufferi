function ajaxMyShit (formId, callback) {
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
        $('#successModal').modal('show');
        setTimeout(function(){
          $('#successModal').modal('hide')
        }, 1750);
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

    // http://getbootstrap.com/javascript/#modals-related-target
    $('#productModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this);
        modal.find('#product-modal-name').text(button.data('productname'));
        modal.find('#product-modal-pk').val(button.data('productkey'));
        modal.find('#product-modal-price').text(button.data('productprice'));
        modal.find('#product-modal-inventory').text(button.data('productinventory'));
    });

    $('#receiptModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var transactionkey = button.data('transactionkey') || $(this).data('transactionkey');
        //$('#historyModal').modal('hide');
        $.post("/receipt/", { transaction_key: transactionkey })
            .done(function(data) {
                $("#receiptModal").toggleClass( "canceled", data.receipt.canceled );
                $("#timestamp").html(data.receipt.timestamp);
                $("#customer").html(data.receipt.customer);
                $("#product").html(data.receipt.product);
                $("#amount").html(data.receipt.amount);
                $("#transaction_key").val(data.receipt.transactionkey);
            });
    });

    $('#historyModal').on('show.bs.modal', function(event) {
        $.get("/history/")
            .done(function(data) {
                $("#history").html(data.transactionhistory);
            });
    });
    $('#historycheckbox').change(function(){
        $('.canceled').toggle(this.checked);
    });
    // Search: Add class to parent when focusing on child
    $('.namu-search > *')
    .focus(function() {
        $('.namu-search').addClass('namu-search-focused');
    })
    .blur(function() {
        $('.namu-search').removeClass('namu-search-focused');
    });

});
