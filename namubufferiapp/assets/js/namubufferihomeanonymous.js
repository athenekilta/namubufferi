require("bootstrap-webpack") 

require("fittext/dist/jquery.fittext");
require("hideseek/jquery.hideseek");


require("./csrftoken");

require("jQuery-Scanner-Detection/jquery.scannerdetection");

var amyshit = require("./ajaxmyshit.js");


$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();

    amyshit("#buy-form", function (data) {
        // Redirect to login after successful buy
        window.location.href = "/";
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
    $(".product").fitText();

});
