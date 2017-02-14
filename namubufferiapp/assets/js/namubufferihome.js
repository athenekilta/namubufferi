require("bootstrap-webpack") 

require("hideseek/jquery.hideseek");


require("./csrftoken");

require("jQuery-Scanner-Detection/jquery.scannerdetection");

var amyshit = require("./ajaxmyshit.js");

function updateTagsModal() { 
    $.get("/tag/").done(function(data) { 
        $("#tags").html(data.taglist);
    });

    //Needed to unbind previously binded buttons.
    //Otherwise we would get multiple events per click.
    $("#tags").off("click", "button");
    $("#tags").on("click", "button", function(clickevent) { 
        var uid = $(clickevent.currentTarget).data("uid");
        $.ajax({
            url:"/tag/".concat(uid, "/"),
            type: "DELETE",
            complete: updateTagsModal
        });
    });
}


$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();

    amyshit("#buy-form", function (data) {
        $("#productModal").modal("hide");
        $("#receiptModal").data("transactionkey", data.transactionkey);
        $("#receiptModal").modal("show");

        $(".balance").text(data.balance + "€");
        if(data.balance < 0) {
            $(".balance").addClass("text-danger");
        } else {
            $(".balance").removeClass("text-danger");
        }


    });
    amyshit("#money-form", function (data) {
        $("#moneyModal").modal("hide");
        $("#receiptModal").data("transactionkey", data.transactionkey);
        $("#receiptModal").modal("show");


        $(".balance").text(data.balance + "€");
        if(data.balance < 0) {
            $(".balance").addClass("text-danger");
        } else {
            $(".balance").removeClass("text-danger");
        }


    });
    amyshit("#cancelform", function (data) {
        $("#receiptModal").modal("hide");
        $("#messageModal").modal("show");

        $(".balance").text(data.balance + "€");
        if(data.balance < 0) {
            $(".balance").addClass("text-danger");
        } else {
            $(".balance").removeClass("text-danger");
        }

    });


    var product_barcodes;
    $.getJSON("/product/barcodes/", function(json){
        product_barcodes = json;
    });

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

    $(document).bind("scannerDetectionComplete", function(e, data){

        // Add a tag in tag handling modal
        if ($("#tagModal").hasClass("in")) { 
            // try to create a new tag if it was read
            $.ajax({
                url:"/tag/".concat(data.string, "/"),
                type: "post",
                complete: updateTagsModal
            });
        } 
    });


    $("#tagModal").on("show.bs.modal", function(event) { 
        updateTagsModal();
    });


    $( "#search" ).focus(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
        //$( window ).scrollTop(0);
    });
    $( "#search" ).focusout(function(event) {
        //$( window ).scrollTop($("#search").offset().top);
        $( window ).scrollTop($("#page-top").offset().top);
    });
    $( "#search" ).keypress(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
        //$( window ).scrollTop(0);
    });

    $("#search").hideseek();


    $( "#id_euros" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_euros" ).val("");
    });
    $( "#id_euros" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if(!cents.val()) {
            cents.val("00");
        }
        var euros = $( "#id_euros" );
        if(!euros.val()) {
            euros.val("00");
        }
    });
    $( "#id_cents" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_cents" ).val("");
    });
    $( "#id_cents" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if (cents.val().length == 1){
            cents.val("0"+cents.val());
        } else if(!cents.val()) {
            cents.val("00");
        }
    });


});
