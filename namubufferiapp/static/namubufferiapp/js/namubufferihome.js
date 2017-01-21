$(document).ready(function() {
    "use strict";

    $("#productModal").on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);
        modal.find("#product-modal-name").text(button.data("productname"));
        modal.find("#product-modal-pk").val(button.data("productkey"));
        modal.find("#product-modal-price").text(button.data("productprice"));
        modal.find("#product-modal-inventory").text(button.data("productinventory")); 
    });

    $("#receiptModal").on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget);
        var transactionkey = button.data("transactionkey") || $(this).data("transactionkey");
        //$("#historyModal").modal("hide");
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

    $("#historyModal").on("show.bs.modal", function(event) {
        $.get("/history/")
            .done(function(data) {
                $("#history").html(data.transactionhistory);
            });
    });
    $("#historycheckbox").change(function(){
        $(".canceled").toggle(this.checked);
    });

    /* global product_barcodes */
    $(document).bind("scannerDetectionComplete", function(e, data){
        // Open a product with tag
        try {
            if ( product_barcodes.hasOwnProperty(data.string)) {
                var productkey = product_barcodes[data.string];
                $("button[data-productkey="+productkey+"]").click();
            }
        }
        catch(err){}
    });
});
