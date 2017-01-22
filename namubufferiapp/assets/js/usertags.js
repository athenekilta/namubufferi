var amyshit = require("./ajaxmyshit.js");

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
    amyshit("#tag-auth-form", function (data) {
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

    $(document).bind("scannerDetectionComplete", function(e, data){
        // Add a tag in tag handling modal
        if (($("#tagmodal").data('bs.modal') || {isshown: false}).isshown) {
            // try to create a new tag if it was read
            $.ajax({
                url:"/tag/".concat(data.string, "/"),
                type: "post",
                complete: updatetagsmodal
            });
        }
    });

    $(document).bind("scannerDetectionComplete", function(e, data){
        $("#id_tag_uid").val(data.string);
        $("#tag-auth-form").submit();
    });


    $("#tagModal").on("show.bs.modal", function(event) {
        updateTagsModal();
    });

});
