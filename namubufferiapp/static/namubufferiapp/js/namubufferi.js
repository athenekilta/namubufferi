function updateReceiptModal (data) {
  $( "#timestamp" ).html(data.receipt.timestamp);
  $( "#customer" ).html(data.receipt.customer);
  $( "#product" ).html(data.receipt.product);
  $( "#amount" ).html(data.receipt.amount);
  $( "#transaction_key" ).val(data.receipt.transactionkey);
}

function getReceipt(transactionkey) {
  $('#moneyModal').modal('hide');
  $.get( "/receipt/" + transactionkey)
    .done(function( data ) {
      updateReceiptModal(data);
    });
}

function getTransactionHistory() {
  $.get( "/history/")
    .done(function( data ) {
      $("#history").html(data.transactionhistory);
    });
}

$(document).ready(function() {
    'use strict';
    
    // https://api.jquery.com/jquery.post/
    // Attach a submit handler to the form
    $( "#buy-form" ).submit(function( event ) {
     
      // Stop form from submitting normally
      event.preventDefault();

      // Get some values from elements on the page:
      var $form = $( this ),
        productkey = $form.find( "input[name='product_key']" ).val(),
        url = $form.attr( "action" );
     
      // Send the data using post
      var posting = $.post( url, { product_key: productkey } );
     
      // Put the results in a div
      posting.done(function( data ) {
        console.log(data);
        $('#productModal').modal('hide');
        $( "#balance" ).html(data.balance);
        $( "#receiptModal" ).data( "transactionkey", data.transactionkey );
        $( "#receiptModal" ).modal();
      });
    });
    $( "#money-form" ).submit(function( event ) {
     
      // Stop form from submitting normally
      event.preventDefault();
      
      // Get some values from elements on the page:
      var $form = $( this ),
        amount = $form.find( "input[name='amount']" ).val(),
        url = $form.attr( "action" );
     
      // Send the data using post
      var posting = $.post( url, { amount: amount } );
     
      // Put the results in a div
      posting.done(function( data ) {
        console.log(data);
        $( '#moneyModal' ).modal('hide');
        $( "#balance" ).html(data.balance);
        $( "#receiptModal" ).data( "transactionkey", data.transactionkey );
        $( "#receiptModal" ).modal();
      });
    });

    $('#search').hideseek();
    $(".product").fitText();
    $('#productModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var productkey = button.data('productkey'); // Extract info from data-* attributes
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this);
      modal.find('#product-modal-name').text(button.data('productname'));
      modal.find('#product-modal-pk').val(button.data('productkey'));
      modal.find('#product-modal-price').text(button.data('productprice'));
    });

    $('#receiptModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var transactionkey = button.data('transactionkey') || $(this).data('transactionkey'); // Extract info from data-* attributes
      getReceipt(transactionkey);
    });

    $('#moneyModal').on('show.bs.modal', function (event) {
      getTransactionHistory();
    });
});
