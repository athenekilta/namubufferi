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
   
    // Tag auth form is filled by scannerDetector
    // which means there's no reason to directly show
    // it to user.
    $('#tag-auth-form').addClass('hidden');
    ajaxMyShit('#tag-auth-form', function (data) {
        if (typeof(data.redirect) !== 'undefined')
                  window.location.href = data.redirect;
      },
      function(errordata) {
        $('#tag-auth-form').removeClass('hidden');
        if (errordata.errors['tag_uid'][0].code == 'tagnotfound') {
          $('#tag-auth-error').removeClass('hidden');
          $('#tag-auth-error').text(errordata.errors['tag_uid'][0].message);
        }
    });

    // we want to attach scanner detection to whole document, but only
    // in login page. this is done by detecting tag authentication form
    $('#tag-auth-form').parentsUntil('html').scannerDetection(function(data){
        $('#id_tag_uid').val(data);
        $('#tag-auth-form').submit();
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


    function updateTagsModal() {
      $.get('/tag/').done(function(data) {
                $('#tags').html(data.taglist);
            });
      $('#tags').off('click', 'button');
      $('#tags').on('click', 'button', function(clickevent) {
          var uid = $(clickevent.currentTarget).data('uid');
          $.ajax({
                  url:'/tag/'.concat(uid, '/'),
                  type: 'DELETE',
                  complete: updateTagsModal
                });
        });
    }

    $('#tagModal').on('show.bs.modal', function(event) {
        updateTagsModal();

        $('html').scannerDetection(function(data){
           $.ajax({
                  url:'/tag/'.concat(data, '/'),
                  type: 'POST',
                  complete: updateTagsModal
                });
        });
    });
    $('#tagModal').on('hide.bs.modal', function(event) {
        $('html').scannerDetection(false);
    });
   
});
