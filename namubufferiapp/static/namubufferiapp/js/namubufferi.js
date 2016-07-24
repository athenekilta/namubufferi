function getReceipt(productkey) {
  $('#moneyModal').modal('hide');
  $.get( "/receipt/" + productkey)
    .done(function( data ) {
      $( "#receiptModal" ).find('.modal-content').replaceWith( data );
      $( "#receiptModal" ).modal();
    });
}

$(document).ready(function() {
    'use strict';

    // https://docs.djangoproject.com/en/1.9/ref/csrf/#ajax
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // https://api.jquery.com/jquery.post/
    // Attach a submit handler to the form
    $( "#buy-form" ).submit(function( event ) {
     
      // Stop form from submitting normally
      event.preventDefault();
      console.log("lol");
      // Get some values from elements on the page:
      var $form = $( this ),
        productkey = $form.find( "input[name='product_key']" ).val(),
        url = $form.attr( "action" );
     
      // Send the data using post
      var posting = $.post( url, { product_key: productkey } );
     
      // Put the results in a div
      posting.done(function( data ) {
        console.log(data);
        $( "#balance" ).html(data.balance);
        $('#productModal').modal('hide');
        $( "#receiptModal" ).find('.modal-content').replaceWith( data.receipt );
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

});
