require("bootstrap-webpack");
require("jQuery-Scanner-Detection/jquery.scannerdetection");
require("./csrftoken");
var amyshit = require("./ajaxmyshit.js");

$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();
    $(document).bind("scannerDetectionComplete", function(e, data){
        // On successfull scan, write uid to
        // tag authentication form and submit it
        $("#id_tag_uid").val(data.string);
        $("#tag-auth-form").submit();
    });

    $("#magicCodeLoginButton").click(function(event) {
      window.location.href = "magic/"+$("#magicCode").val();
    });

    // This will most probably show "check your email"
    // for the user after they are requested magic
    // login link to their email
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
            $("#messageModal").modal("show");
        });

});
