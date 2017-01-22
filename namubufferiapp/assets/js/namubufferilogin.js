require("bootstrap-webpack")
require("./csrftoken");

require("jQuery-Scanner-Detection/jquery.scannerdetection");


var amyshit = require("./ajaxmyshit.js");

$(document).ready(function() {
    "use strict";
    
    $(document).scannerDetection();

    amyshit("#register-form", function (data) {
        $("#authModal").modal("hide");
        $("#messageModal").modal("show");
    });
    amyshit("#magic-auth-form", function (data) {
        $("#messageModal").modal("show");
    });



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
        $("#id_tag_uid").val(data.string);
        $("#tag-auth-form").submit();
    });
});
