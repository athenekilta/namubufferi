$(document).ready(function() {
    'use strict';

    // https://api.jquery.com/jquery.post/
    // Attach a submit handler to the form
    $("#buy-form").submit(function(event) {

        // Stop form from submitting normally
        event.preventDefault();

        // Get some values from elements on the page:
        var $form = $(this),
            productkey = $form.find("input[name='product_key']").val(),
            url = $form.attr("action");

        // Send the data using post
        var posting = $.post(url, {
            product_key: productkey
        });

        // Put the results in a div
        posting.done(function(data) {
            $('#productModal').modal('hide');
            $("#balance").html(data.balance);
            $("#receiptModal").data("transactionkey", data.transactionkey);
            $("#receiptModal").modal();
        });
    });
    $("#money-form").submit(function(event) {
        event.preventDefault();
        var $form = $(this),
            amount = $form.find("input[name='amount']").val(),
            url = $form.attr("action");
        var posting = $.post(url, {
            amount: amount
        });
        posting.done(function(data) {
            $('#moneyModal').modal('hide');
            $("#balance").html(data.balance);
            $("#receiptModal").data("transactionkey", data.transactionkey);
            $("#receiptModal").modal();
        });
    });

    // http://getbootstrap.com/javascript/#modals-related-target
    $('#productModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var productkey = button.data('productkey'); // Extract info from data-* attributes
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
        $('#moneyModal').modal('hide');
        $.get("/receipt/" + transactionkey)
            .done(function(data) {
                $("#timestamp").html(data.receipt.timestamp);
                $("#customer").html(data.receipt.customer);
                $("#product").html(data.receipt.product);
                $("#amount").html(data.receipt.amount);
                $("#transaction_key").val(data.receipt.transactionkey);
            });
    });

    $('#moneyModal').on('show.bs.modal', function(event) {
        $.get("/history/")
            .done(function(data) {
                $("#history").html(data.transactionhistory);
            });
    });


    $('#search').hideseek();
    $(".product").fitText();
});
