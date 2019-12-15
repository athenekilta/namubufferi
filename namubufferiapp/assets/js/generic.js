
require("../css/style.css");
require("./csrftoken.js");


$(document).ready(function() {
    "use strict";

    $(".modal").on("shown.bs.modal", function() {
        $(this).find("[autofocus]").focus();
    });

});
