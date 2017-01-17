// tags is a element which stores a list
// of user identification tags.
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

    // Tag auth form is filled by scannerDetector
    // which means there"s no reason to directly show
    // it to user.
    $("#tag-auth-form").addClass("hidden");
    ajaxMyShit("#tag-auth-form", function (data) {
        // On success, we should get the next
        // waypoint as response
        if (typeof(data.redirect) !== "undefined")
            window.location.href = data.redirect;
        },
        function(errordata) {
            $("#tag-auth-form").removeClass("hidden");
            if (errordata.errors["tag_uid"][0].code == "tagnotfound") {
                $("#tag-auth-error").removeClass("hidden");
                $("#tag-auth-error").text(errordata.errors["tag_uid"][0].message);
        }
    });

    // we want to attach scanner detection to whole document, but only
    // in login page. this is done by detecting tag authentication form
    $("#tag-auth-form").parentsUntil("html").scannerDetection(function(data){
        $("#id_tag_uid").val(data);
        $("#tag-auth-form").submit();
    });


    // Same thing with managment modal. We want scanner
    // to be active while the modal is active but not
    // at any different time.
    $("#tagModal").on("show.bs.modal", function(event) {
        updateTagsModal();

        $("html").scannerDetection(function(data){
            // Try to create a new tag if it was read
            $.ajax({
                url:"/tag/".concat(data, "/"),
                type: "POST",
                complete: updateTagsModal
            });
        });
    });
    $("#tagModal").on("hide.bs.modal", function(event) {
        // Shut off the scanner when closing the modal
        $("html").scannerDetection(false);
    });

});
