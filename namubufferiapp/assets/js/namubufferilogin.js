require("bootstrap-webpack");
require("jQuery-Scanner-Detection/jquery.scannerdetection");

require("./csrftoken");
var amyshit = require("./ajaxmyshit.js");

$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();
    $(document).bind("scannerDetectionComplete", function(e, data){
        // On successfull scan, apply uid to
        // tag authentication form and submit it
        $("#id_tag_uid").val(data.string);
        $("#tag-auth-form").submit();
    });

    amyshit("#magic-auth-form", function () {
        $("#messageModal").modal("show");
    });


    // Tag-auth-form is meant to be filled by scannerDetector
    // which means there's no reason to directly show
    // it to user.
    $("#tag-auth-form").addClass("hidden");
    amyshit("#tag-auth-form",
        function (data) {
            // On success, we should get the next
            // waypoint as a response
            if (typeof(data.redirect) === "string")
                window.location.href = data.redirect;
        },
        function(errordata) {
            // On error, show the field for user. Maybe
            // it has something they can fix
            $("#tag-auth-form").removeClass("hidden");
            if (errordata.errors["tag_uid"][0].code == "tagnotfound") {
                $("#tag-auth-error").removeClass("hidden");
                $("#tag-auth-error").text(errordata.errors["tag_uid"][0].message);
            }
        });

});
