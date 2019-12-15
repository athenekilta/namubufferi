require("bootstrap-webpack") 
require("hideseek/jquery.hideseek");
require("jQuery-Scanner-Detection/jquery.scannerdetection");

require("./csrftoken");
var amyshit = require("./ajaxmyshit.js");


$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();

    var product_barcodes;
    $.getJSON("/product/barcodes/", function(json){
        product_barcodes = json;
    });

    amyshit("#buy-form", function (data) {
        // Redirect to login after successful buy
        // as no receipt is shown in anonymous mode
        window.location.href = "/";
    });


    // Some product was clicked to show the generic product modal
    // now it should be populated with correct values
    $("#productModal").on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);
        modal.find("#product-modal-name").text(button.data("productname"));
        modal.find("#product-modal-pk").val(button.data("productkey"));
        modal.find("#product-modal-price").text(button.data("productprice"));
        modal.find("#product-modal-inventory").text(button.data("productinventory")); 
    });


    $(document).bind("scannerDetectionComplete", function(e, data){
        // If we find a product with the same barcode as scanned
        // one is, lets click it from the list
        try {
            if ( product_barcodes.hasOwnProperty(data.string)) {
                var productkey = product_barcodes[data.string];
                $("button[data-productkey="+productkey+"]").click();
            }
        }
        catch(err){}
    });

    
    // UI tweaks for positioning on the site when using search bar
    $( "#search" ).focus(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
    });
    $( "#search" ).focusout(function(event) {
        $( window ).scrollTop($("#page-top").offset().top);
    });
    $( "#search" ).keypress(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
    });

    $("#search").hideseek();
});
