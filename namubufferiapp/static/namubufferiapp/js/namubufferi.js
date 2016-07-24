
$(document).ready(function() {
    'use strict';
    $('#search').hideseek();
    $(".product").fitText();
    $('#receiptModal').modal();    
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
});
