$(document).ready(function() {
	"use strict";

	// http://getbootstrap.com/javascript/#modals-related-target
	$("#productModal").on("show.bs.modal", function(event) {
		var button = $(event.relatedTarget); // Button that triggered the modal
		// Extract info from data-* attributes
		// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
		// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
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


	$("html").scannerDetection(function(data){
		// Authentication by tag
		if ($("#tag-auth-form").length) {
			$("#id_tag_uid").val(data);
			$("#tag-auth-form").submit();
		}

		// Add a tag in tag handling modal
		if (($("#tagmodal").data('bs.modal') || {isshown: false}).isshown) {
			// try to create a new tag if it was read
			$.ajax({
				url:"/tag/".concat(data, "/"),
				type: "post",
				complete: updatetagsmodal
			});
		}

		// Open a product with tag
		if (product_barcodes.hasOwnProperty(data)) {
			var productkey = product_barcodes[data];
			$('button[data-productkey='+productkey+']').click();
		}
	});


});
