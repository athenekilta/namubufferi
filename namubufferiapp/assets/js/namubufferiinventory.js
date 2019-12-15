require("bootstrap-webpack")

require("hideseek/jquery.hideseek");
require("jQuery-Scanner-Detection/jquery.scannerdetection");

require("./csrftoken");
var amyshit = require("./ajaxmyshit.js");


// Try to guess product name by its barcode based
// on external resources.
function populate_by_bcode(modal, bcode) {
    modal.find("#id_name").addClass("alert alert-warning");
    modal.find("#id_name").removeClass("alert-success");

    $.getJSON("/product/barcode/discover/"+bcode, function(data) {
        var element = modal.find("#id_name");

        if (element.val() == "")
            modal.find("#id_name").val(data["name"]);

        element.removeClass("alert-warning");
        element.addClass("alert-success");
    })
    .fail(function() {
        modal.find("#id_name").removeClass("alert alert-warning");
    });
}

var product_barcodes;
function update_barcodes() {
    $.getJSON("/product/barcodes/", function(json){
        product_barcodes = json;
    });
}

$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();
    update_barcodes();

    $("#bcode-assign-btn").click(function(event) {
        $(this).addClass("hidden");
    });

    amyshit("#update-product-form", function (data) {
        $("#productUpdateModal").modal("hide");
        location.reload();
    });

    // http://getbootstrap.com/javascript/#modals-related-target
    $("#productUpdateModal").on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);


        // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        if (button.data("mode") === "update") {
            // In case we have barcode active in bcode-assign-btn we want to assign
            // that barcode to product chosen. After that everything should be updated
            // and for now, 
            if (!$("#bcode-assign-btn").hasClass("hidden")) {
                $("#bcode-assign-btn").addClass("hidden");
                var bcode = $("#bcode-assign-btn").data("barcode");
                var pk = button.data("productkey");

                $.ajax({
                    url:"/product/".concat(pk, "/barcode/", bcode),
                    type: "put",
                    complete: function() {
                        update_barcodes();
                        $("#productUpdateModal").modal("hide");
                    },
                });
            }

            // If we get this far, we really want to update the product,
            // not change its barcode
            modal.find("#id_name").val(button.data("productname"));
            modal.find("#id_name").attr("readonly", true);

            modal.find("#id_category").val(button.data("productcategoryid"));
            modal.find("#id_price").val(button.data("productprice"));
            modal.find("#id_inventory").val(button.data("productinventory")); 
            modal.find("#id_hidden").prop("checked", button.data("producthidden"));
            modal.find("#id_barcode").val("");
            modal.find(":submit").text("Update");
        }
        else if (button.data("mode") === "add") {
            modal.find("#id_name").val("");
            modal.find("#id_name").attr("readonly", false);

            modal.find("#id_category").val("");
            modal.find("#id_price").val("");
            modal.find("#id_inventory").val("0"); 
            modal.find("#id_hidden").prop("checked", false);
            modal.find("#id_barcode").val("");
            modal.find(":submit").text("Add");

            if (!$("#bcode-assign-btn").hasClass("hidden")) {
                var bcode = $("#bcode-assign-btn").data("barcode");
                modal.find("#id_barcode").val(bcode);
                populate_by_bcode(modal, bcode);
            }
        }
    });

    $(document).bind("scannerDetectionComplete", function(e, data){
        if (!product_barcodes.hasOwnProperty(data.string)) {
            $("#bcode-assign-btn").removeClass("hidden");
            $("#bcode-assign-btn").data("barcode", data.string);
            $("#bcode-assign-btn-bcode").text(data.string);
        } else {
            var productkey = product_barcodes[data.string];
            $("button[data-productkey="+productkey+"]").click();
        }
    });

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
