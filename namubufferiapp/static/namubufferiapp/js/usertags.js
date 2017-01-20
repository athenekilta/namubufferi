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


    $("#tagModal").on("show.bs.modal", function(event) {
        updateTagsModal();
    });

});
