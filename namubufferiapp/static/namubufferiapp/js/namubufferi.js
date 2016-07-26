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
            console.log(data);
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


$(document).ready(function() {
    'use strict';

    ajaxMyShit('#buy-form', function (data) {
         $('#productModal').modal('hide');
         $(".balance").html(data.balance);
         $("#messageModalBody").html(data.modalMessage);
         //$("#messages").prepend(data.message);
         $("#receiptModal").data("transactionkey", data.transactionkey);
         $("#receiptModal").modal();
    });

    ajaxMyShit('#money-form', function (data) {
        console.log(data);
        $('#moneyModal').modal('hide');
        $(".balance").html(data.balance);
        $("#messageModalBody").html(data.modalMessage);
        //$("#messages").prepend(data.message);
        $("#receiptModal").data("transactionkey", data.transactionkey);
        $("#receiptModal").modal();
    });

    ajaxMyShit('#cancelform', function (data) {
        console.log(data);
        $('#receiptModal').modal('hide');
        $(".balance").html(data.balance);
        $("#messageModalBody").html(data.modalMessage);
        $('#messageModal').modal('show');
        //$("#messages").prepend(data.message);
    });
    ajaxMyShit('#register-form', function (data) {
        console.log(data);
        $('#authModal').modal('hide');
        $("#messageModalBody").html(data.modalMessage);
        $('#messageModal').modal('show');
        //$("#messages").prepend(data.message);
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
    });

    $('#receiptModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var transactionkey = button.data('transactionkey') || $(this).data('transactionkey');
        $('#historyModal').modal('hide');
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

    $('.modal').on('shown.bs.modal', function() {
      $(this).find('[autofocus]').focus();
    });

    $( "#id_euros" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_euros" ).val('');
    });
    $( "#id_euros" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if(!cents.val()) {
            cents.val('00');
        }
        var euros = $( "#id_euros" );
        if(!euros.val()) {
            euros.val('00');
        }
    });
    $( "#id_cents" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_cents" ).val('');
    });
    $( "#id_cents" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if (cents.val().length == 1){
            cents.val('0'+cents.val());
        } else if(!cents.val()) {
            cents.val('00');
        }
    });
    $( "#search" ).focus(function(event) {
        $( window ).scrollTop($("#search").offset().top);
        //$( window ).scrollTop(0);
    });
    $( "#search" ).focusout(function(event) {
        //$( window ).scrollTop($("#search").offset().top);
        $( window ).scrollTop(0);
    });
    $( "#search" ).keypress(function(event) {
        $( window ).scrollTop($("#search").offset().top);
        //$( window ).scrollTop(0);
    });

    $('#search').hideseek();
    $(".product").fitText();
});
